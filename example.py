"""
Edgeful API – quickstart examples.
Make sure you have filled in your key in .env before running.
"""
from client import EdgefulClient

client = EdgefulClient()

# ── Example 1: Opening Range Breakout on ES futures ───────────────────────────
print("=== ORB Standard (ES, last 12 months) ===")
orb = client.intraday(
    report_slug="opening-range-breakout-standard",
    market_type="futures",
    ticker="ES",
    start_date="2025-06-01",
    end_date="2026-06-10",
    start_time="09:30:00",
    end_time="16:00:00",
    timezone="America/New_York",
)
print(orb)

# ── Example 2: ADR by weekday on NQ futures ───────────────────────────────────
print("\n=== ADR by Weekday (NQ) ===")
adr = client.report(
    report_slug="adr-average-daily-range-by-weekday",
    market_type="futures",
    ticker="NQ",
    start_date="2025-06-01",
    end_date="2026-06-10",
)
print(adr)

# ── Example 3: Screener snapshot ─────────────────────────────────────────────
print("\n=== Screener snapshot (ES) ===")
snap = client.screener(ticker="ES", market_type="futures")
print(snap)
