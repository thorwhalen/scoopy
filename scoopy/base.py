"""Base functionality of scoopy"""

import os
from typing import Literal
from functools import lru_cache

NewSources = Literal['newsdata']
DFLT_NEWS_SOURCE = 'newsdata'


def search_news(query: str, source: NewSources = DFLT_NEWS_SOURCE, **kwargs):
    if source == 'newsdata':
        return _newsdata_search(query, **kwargs)
        # https://newsdata.io/documentation
    raise ValueError(f"Unknown news source: {source}")


def _get_config(key):
    val = os.getenv(key)
    if val is None:
        raise ValueError(f"Missing environment variable: {key}")
    return val


# --------------------------------------------------------------------------------------
# Newsdata API


@lru_cache
def _newsdata_client():
    from newsdataapi import NewsDataApiClient

    return NewsDataApiClient(apikey=_get_config('NEWSDATA_API_KEY'))


_newsdata_search_default_params = {
    "qInTitle": None,  # Optional: Use if you want keywords in headlines only
    "category": "business, technology, politics",  # Focus on market-relevant categories
    "country": "us,gb,cn,jp,de",  # Major financial hubs
    "language": "en",
    # "timeframe": "24",  # Last 24 hours (Requires premium plan)
    # "prioritydomain": "newsdata.io"  # Optional: Prioritize high-quality sources
}


def _newsdata_search(query, *, _egress=lambda x: x['results'], **kwargs):
    # Initialize the client with your API key
    api = _newsdata_client()

    # Fetch news articles based on a query
    kwargs.update(_newsdata_search_default_params)
    response = api.latest_api(**kwargs)

    if response['status'] != 'success':
        raise ValueError(f"Newsdata API did not return a 'success' status.")

    return _egress(response)
