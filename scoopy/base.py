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


@lru_cache
def _newsdata_client():
    from newsdataapi import NewsDataApiClient

    return NewsDataApiClient(apikey=_get_config('NEWSDATA_API_KEY'))


def _newsdata_search(query, *, _egress=lambda x: x['results'], **kwargs):
    # Initialize the client with your API key
    api = _newsdata_client()

    # Fetch news articles based on a query
    response = api.latest_api(**kwargs)

    if response['status'] != 'success':
        raise ValueError(f"Newsdata API did not return a 'success' status.")

    return _egress(response)
