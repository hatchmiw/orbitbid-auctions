#!/usr/bin/env python3
"""Run the OrbitBid exporter using a rendered Chromium catalog.

This wraps export_orbitbid.py and replaces only its catalog-discovery function.
It prevents raw app-shell HTML from contributing unrelated lot links.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

import export_orbitbid as base

MAX_PAGES = 200
PAGE_SIZE = 60
MAX_CLOSE_SPAN_SECONDS = 2 * 24 * 60 * 60


def page_url(auction_id: str, page_number: int) -> str:
    params = {
        "auction_id": auction_id,
        "items": "all",
        "display": "grid",
        "limit": str(PAGE_SIZE),
        "page": str(page_number),
    }
    return "https://bid.orbitbid.com/?" + urlencode(params)


def ids_from_hrefs(hrefs: list[str]) -> list[int]:
    result = []
    seen = set()
    for href in hrefs:
        match = re.search(r"/lot/(\d+)(?:/|$|[?#])", href or "")
        if not match:
            continue
        lot_id = int(match.group(1))
        if lot_id not in seen:
            seen.add(lot_id)
            result.append(lot_id)
    return result


def rendered_discover(_session, auction_id: str):
    page_sets = []
    urls = []
    seen_any = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1200})
        try:
            for page_number in range(1, MAX_PAGES + 1):
                url = page_url(auction_id, page_number)
                print(f"Rendered catalog page {page_number}: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                try:
                    page.wait_for_selector('a[href*="/lot/"]', timeout=30000)
                except PlaywrightTimeoutError:
                    if page_number == 1:
                        raise RuntimeError("No rendered OrbitBid lot links found.")
                    break

                page.wait_for_timeout(1800)
                locator = page.locator('main a[href*="/lot/"]:visible')
                if locator.count() == 0:
                    locator = page.locator('a[href*="/lot/"]:visible')
                hrefs = locator.evaluate_all("(els) => els.map(e => e.href)")
                ids = ids_from_hrefs(hrefs)
                if not ids:
                    break

                fresh = [lot_id for lot_id in ids if lot_id not in seen_any]
                print(f"Page {page_number}: {len(ids)} visible lot IDs, {len(fresh)} new")
                page_sets.append(ids)
                urls.append(url)

                if not fresh:
                    break
                seen_any.update(ids)
        finally:
            browser.close()

    if not page_sets:
        raise RuntimeError("No OrbitBid catalog pages yielded lot IDs.")

    occurrence = Counter()
    for ids in page_sets:
        occurrence.update(set(ids))

    ordered = []
    seen = set()
    for ids in page_sets:
        for lot_id in ids:
            if lot_id not in seen:
                seen.add(lot_id)
                ordered.append(lot_id)

    if len(page_sets) > 1:
        filtered = [lot_id for lot_id in ordered if occurrence[lot_id] == 1]
        if filtered:
            print(f"Removed {len(ordered)-len(filtered)} links repeated across pages.")
            ordered = filtered

    if not ordered:
        raise RuntimeError("Rendered catalog filtering produced zero lot IDs.")
    return ordered, urls


def validate_written_export(auction_id: str):
    path = Path("auctions") / auction_id / "lots.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    closes = []
    for lot in data.get("lots", []):
        for key in ("end_time", "offer_end_time"):
            raw = lot.get(key)
            if raw in (None, "", 0, "0"):
                continue
            try:
                value = int(float(raw))
            except (TypeError, ValueError):
                continue
            if value > 10_000_000_000:
                value //= 1000
            closes.append(value)

    if closes and max(closes) - min(closes) > MAX_CLOSE_SPAN_SECONDS:
        span_days = (max(closes) - min(closes)) / 86400
        raise RuntimeError(
            f"Mixed-auction safety check failed: lot close times span {span_days:.1f} days. "
            "Nothing will be committed."
        )


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: export_orbitbid_rendered.py <auction_id>")
    auction_id = sys.argv[1].strip()
    base.discover_lot_ids = rendered_discover
    code = base.main()
    if code:
        raise SystemExit(code)
    validate_written_export(auction_id)


if __name__ == "__main__":
    main()
