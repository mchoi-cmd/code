#!/usr/bin/env python3
"""Anime downloader that searches SubsPlease and adds torrents to Transmission."""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import requests

DEFAULT_SUBSPLEASE_URL = "https://subsplease.org"
DEFAULT_TRANSMISSION_URL = "http://192.168.1.103:9093/transmission/rpc"
DEFAULT_DOWNLOAD_DIR = "/Volumes/BT/Videos"
DEFAULT_RESOLUTIONS = [480, 720, 1080]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def normalize_resolution_list(value):
    if value is None:
        return list(DEFAULT_RESOLUTIONS)
    if isinstance(value, int):
        return [value]
    if isinstance(value, str):
        return [int(v.strip()) for v in value.split(",") if v.strip()]
    if isinstance(value, list):
        return [int(v) for v in value]
    return list(DEFAULT_RESOLUTIONS)


def load_entries(json_path):
    path = Path(json_path)
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    if isinstance(data, list):
        entries = data
    elif isinstance(data, dict):
        entries = data.get("anime") or data.get("shows") or data.get("entries") or data.get("list") or []
        if isinstance(entries, dict):
            entries = [entries]
    else:
        raise ValueError(f"Unsupported JSON structure in {json_path}")

    normalized = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        title = item.get("title") or item.get("name") or item.get("anime")
        if not title:
            continue
        resolutions = normalize_resolution_list(item.get("resolutions") or item.get("resolution") or item.get("res") or item.get("quality"))
        normalized.append({"title": str(title).strip(), "resolutions": resolutions})

    if not normalized:
        raise ValueError(f"No valid anime entries found in {json_path}")
    return normalized


def build_search_urls(subsplease_url, title):
    search_variants = [
        title,
        title.replace(" - ", " "),
        title.replace(" ", "+"),
    ]
    seen = set()
    urls = []
    for variant in search_variants:
        if not variant:
            continue
        cleaned = variant.strip()
        if cleaned in seen:
            continue
        seen.add(cleaned)
        urls.extend(
            [
                f"{subsplease_url}/?s={quote_plus(cleaned)}",
                f"{subsplease_url}/search/?s={quote_plus(cleaned)}",
                f"{subsplease_url}/shows/?s={quote_plus(cleaned)}",
                f"{subsplease_url}/rss/?search={quote_plus(cleaned)}",
            ]
        )
    return urls


def extract_resolution_from_magnet(magnet_url):
    try:
        parsed = urlparse(magnet_url)
        query = parse_qs(parsed.query)
        dn_value = query.get("dn", [""])[0]
        decoded = unquote(dn_value)
        match = re.search(r"(?<!\d)(\d{3,4})p", decoded, re.IGNORECASE)
        if match:
            return int(match.group(1))
        match = re.search(r"(?<!\d)(\d{3,4})\s*p", decoded, re.IGNORECASE)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return None


def magnet_candidates_from_html(text):
    candidates = set()
    pattern = r"magnet:\?[^\s\"'<>]+"
    for match in re.finditer(pattern, text, re.IGNORECASE):
        candidates.add(match.group(0))
    for match in re.finditer(r"href=[\"'](magnet:\?[^\"']+)[\"']", text, re.IGNORECASE):
        candidates.add(match.group(1))
    return sorted(candidates)


def pick_best_magnet(magnets, preferred_resolutions):
    if not magnets:
        raise RuntimeError("No magnet links found for this title")

    exact_matches = []
    fallback_matches = []

    for magnet in magnets:
        res = extract_resolution_from_magnet(magnet)
        if res is None:
            fallback_matches.append((magnet, None, float("inf")))
            continue

        if res in preferred_resolutions:
            exact_matches.append((magnet, res, preferred_resolutions.index(res)))
        else:
            closest = min(abs(res - pref) for pref in preferred_resolutions)
            fallback_matches.append((magnet, res, closest))

    if exact_matches:
        exact_matches.sort(key=lambda item: item[2])
        return exact_matches[0][0]

    if fallback_matches:
        fallback_matches.sort(key=lambda item: item[2])
        return fallback_matches[0][0]

    return magnets[0]


def search_for_magnet(subsplease_url, title, preferred_resolutions):
    urls = build_search_urls(subsplease_url, title)
    seen_magnets = set()

    for url in urls:
        try:
            response = requests.get(url, headers=HEADERS, timeout=20)
            response.raise_for_status()
        except requests.RequestException:
            continue

        text = response.text
        magnets = magnet_candidates_from_html(text)
        for magnet in magnets:
            if magnet in seen_magnets:
                continue
            seen_magnets.add(magnet)

    if not seen_magnets:
        raise RuntimeError(f"Could not find a magnet link for {title} on {subsplease_url}")

    return pick_best_magnet(sorted(seen_magnets), preferred_resolutions)


def transmission_request(session, url, payload):
    headers = {"Content-Type": "application/json"}
    response = session.post(url, json=payload, headers=headers, timeout=30)

    if response.status_code == 409 and "X-Transmission-Session-Id" in response.headers:
        session.headers["X-Transmission-Session-Id"] = response.headers["X-Transmission-Session-Id"]
        response = session.post(url, json=payload, headers=headers, timeout=30)

    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}


def add_to_transmission(session, download_dir, magnet_url, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "method": "free_space",
        "params": {"path": download_dir},
        "id": "webui",
    }
    transmission_request(session, rpc_url, payload)

    payload = {
        "jsonrpc": "2.0",
        "method": "torrent_add",
        "params": {"download_dir": download_dir, "filename": magnet_url, "paused": False},
        "id": "webui",
    }
    return transmission_request(session, rpc_url, payload)


def main():
    parser = argparse.ArgumentParser(description="Download anime torrents from SubsPlease and add them to Transmission.")
    parser.add_argument("--input", default="anime_list.json", help="Path to the JSON file containing anime titles and preferred resolutions.")
    parser.add_argument("--download-dir", default=DEFAULT_DOWNLOAD_DIR, help="Transmission download directory.")
    parser.add_argument("--subsplease-url", default=DEFAULT_SUBSPLEASE_URL, help="Base URL for SubsPlease.")
    parser.add_argument(
        "--transmission-url",
        default=DEFAULT_TRANSMISSION_URL,
        help="Transmission RPC endpoint.",
    )
    args = parser.parse_args()

    try:
        entries = load_entries(args.input)
    except Exception as exc:
        print(f"Error reading input JSON: {exc}", file=sys.stderr)
        return 1

    session = requests.Session()

    for item in entries:
        title = item["title"]
        preferred = item["resolutions"]
        print(f"Searching for: {title} (preferred: {preferred})")
        try:
            magnet = search_for_magnet(args.subsplease_url, title, preferred)
        except Exception as exc:
            print(f"  [ERROR] {title}: {exc}", file=sys.stderr)
            continue

        print(f"  Found magnet: {magnet}")
        try:
            result = add_to_transmission(session, args.download_dir, magnet, args.transmission_url)
            print(f"  [OK] Added {title} to Transmission:")
            print(f"      {json.dumps(result, ensure_ascii=False, indent=2)}")
        except Exception as exc:
            print(f"  [ERROR] Could not add {title} to Transmission: {exc}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
