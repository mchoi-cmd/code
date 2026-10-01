"""Module for interacting with SubsPlease."""

import html
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, quote, unquote, urlparse

import requests

DEFAULT_SUBSPLEASE_URL = "https://subsplease.org"
DEFAULT_RESOLUTIONS = [480, 720, 1080]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 "
        "Safari/537.36"
    ),
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9," "*/*;q=0.8"),
}


def clean_text(value):
    """Normalize HTML/text content into plain text."""
    if value is None:
        return ""
    text = html.unescape(value)
    text = re.sub(r"<[^>]+>", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_title(value):
    """Convert a title to a stable tokenized form for matching."""
    if not value:
        return ""
    text = html.unescape(unquote(value))
    text = clean_text(text)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    return " ".join(text.lower().split())


def title_matches(expected_title, candidate_title):
    """Return True if candidate and expected look like the same show."""
    expected = normalize_title(expected_title)
    candidate = normalize_title(candidate_title)

    if not expected or not candidate:
        return True
    if expected in candidate or candidate in expected:
        return True

    expected_tokens = set(expected.split())
    candidate_tokens = set(candidate.split())
    if not expected_tokens:
        return True

    overlap = expected_tokens & candidate_tokens
    required = max(1, len(expected_tokens) // 2)
    return len(overlap) >= required


def magnet_title_matches(expected_title, magnet):
    """Return whether the magnet display name contains the requested title."""
    display_name = parse_qs(urlparse(magnet).query).get("dn", [""])[0]
    expected = normalize_title(expected_title)
    candidate = normalize_title(display_name)
    return bool(expected and candidate and expected in candidate)


def is_batch_release(episode):
    """Return whether an episode value describes a range of episodes."""
    return re.fullmatch(r"\d+\s*-\s*\d+", str(episode or "").strip()) is not None


def find_release_table(page_html):
    """Find the releases table in the page source if it actually exists."""
    patterns = [
        r'<table[^>]*id=["\']releases-table["\'][^>]*>(.*?)</table>',
        r'<table[^>]*id=["\']release-table["\'][^>]*>(.*?)</table>',
    ]

    for pattern in patterns:
        match = re.search(pattern, page_html, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1)
    return ""


def parse_release_rows(table_html):
    """Parse row entries from a release table when it is populated."""
    rows = []
    row_pattern = re.compile(r"<tr\b[^>]*>.*?</tr>", flags=re.IGNORECASE | re.DOTALL)

    for row_match in row_pattern.finditer(table_html):
        row_html = row_match.group(0)

        title_match = re.search(
            r'<td\s+class=["\']release-item["\'][^>]*>.*?<a[^>]*>(.*?)</a>',
            row_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not title_match:
            continue

        title = clean_text(title_match.group(1))
        if not title:
            continue

        badge_pattern = re.compile(
            r'<a\s+href=["\'](magnet:[^"\']+)["\'][^>]*>'
            r".*?<span[^>]*>\s*(\d{3,4})p\s*</span>",
            flags=re.IGNORECASE | re.DOTALL,
        )

        for magnet_match in badge_pattern.finditer(row_html):
            rows.append(
                {
                    "title": title,
                    "magnet": html.unescape(magnet_match.group(1)),
                    "resolution": int(magnet_match.group(2)),
                }
            )

    return rows


def pick_best_magnet(rows, requested_title, preferred_resolutions):
    """Choose the best magnet for the requested show and resolutions."""
    if not rows:
        raise RuntimeError("No magnet links found for this title")

    rows = [row for row in rows if magnet_title_matches(requested_title, row["magnet"])]
    if not rows:
        raise RuntimeError(
            f"No magnet link contains the requested title '{requested_title}'"
        )

    preferred = [int(res) for res in preferred_resolutions]
    matching = [row for row in rows if title_matches(requested_title, row["title"])]
    if not matching:
        matching = list(rows)

    exact = []
    fallback = []
    for row in matching:
        resolution = int(row["resolution"])
        magnet = row["magnet"]

        if resolution in preferred:
            exact.append((resolution, magnet, preferred.index(resolution)))
        else:
            closest = min(abs(resolution - pref) for pref in preferred)
            fallback.append((closest, magnet))

    if exact:
        exact.sort(key=lambda item: item[2])
        return exact[0][1]

    if fallback:
        fallback.sort(key=lambda item: item[0])
        return fallback[0][1]

    return matching[0]["magnet"]


def parse_api_results(api_payload):
    """Convert the JSON output from the SubsPlease API into row objects."""
    rows = []
    if not isinstance(api_payload, dict):
        return rows

    today = datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=7)

    for release_key, release_data in api_payload.items():
        if not isinstance(release_data, dict):
            continue

        try:
            release_date = datetime.strptime(
                release_data.get("time", ""), "%m/%d/%y"
            ).date()
        except (TypeError, ValueError):
            continue
        if not cutoff <= release_date <= today:
            continue

        title = release_data.get("show") or release_key.split(" - ", 1)[0]
        if is_batch_release(release_data.get("episode")):
            continue
        downloads = release_data.get("downloads") or []
        for download in downloads:
            magnet = download.get("magnet") or ""
            resolution = download.get("res")
            if not magnet or resolution is None:
                continue
            try:
                rows.append(
                    {
                        "title": title,
                        "magnet": magnet,
                        "resolution": int(resolution),
                    }
                )
            except (TypeError, ValueError):
                continue

    return rows


def search_for_magnet(subsplease_url, title, preferred_resolutions):
    """Find the best magnet for a title from SubsPlease's live data."""
    base_url = subsplease_url.rstrip("/")

    # The homepage HTML is only a shell and typically contains an empty
    # releases-table placeholder. The real data is loaded by the API.
    api_url = f"{base_url}/api/?f=search&tz=UTC&s={quote(title)}"
    try:
        api_response = requests.get(api_url, headers=HEADERS, timeout=20)
        api_response.raise_for_status()
        api_payload = api_response.json()
        rows = parse_api_results(api_payload)
        if rows:
            return pick_best_magnet(rows, title, preferred_resolutions)
    except Exception:
        # Fall back to the HTML page if the API fails for any reason.
        pass

    try:
        home_response = requests.get(base_url, headers=HEADERS, timeout=20)
        home_response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Unable to fetch SubsPlease page: {exc}") from exc

    table_html = find_release_table(home_response.text)
    if not table_html:
        raise RuntimeError(
            f"Could not find a matching release for '{title}' in the release table."
        )

    rows = parse_release_rows(table_html)
    if not rows:
        raise RuntimeError(
            f"Could not find a matching release for '{title}' in the release table."
        )

    return pick_best_magnet(rows, title, preferred_resolutions)
