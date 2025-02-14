import sys
from urllib.parse import quote

import cloudscraper
import requests


class ScrapeClient:
    def __init__(self, delay: int = 30):
        self._client = cloudscraper.create_scraper(delay=delay, debug=False)

    def get(self, url: str) -> str:
        try:
            response = requests.get(quote(url, safe='/:&=?%#'))
            #response = self._client.get(quote(url, safe='/:&=?%#'))
            response.raise_for_status()

            return response.text
        except Exception as err:
            print(f"Ошибка при получении страницы: {err}")
            sys.exit(1)