(() => {
  const params = new URLSearchParams(location.search);
  const CONFIG = {
    auctionId: Number(params.get("auction_id")),
    pageSize: 60,
    maxPages: 100,
    requestDelayMs: 250
  };

  if (!Number.isInteger(CONFIG.auctionId) || CONFIG.auctionId <= 0) {
    throw new Error("Open an OrbitBid auction catalog URL containing ?auction_id=... before running the exporter.");
  }

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

  function showDownloadButton(name, blob) {
    const old = document.getElementById("auction-export-download-panel");
    if (old) old.remove();

    const url = URL.createObjectURL(blob);
    const panel = document.createElement("div");
    panel.id = "auction-export-download-panel";
    Object.assign(panel.style, {
      position: "fixed",
      right: "24px",
      bottom: "24px",
      zIndex: "2147483647",
      background: "#ffffff",
      color: "#111111",
      border: "2px solid #222222",
      borderRadius: "10px",
      padding: "16px",
      boxShadow: "0 4px 18px rgba(0,0,0,.28)",
      font: "14px/1.4 Arial, sans-serif",
      maxWidth: "360px",
    });

    const title = document.createElement("div");
    title.textContent = "Auction export ready";
    Object.assign(title.style, { fontWeight: "700", marginBottom: "8px" });

    const note = document.createElement("div");
    note.textContent = name;
    Object.assign(note.style, { marginBottom: "12px", wordBreak: "break-all" });

    const link = document.createElement("a");
    link.href = url;
    link.download = name;
    link.textContent = "Download export ZIP";
    Object.assign(link.style, {
      display: "inline-block",
      background: "#111111",
      color: "#ffffff",
      padding: "10px 14px",
      borderRadius: "6px",
      textDecoration: "none",
      fontWeight: "700",
      cursor: "pointer",
    });
    link.addEventListener("click", () => {
      link.textContent = "Download started";
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    }, { once: true });

    const close = document.createElement("button");
    close.textContent = "×";
    close.title = "Close";
    Object.assign(close.style, {
      position: "absolute",
      top: "4px",
      right: "8px",
      border: "0",
      background: "transparent",
      fontSize: "22px",
      cursor: "pointer",
    });
    close.addEventListener("click", () => {
      URL.revokeObjectURL(url);
      panel.remove();
    });

    panel.append(title, note, link, close);
    document.body.appendChild(panel);
    panel.scrollIntoView({ block: "nearest" });
    return panel;
  }

  const CRC32_TABLE = (() => {
    const table = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) {
        c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      }
      table[n] = c >>> 0;
    }
    return table;
  })();

  function crc32(bytes) {
    let crc = 0xFFFFFFFF;
    for (const b of bytes) crc = CRC32_TABLE[(crc ^ b) & 0xFF] ^ (crc >>> 8);
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }

  function u16(value) {
    return new Uint8Array([value & 0xFF, (value >>> 8) & 0xFF]);
  }

  function u32(value) {
    return new Uint8Array([
      value & 0xFF,
      (value >>> 8) & 0xFF,
      (value >>> 16) & 0xFF,
      (value >>> 24) & 0xFF,
    ]);
  }

  function concatBytes(parts) {
    const total = parts.reduce((sum, part) => sum + part.length, 0);
    const out = new Uint8Array(total);
    let offset = 0;
    for (const part of parts) {
      out.set(part, offset);
      offset += part.length;
    }
    return out;
  }

  function makeZip(files) {
    const encoder = new TextEncoder();
    const localParts = [];
    const centralParts = [];
    let offset = 0;

    for (const file of files) {
      const nameBytes = encoder.encode(file.name);
      const dataBytes = encoder.encode(file.content);
      const crc = crc32(dataBytes);
      const size = dataBytes.length;

      const localHeader = concatBytes([
        u32(0x04034B50), u16(20), u16(0x0800), u16(0), u16(0), u16(0),
        u32(crc), u32(size), u32(size), u16(nameBytes.length), u16(0), nameBytes,
      ]);
      localParts.push(localHeader, dataBytes);

      const centralHeader = concatBytes([
        u32(0x02014B50), u16(20), u16(20), u16(0x0800), u16(0), u16(0), u16(0),
        u32(crc), u32(size), u32(size), u16(nameBytes.length), u16(0), u16(0),
        u16(0), u16(0), u32(0), u32(offset), nameBytes,
      ]);
      centralParts.push(centralHeader);
      offset += localHeader.length + dataBytes.length;
    }

    const centralDirectory = concatBytes(centralParts);
    const endRecord = concatBytes([
      u32(0x06054B50), u16(0), u16(0), u16(files.length), u16(files.length),
      u32(centralDirectory.length), u32(offset), u16(0),
    ]);

    return new Blob([...localParts, centralDirectory, endRecord], { type: "application/zip" });
  }

  function lotIdsFromDocument(doc) {
    const ids = [];
    const seen = new Set();

    for (const a of doc.querySelectorAll('a[href*="/lot/"]')) {
      const href = a.getAttribute("href") || "";
      const match = href.match(/\\/lot\\/(\\d+)(?:\\/|$)/);
      if (!match) continue;
      const id = Number(match[1]);
      if (!Number.isInteger(id) || seen.has(id)) continue;
      seen.add(id);
      ids.push(id);
    }
    return ids;
  }

  async function discoverLotIds() {
    const all = [];
    const seen = new Set();

    for (let page = 1; page <= CONFIG.maxPages; page++) {
      const url = new URL(location.origin + "/");
      url.searchParams.set("items", "all");
      url.searchParams.set("auction_id", String(CONFIG.auctionId));
      url.searchParams.set("display", "grid");
      url.searchParams.set("limit", String(CONFIG.pageSize));
      url.searchParams.set("page", String(page));

      const r = await fetch(url, { credentials: "same-origin" });
      if (!r.ok) throw new Error(`Catalog page ${page} failed: HTTP ${r.status}`);

      const html = await r.text();
      const doc = new DOMParser().parseFromString(html, "text/html");
      const pageIds = lotIdsFromDocument(doc);
      const fresh = pageIds.filter(id => !seen.has(id));

      for (const id of fresh) {
        seen.add(id);
        all.push(id);
      }

      console.log(`Catalog page ${page}: ${pageIds.length} lot links, ${fresh.length} new`);

      if (fresh.length === 0) break;
      if (pageIds.length < CONFIG.pageSize) break;
      await sleep(150);
    }

    if (!all.length) {
      const fallback = lotIdsFromDocument(document);
      for (const id of fallback) {
        if (!seen.has(id)) {
          seen.add(id);
          all.push(id);
        }
      }
    }

    if (!all.length) {
      throw new Error("No OrbitBid lot links were discovered in this auction catalog.");
    }

    return all;
  }

  async function fetchLot(internalId) {
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

    const requestedLotNumber = String(lot.item_number || internalId).replace(/^1-/, "");

    return {
      requested_lot_number: requestedLotNumber,
      internal_id: internalId,
      ...lot,
      photo_count: lot.images?.length ?? 0
    };
  }

  (async () => {
    const lots = [];
    const errors = [];

    console.log(`OrbitBid ${CONFIG.auctionId}: discovering catalog lots...`);
    const lotIds = await discoverLotIds();
    console.log(`OrbitBid ${CONFIG.auctionId}: discovered ${lotIds.length} unique lot IDs. Retrieving lot details...`);

    for (let i = 0; i < lotIds.length; i++) {
      const internalId = lotIds[i];
      try {
        const lot = await fetchLot(internalId);
        lots.push(lot);
        console.log(
          `✓ ${lot.requested_lot_number} | ID ${internalId} | $${lot.amount ?? "?"} | ${lot.bid_count ?? "?"} bids | ${lot.photo_count} photos`
        );
      } catch (e) {
        errors.push({ internalId, error: String(e) });
        console.warn(`✗ ID ${internalId}`, e);
      }

      await sleep(CONFIG.requestDelayMs);
      if ((i + 1) % 15 === 0) await sleep(1500);
    }

    const retrievedAt = new Date().toISOString();
    const data = {
      auction_id: CONFIG.auctionId,
      source_url: location.href,
      retrieved_at: retrievedAt,
      total_discovered: lotIds.length,
      total_retrieved: lots.length,
      total_errors: errors.length,
      lots,
      errors
    };

    let summary = `# OrbitBid Auction ${CONFIG.auctionId}\n\n`;
    summary += `- Retrieved: ${retrievedAt}\n`;
    summary += `- Source: ${location.href}\n`;
    summary += `- Catalog lots discovered: ${lotIds.length}\n`;
    summary += `- Lots retrieved: ${lots.length}\n`;
    summary += `- Errors: ${errors.length}\n\n`;

    for (const lot of lots) {
      summary += `---\n\n## Lot ${lot.requested_lot_number} — ${md(lot.title)}\n\n`;
      summary += `- OrbitBid item number: ${md(lot.item_number)}\n`;
      summary += `- Internal ID: ${lot.internal_id}\n`;
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
      "lot","item_number","internal_id","current_bid","bid_count","photo_count","status","live_status","end_time","title"
    ].map(csv).join(",")];

    for (const lot of lots) {
      rows.push([
        lot.requested_lot_number, lot.item_number, lot.internal_id, lot.amount, lot.bid_count,
        lot.photo_count, lot.status, lot.live_status, lot.end_time, clean(lot.title)
      ].map(csv).join(","));
    }

    const lotsJson = JSON.stringify(data, null, 2);
    const summaryCsv = rows.join("\r\n");
    const zipName = `orbitbid-${CONFIG.auctionId}-export.zip`;
    const zip = makeZip([
      { name: "summary.md", content: summary },
      { name: "lots.json", content: lotsJson },
      { name: "summary.csv", content: summaryCsv },
    ]);

    showDownloadButton(zipName, zip);

    console.log(
      `READY — ${lots.length} lots retrieved, ${errors.length} errors. Click the on-page Download export ZIP button for ${zipName}.`
    );
  })();
})();