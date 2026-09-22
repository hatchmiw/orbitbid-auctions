(() => {
  const CONFIG = {
    auctionId: 1970,
    firstLot: 9926,
    lastLot: 9985,
    idOffset: 1728322,
    excludedNote: "9900-9925 (conduit excluded intentionally)"
  };

  const endpoint = "https://oas3.oasbid.com/__graphql__";
  const clientToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwibmFtZSI6InB1YmxpYyIsImlhdCI6MTc5MDAwMjU0OH0.QAXWKPsNUMzLm-kGZh3V3UI_8Cn8Jzm2WqX02qZRcOY";

  const query = `
    query getPublicLot($id: Int!, $increment_view: Boolean) {
      lot: getPublicLot(id: $id, increment_view: $increment_view) {
        id item_number title subtitle description amount max_amount bid_count
        status live_status prebid_start_time start_time end_time offer_end_time
        has_reserve has_reserve_met
        premium { id name type amount cash_discount }
        expenses { id name type amount is_taxable }
        location {
          id display_name address1 address2 city zip_code
          state { id code }
        }
        images { id small_path large_path metadata }
        fields { id type label value other_value }
        terms { id stub name display_name value }
      }
    }
  `;

  const headers = {
    accept: "*/*",
    "content-type": "application/json",
    "x-client-host": "bid.orbitbid.com",
    "x-client-token": clientToken,
    "x-operation-name": "getPublicLot"
  };

  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const clean = v => String(v ?? "").replace(/\s+/g, " ").trim();
  const md = v => clean(v).replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const csv = v => '"' + String(v ?? "").replace(/"/g, '""') + '"';

  function download(name, content, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = Object.assign(document.createElement("a"), { href: url, download: name });
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 3000);
  }

  async function fetchLot(lotNumber) {
    const internalId = lotNumber + CONFIG.idOffset;
    const r = await fetch(endpoint, {
      method: "POST",
      mode: "cors",
      credentials: "omit",
      headers,
      body: JSON.stringify({
        operationName: "getPublicLot",
        variables: { id: internalId, increment_view: false },
        query
      })
    });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const j = await r.json();
    if (j.errors?.length) throw new Error(JSON.stringify(j.errors));
    const lot = j?.data?.lot;
    if (!lot) throw new Error("No lot returned");
    if (!String(lot.item_number || "").endsWith(String(lotNumber))) {
      throw new Error(`ID mismatch: got ${lot.item_number}`);
    }
    return {
      requested_lot_number: lotNumber,
      internal_id: internalId,
      ...lot,
      photo_count: lot.images?.length ?? 0
    };
  }

  (async () => {
    const lots = [];
    const errors = [];

    console.log(`OrbitBid ${CONFIG.auctionId}: retrieving lots ${CONFIG.firstLot}-${CONFIG.lastLot}...`);

    for (let n = CONFIG.firstLot; n <= CONFIG.lastLot; n++) {
      try {
        const lot = await fetchLot(n);
        lots.push(lot);
        console.log(`✓ ${n} | $${lot.amount ?? "?"} | ${lot.bid_count ?? "?"} bids | ${lot.photo_count} photos`);
      } catch (e) {
        errors.push({ lotNumber: n, internalId: n + CONFIG.idOffset, error: String(e) });
        console.warn(`✗ ${n}`, e);
      }
      await sleep(350);
      if ((n - CONFIG.firstLot + 1) % 15 === 0) await sleep(2000);
    }

    const retrievedAt = new Date().toISOString();
    const data = {
      auction_id: CONFIG.auctionId,
      retrieved_at: retrievedAt,
      lot_range: `${CONFIG.firstLot}-${CONFIG.lastLot}`,
      excluded_lots: CONFIG.excludedNote,
      total_requested: CONFIG.lastLot - CONFIG.firstLot + 1,
      total_retrieved: lots.length,
      total_errors: errors.length,
      lots,
      errors
    };

    let summary = `# OrbitBid Auction ${CONFIG.auctionId}\n\n`;
    summary += `- Retrieved: ${retrievedAt}\n`;
    summary += `- Included lots: ${CONFIG.firstLot}-${CONFIG.lastLot}\n`;
    summary += `- Excluded: ${CONFIG.excludedNote}\n`;
    summary += `- Lots retrieved: ${lots.length}\n`;
    summary += `- Errors: ${errors.length}\n\n`;

    for (const lot of lots) {
      summary += `---\n\n## Lot ${lot.requested_lot_number} — ${md(lot.title)}\n\n`;
      summary += `- Current bid: $${lot.amount ?? ""}\n`;
      summary += `- Bid count: ${lot.bid_count ?? ""}\n`;
      summary += `- Photo count: ${lot.photo_count}\n`;
      summary += `- End time: ${lot.end_time ?? ""}\n\n`;

      if (clean(lot.description)) summary += `**Description:** ${md(lot.description)}\n\n`;

      if (lot.fields?.length) {
        summary += "**Fields:**\n\n";
        for (const f of lot.fields) {
          const value = clean(f.value || f.other_value);
          if (f.label || value) summary += `- ${md(f.label)}: ${md(value)}\n`;
        }
        summary += "\n";
      }

      if (lot.images?.length) {
        summary += "**Photos:**\n\n";
        lot.images.forEach((img, i) => {
          summary += `- [Photo ${i + 1}](${img.large_path})\n`;
        });
        summary += "\n";
      }
    }

    const rows = [[
      "lot","internal_id","current_bid","bid_count","photo_count","status","live_status","end_time","title"
    ].map(csv).join(",")];

    for (const lot of lots) {
      rows.push([
        lot.requested_lot_number, lot.internal_id, lot.amount, lot.bid_count,
        lot.photo_count, lot.status, lot.live_status, lot.end_time, clean(lot.title)
      ].map(csv).join(","));
    }

    const base = `orbitbid-${CONFIG.auctionId}`;
    download(base + "-summary.md", summary, "text/markdown;charset=utf-8");
    download(base + "-lots.json", JSON.stringify(data, null, 2), "application/json;charset=utf-8");
    download(base + "-summary.csv", rows.join("\r\n"), "text/csv;charset=utf-8");

    console.log(`DONE — ${lots.length} lots retrieved, ${errors.length} errors.`);
  })();
})();