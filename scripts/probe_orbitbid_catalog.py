#!/usr/bin/env python3
"""Temporary diagnostic: capture OrbitBid catalog GraphQL operations without network navigation."""

from __future__ import annotations

import json
import sys
from urllib.parse import urlencode

from curl_cffi import requests
from playwright.sync_api import sync_playwright

CATALOG_URL = "https://bid.orbitbid.com/"


def main() -> int:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        raise SystemExit("Usage: probe_orbitbid_catalog.py <auction_id>")

    auction_id = sys.argv[1]
    params = {
        "items": "all",
        "auction_id": auction_id,
        "display": "grid",
        "limit": "60",
        "page": "1",
    }
    url = CATALOG_URL + "?" + urlencode(params)

    session = requests.Session(impersonate="chrome")
    response = session.get(url, timeout=45)
    response.raise_for_status()
    html = response.text

    captured: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200})

        def handle_request(request):
            if "__graphql__" not in request.url:
                return
            data = request.post_data or ""
            try:
                payload = json.loads(data)
            except Exception:
                payload = {"raw": data[:3000]}
            record = {
                "url": request.url,
                "method": request.method,
                "operationName": payload.get("operationName") if isinstance(payload, dict) else None,
                "variables": payload.get("variables") if isinstance(payload, dict) else None,
                "query": payload.get("query") if isinstance(payload, dict) else None,
            }
            captured.append(record)
            print("GRAPHQL_CAPTURE " + json.dumps(record, ensure_ascii=False), flush=True)

        page.on("request", handle_request)

        def route_main(route):
            if route.request.resource_type == "document":
                route.fulfill(status=200, content_type="text/html", body=html)
            else:
                route.continue_()

        page.route("https://bid.orbitbid.com/**", route_main)
        page.goto(url, wait_until="commit", timeout=30000)
        page.wait_for_timeout(25000)

        print(f"CAPTURED_COUNT {len(captured)}", flush=True)
        print(f"PAGE_URL {page.url}", flush=True)
        print(f"LOT_LINK_COUNT {page.locator('a[href*=\"/lot/\"]').count()}", flush=True)
        browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
