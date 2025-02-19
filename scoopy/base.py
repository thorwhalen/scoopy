"""Base functionality of scoopy"""

import os
from typing import Literal
from functools import lru_cache

from scoopy.data_sources import (
    newsdata_search,
    yahoo_finance_news_search,
    yahoo_finance_headlines,
)

NewSources = Literal['newsdata', 'yahoo_finance', 'yahoo_finance_headlines']
DFLT_NEWS_SOURCE = 'newsdata'


def search_news(query: str = '', source: NewSources = DFLT_NEWS_SOURCE, **kwargs):
    if source == 'yahoo_finance_headlines':
        assert not query, "Yahoo headlines does not take a query."
        return list(yahoo_finance_headlines())
    else:
        assert query, "Query must be provided for newsdata and yahoo_finance."

    if source == 'newsdata':
        # https://newsdata.io/documentation
        return newsdata_search(query, **kwargs)
    elif source == 'yahoo_finance':
        return yahoo_finance_news_search(query, **kwargs)
    else:
        raise ValueError(f"Unknown news source: {source}")
