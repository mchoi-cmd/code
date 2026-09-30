#!/usr/bin/env python3
"""Anime downloader that searches SubsPlease and adds torrents to Transmission."""
import argparse
import json
import sys
from pathlib import Path

import requests

from subsplease import DEFAULT_SUBSPLEASE_URL, search_for_magnet
from transmission import DEFAULT_TRANSMISSION_URL, add_to_transmission

DEFAULT_DOWNLOAD_DIR = "/Volumes/BT/Videos"
DEFAULT_RESOLUTIONS = [480, 720, 1080]


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
        keys = ["anime", "shows", "entries", "list"]
        entries = next((data.get(key) for key in keys if data.get(key)), [])
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
        key = (
            item.get("resolutions")
            or item.get("resolution")
            or item.get("res")
            or item.get("quality")
        )
        resolutions = normalize_resolution_list(key)
        normalized.append({"title": str(title).strip(), "resolutions": resolutions})

    if not normalized:
        raise ValueError(f"No valid anime entries found in {json_path}")
    return normalized


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Download anime torrents from SubsPlease and add them to "
            "Transmission."
        )
    )
    parser.add_argument(
        "--input",
        default="anime_list.json",
        help=(
            "Path to the JSON file containing anime titles and "
            "preferred resolutions."
        ),
    )
    parser.add_argument(
        "--download-dir",
        default=DEFAULT_DOWNLOAD_DIR,
        help="Transmission download directory.",
    )
    parser.add_argument(
        "--subsplease-url",
        default=DEFAULT_SUBSPLEASE_URL,
        help="Base URL for SubsPlease.",
    )
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
            result = add_to_transmission(
                session,
                args.download_dir,
                magnet,
                args.transmission_url,
            )
            print(f"  [OK] Added {title} to Transmission:")
            print(f"      {json.dumps(result, ensure_ascii=False, indent=2)}")
        except Exception as exc:
            print(
                f"  [ERROR] Could not add {title} to Transmission: {exc}",
                file=sys.stderr,
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
