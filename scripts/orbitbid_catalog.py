"""Direct OrbitBid public catalog discovery.

Uses the same searchPublicItems GraphQL operation as OrbitBid's public frontend.
"""

from __future__ import annotations

import json
import time
from typing import Any


SEARCH_ITEMS_QUERY = r"""
query searchPublicItems($search: SearchInput, $viewed: [Int]) {
  data: searchPublicItems(search: $search, viewed: $viewed) {
    rows: data {
      id
      item_number
      auction { id }
    }
    pagination {
      limit
      page
      pageCount
      totalCount
    }
  }
}
"""


def discover_lot_ids(
    session: Any,
    auction_id: str,
    *,
    graphql_url: str,
    client_token: str,
    catalog_url: str = "https://bid.orbitbid.com/",
    page_size: int = 60,
    max_pages: int = 200,
) -> tuple[list[int], list[str]]:
    requested_auction_id = int(auction_id)
    all_ids: list[int] = []
    seen: set[int] = set()
    page_urls: list[str] = []
    expected_total: int | None = None
    expected_page_count: int | None = None

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "x-client-host": "bid.orbitbid.com",
        "x-client-token": client_token,
        "x-operation-name": "searchPublicItems",
        "origin": "https://bid.orbitbid.com",
        "referer": "https://bid.orbitbid.com/",
    }

    for page in range(1, max_pages + 1):
        variables = {
            "search": {
                "pagination": {"limit": page_size, "page": page},
                "filters": {
                    "status": "current",
                    "items": "all",
                    "auction_id": [requested_auction_id],
                },
            },
            "viewed": [],
        }
        response = session.post(
            graphql_url,
            headers=headers,
            json={
                "operationName": "searchPublicItems",
                "variables": variables,
                "query": SEARCH_ITEMS_QUERY,
            },
            timeout=45,
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Catalog API page {page} failed: HTTP {response.status_code}"
            )

        payload = response.json()
        if payload.get("errors"):
            raise RuntimeError(
                "Catalog API returned GraphQL errors: "
                + json.dumps(payload["errors"], ensure_ascii=False)
            )

        data = (payload.get("data") or {}).get("data") or {}
        rows = data.get("rows") or []
        pagination = data.get("pagination") or {}

        if expected_total is None:
            expected_total = int(pagination.get("totalCount") or 0)
            expected_page_count = int(pagination.get("pageCount") or 0)
            if expected_total <= 0:
                raise RuntimeError(
                    "OrbitBid catalog API returned zero lots for this current auction."
                )
            if expected_page_count <= 0 or expected_page_count > max_pages:
                raise RuntimeError(
                    f"Unexpected OrbitBid catalog page count: {expected_page_count}"
                )

        page_ids: list[int] = []
        for row in rows:
            lot_id = row.get("id")
            row_auction_id = (row.get("auction") or {}).get("id")
            if row_auction_id != requested_auction_id:
                raise RuntimeError(
                    "Mixed-auction safety check failed during catalog discovery: "
                    f"lot {lot_id} belongs to auction {row_auction_id}, "
                    f"expected {requested_auction_id}."
                )
            if not isinstance(lot_id, int) or lot_id <= 0:
                raise RuntimeError(f"Invalid lot ID returned by catalog API: {lot_id!r}")
            page_ids.append(lot_id)

        fresh = [lot_id for lot_id in page_ids if lot_id not in seen]
        print(
            f"Catalog API page {page}: {len(page_ids)} lots, {len(fresh)} new "
            f"(total={expected_total}, pages={expected_page_count})"
        )

        if not page_ids:
            raise RuntimeError(
                f"Catalog API returned an empty page before completion at page {page}."
            )

        for lot_id in fresh:
            seen.add(lot_id)
            all_ids.append(lot_id)

        page_urls.append(
            f"{catalog_url}?items=all&auction_id={auction_id}"
            f"&display=grid&limit={page_size}&page={page}"
        )

        if page >= expected_page_count:
            break
        time.sleep(0.1)
    else:
        raise RuntimeError(
            f"Catalog API exceeded the safety maximum of {max_pages} pages."
        )

    if expected_total is None or len(all_ids) != expected_total:
        raise RuntimeError(
            "Incomplete catalog discovery: "
            f"expected {expected_total} unique lots, found {len(all_ids)}."
        )

    return all_ids, page_urls
