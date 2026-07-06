#!/usr/bin/env python3
"""
fetch_images.py

Fetch REAL stock photos (never AI generated) from Pexels and Unsplash for use
in blog posts. Returns clean JSON that Claude Code can read to pick and place
images, with ready-to-use attribution strings.

Uses only the Python standard library, so there is nothing to pip install.

Auth (set at least one, both are free):
  PEXELS_API_KEY        https://www.pexels.com/api/
  UNSPLASH_ACCESS_KEY   https://unsplash.com/developers

Basic search:
  python fetch_images.py --query "student studying at desk" --limit 8

Batch several queries at once (one JSON block per query):
  python fetch_images.py --batch "focused studying" "college campus" "note taking"

Options:
  --source pexels|unsplash|both   default both
  --orientation landscape|portrait|square   default landscape
  --limit N                        results per source per query, default 6

Unsplash license compliance:
  When you actually USE an Unsplash photo, trigger its download event:
  python fetch_images.py --track "<download_location url from the result>"
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def _get(url, headers):
    headers.setdefault("User-Agent", "Mozilla/5.0 StudyEdge Blog")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_pexels(query, limit, orientation):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return []
    params = {
        "query": query,
        "per_page": limit,
        "orientation": orientation,
    }
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(params)
    try:
        data = _get(url, {"Authorization": key})
    except Exception as e:  # noqa: BLE001
        return [{"error": f"pexels: {e}"}]
    out = []
    for p in data.get("photos", []):
        photographer = p.get("photographer", "Unknown")
        out.append({
            "source": "Pexels",
            "id": p.get("id"),
            "url": p.get("src", {}).get("large2x") or p.get("src", {}).get("large"),
            "preview": p.get("src", {}).get("medium"),
            "width": p.get("width"),
            "height": p.get("height"),
            "avg_color": p.get("avg_color"),
            "alt": p.get("alt", ""),
            "photographer": photographer,
            "photographer_url": p.get("photographer_url", ""),
            "photo_page": p.get("url", ""),
            "attribution_text": f"Photo by {photographer} on Pexels",
            "attribution_html": (
                f'Photo by <a href="{p.get("photographer_url","")}">{photographer}</a> '
                f'on <a href="{p.get("url","")}">Pexels</a>'
            ),
            "track_download": None,
        })
    return out


def search_unsplash(query, limit, orientation):
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return []
    params = {
        "query": query,
        "per_page": limit,
        "orientation": orientation,
        "content_filter": "high",
    }
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(params)
    try:
        data = _get(url, {"Authorization": f"Client-ID {key}"})
    except Exception as e:  # noqa: BLE001
        return [{"error": f"unsplash: {e}"}]
    out = []
    for p in data.get("results", []):
        user = p.get("user", {})
        name = user.get("name", "Unknown")
        uname = user.get("username", "")
        prof = f"https://unsplash.com/@{uname}?utm_source=studyedge_blog&utm_medium=referral"
        out.append({
            "source": "Unsplash",
            "id": p.get("id"),
            "url": p.get("urls", {}).get("regular"),
            "preview": p.get("urls", {}).get("small"),
            "width": p.get("width"),
            "height": p.get("height"),
            "avg_color": p.get("color"),
            "alt": p.get("alt_description") or p.get("description") or "",
            "photographer": name,
            "photographer_url": prof,
            "photo_page": p.get("links", {}).get("html", ""),
            "attribution_text": f"Photo by {name} on Unsplash",
            "attribution_html": (
                f'Photo by <a href="{prof}">{name}</a> '
                f'on <a href="https://unsplash.com/?utm_source=studyedge_blog&utm_medium=referral">Unsplash</a>'
            ),
            # Hit this when the image is actually used, per Unsplash API terms.
            "track_download": p.get("links", {}).get("download_location"),
        })
    return out


def track_download(download_location):
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        print(json.dumps({"tracked": False, "reason": "no UNSPLASH_ACCESS_KEY"}))
        return
    try:
        _get(download_location, {"Authorization": f"Client-ID {key}"})
        print(json.dumps({"tracked": True}))
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"tracked": False, "reason": str(e)}))


def run_query(query, source, limit, orientation):
    results = []
    if source in ("both", "pexels"):
        results += search_pexels(query, limit, orientation)
    if source in ("both", "unsplash"):
        results += search_unsplash(query, limit, orientation)
    return {"query": query, "count": len(results), "results": results}


def main():
    ap = argparse.ArgumentParser(description="Fetch real stock photos for blog posts.")
    ap.add_argument("--query", help="single search query")
    ap.add_argument("--batch", nargs="+", help="multiple queries in one run")
    ap.add_argument("--source", default="both", choices=["both", "pexels", "unsplash"])
    ap.add_argument("--orientation", default="landscape",
                    choices=["landscape", "portrait", "square"])
    ap.add_argument("--limit", type=int, default=6)
    ap.add_argument("--track", help="Unsplash download_location url to record a use")
    args = ap.parse_args()

    if args.track:
        track_download(args.track)
        return

    if not os.environ.get("PEXELS_API_KEY") and not os.environ.get("UNSPLASH_ACCESS_KEY"):
        print(json.dumps({
            "error": "No API key found. Set PEXELS_API_KEY and/or UNSPLASH_ACCESS_KEY. Both are free."
        }))
        sys.exit(1)

    queries = args.batch if args.batch else ([args.query] if args.query else [])
    if not queries:
        print(json.dumps({"error": "Provide --query or --batch."}))
        sys.exit(1)

    payload = [run_query(q, args.source, args.limit, args.orientation) for q in queries]
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
