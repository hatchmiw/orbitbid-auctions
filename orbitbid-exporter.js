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