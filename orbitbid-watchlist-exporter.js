(() => {
  "use strict";

  const HOST = "bid.orbitbid.com";
  const SCHEMA = "orbitbid-watchlist-v1";
  const MAX_SCROLL_ROUNDS = 80;
  const STABLE_ROUNDS = 6;
  const SCROLL_DELAY_MS = 450;

  if (location.hostname !== HOST) {
    throw new Error(`Run this only on https://${HOST}/ while signed in to your OrbitBid account.`);
  }

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function lotIdsFromDocument(doc = document) {
    const ids = new Set();
    for (const link of doc.querySelectorAll('a[href*="/lot/"]')) {
      const href = link.getAttribute("href") || "";
      const match = href.match(/\/lot\/(\d+)(?:\/|$|[?#])/);
      if (match) ids.add(Number(match[1]));
    }
    return ids;
  }

  async function loadLazyContent() {
    let previousCount = -1;
    let stable = 0;

    for (let round = 0; round < MAX_SCROLL_ROUNDS && stable < STABLE_ROUNDS; round += 1) {
      window.scrollTo({ top: document.documentElement.scrollHeight, behavior: "instant" });
      await sleep(SCROLL_DELAY_MS);

      const count = lotIdsFromDocument().size;
      if (count === previousCount) {
        stable += 1;
      } else {
        stable = 0;
        previousCount = count;
      }
    }

    window.scrollTo({ top: 0, behavior: "instant" });
  }

  function paginationLinks() {
    const urls = new Set();
    const here = new URL(location.href);

    for (const link of document.querySelectorAll("a[href]")) {
      const text = (link.textContent || "").trim().toLowerCase();
      const aria = (link.getAttribute("aria-label") || "").trim().toLowerCase();
      let url;
      try {
        url = new URL(link.href, location.href);
      } catch {
        continue;
      }

      if (url.origin !== here.origin || url.pathname !== here.pathname || url.href === here.href) continue;

      const looksLikePage =
        /^\d+$/.test(text) ||
        text === "next" ||
        text === "previous" ||
        text === "prev" ||
        aria.includes("next") ||
        aria.includes("previous") ||
        url.searchParams.has("page");

      if (looksLikePage) urls.add(url.href);
    }

    return [...urls];
  }

  async function collectIdsFromPagination(ids) {
    const queue = paginationLinks();
    const visited = new Set([location.href]);

    while (queue.length) {
      const url = queue.shift();
      if (!url || visited.has(url)) continue;
      visited.add(url);

      try {
        const response = await fetch(url, {
          credentials: "include",
          cache: "no-store",
          headers: { accept: "text/html" },
        });
        if (!response.ok) continue;

        const html = await response.text();
        const doc = new DOMParser().parseFromString(html, "text/html");
        for (const id of lotIdsFromDocument(doc)) ids.add(id);

        for (const link of doc.querySelectorAll("a[href]")) {
          let next;
          try {
            next = new URL(link.getAttribute("href") || "", url);
          } catch {
            continue;
          }
          const text = (link.textContent || "").trim().toLowerCase();
          const aria = (link.getAttribute("aria-label") || "").trim().toLowerCase();
          if (
            next.origin === location.origin &&
            next.pathname === location.pathname &&
            !visited.has(next.href) &&
            (/^\d+$/.test(text) || text === "next" || aria.includes("next") || next.searchParams.has("page"))
          ) {
            queue.push(next.href);
          }
        }
      } catch (error) {
        console.warn("Watch-list pagination fetch skipped:", url, error);
      }
    }
  }

  function showPanel(payload, json) {
    document.getElementById("orbitbid-watchlist-export-panel")?.remove();

    const panel = document.createElement("div");
    panel.id = "orbitbid-watchlist-export-panel";
    Object.assign(panel.style, {
      position: "fixed",
      right: "20px",
      bottom: "20px",
      zIndex: "2147483647",
      maxWidth: "430px",
      padding: "16px",
      border: "2px solid #222",
      borderRadius: "10px",
      background: "#fff",
      color: "#111",
      boxShadow: "0 4px 18px rgba(0,0,0,.25)",
      font: "14px/1.45 Arial,sans-serif",
    });

    const heading = document.createElement("div");
    heading.textContent = `OrbitBid Watch List export: ${payload.lot_ids.length} lot IDs`;
    heading.style.fontWeight = "700";
    heading.style.marginBottom = "8px";

    const note = document.createElement("div");
    note.textContent =
      "Only lot IDs are included. No cookies, login tokens, bidder identity, max bids, auto bids, or page text are exported.";
    note.style.marginBottom = "10px";

    const copy = document.createElement("button");
    copy.textContent = "Copy JSON for GitHub Action";
    copy.style.marginRight = "8px";
    copy.onclick = async () => {
      await navigator.clipboard.writeText(json);
      copy.textContent = "Copied";
    };

    const download = document.createElement("button");
    download.textContent = "Download JSON";
    download.onclick = () => {
      const blob = new Blob([json + "\n"], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "orbitbid-watchlist.json";
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
    };

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
    close.onclick = () => panel.remove();

    panel.append(heading, note, copy, download, close);
    document.body.appendChild(panel);
  }

  (async () => {
    console.log("OrbitBid Watch List: loading lazy-rendered items...");
    await loadLazyContent();

    const ids = lotIdsFromDocument();
    await collectIdsFromPagination(ids);

    const lotIds = [...ids].filter(Number.isInteger).sort((a, b) => a - b);
    if (!lotIds.length) {
      throw new Error(
        "No OrbitBid lot links were found. Open your authenticated Watch List, wait for it to render, then run this exporter again."
      );
    }

    const payload = {
      schema: SCHEMA,
      captured_at: new Date().toISOString(),
      source_host: HOST,
      lot_ids: lotIds,
    };
    const json = JSON.stringify(payload);

    try {
      await navigator.clipboard.writeText(json);
      console.log("OrbitBid Watch List JSON copied to clipboard.");
    } catch {
      console.log("Clipboard permission was unavailable; use the on-page Copy button.");
    }

    showPanel(payload, json);
    console.log("OrbitBid Watch List export ready.", payload);
  })();
})();