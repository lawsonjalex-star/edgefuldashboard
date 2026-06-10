import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.edgeful.com"


class EdgefulClient:
    """Client for the Edgeful trading probability API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("EDGEFUL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Set EDGEFUL_API_KEY in .env or pass api_key=..."
            )
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

    def _get(self, path: str, params: dict = None) -> dict:
        url = f"{BASE_URL}{path}"
        response = self.session.get(url, params=params)
        if response.status_code == 401:
            raise PermissionError("Invalid or missing API key (401).")
        if response.status_code == 403:
            data = response.json()
            raise PermissionError(
                f"Access denied (403): {data.get('code', 'forbidden')} — "
                "this report may require a higher subscription tier."
            )
        if response.status_code == 429:
            raise RuntimeError("Rate limit exceeded (429). Default limit: 30 req/60s.")
        response.raise_for_status()
        return response.json()

    # ── Report endpoints ──────────────────────────────────────────────────────

    def report(
        self,
        report_slug: str,
        market_type: str,
        ticker: str,
        start_date: str,
        end_date: str,
        **kwargs,
    ) -> dict:
        """Call any /report_calculation endpoint by slug.

        Args:
            report_slug: e.g. "adr-average-daily-range-by-weekday"
            market_type: "futures" | "forex" | "crypto" | "stock"
            ticker:      e.g. "ES", "NQ", "EURUSD"
            start_date:  "YYYY-MM-DD"
            end_date:    "YYYY-MM-DD"
            **kwargs:    Extra query params (period, timezone, days_to_use, etc.)
        """
        path = f"/report_calculation/{report_slug}/{market_type}/{ticker}"
        params = {"start_date": start_date, "end_date": end_date, **kwargs}
        return self._get(path, params)

    def intraday(
        self,
        report_slug: str,
        market_type: str,
        ticker: str,
        start_date: str,
        end_date: str,
        start_time: str = None,
        end_time: str = None,
        timezone: str = "America/New_York",
        **kwargs,
    ) -> dict:
        """Call any /intraday_calculation endpoint by slug.

        Args:
            report_slug: e.g. "opening-range-breakout-standard"
            market_type: "futures" | "forex" | "crypto" | "stock"
            ticker:      e.g. "ES"
            start_date:  "YYYY-MM-DD"
            end_date:    "YYYY-MM-DD"
            start_time:  "HH:MM:SS" session open
            end_time:    "HH:MM:SS" session close
            timezone:    IANA timezone string
        """
        path = f"/intraday_calculation/{report_slug}/{market_type}/{ticker}"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "timezone": timezone,
            **kwargs,
        }
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        return self._get(path, params)

    def screener(self, ticker: str, market_type: str = "futures") -> dict:
        """Fetch the historic data screener snapshot for a ticker."""
        path = f"/screener/{market_type}/{ticker}"
        return self._get(path)
