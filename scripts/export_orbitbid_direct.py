#!/usr/bin/env python3
"""Run the OrbitBid exporter with direct public catalog API discovery."""

from __future__ import annotations

import export_orbitbid as base
from orbitbid_catalog import discover_lot_ids


def direct_discover(session, auction_id: str):
    return discover_lot_ids(
        session,
        auction_id,
        graphql_url=base.GRAPHQL_URL,
        client_token=base.CLIENT_TOKEN,
        catalog_url=base.CATALOG_URL,
        page_size=base.PAGE_SIZE,
        max_pages=base.MAX_PAGES,
    )


def main() -> int:
    base.discover_lot_ids = direct_discover
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
