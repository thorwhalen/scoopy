"""Data sources."""

from functools import lru_cache

import requests
from scoopy.util import get_config


dflt_headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/110.0.0.0 Safari/537.36'
    )
}


# --------------------------------------------------------------------------------------
# Newsdata API


@lru_cache
def _newsdata_client():
    from newsdataapi import NewsDataApiClient

    return NewsDataApiClient(apikey=get_config('NEWSDATA_API_KEY'))


def newsdata_search(query, *, _egress=lambda x: x['results'], **kwargs):
    # Initialize the client with your API key
    api = _newsdata_client()

    # Fetch news articles based on a query
    response = api.latest_api(query, **kwargs)

    if response['status'] != 'success':
        raise ValueError(f"Newsdata API did not return a 'success' status.")

    return _egress(response)


# --------------------------------------------------------------------------------------
# Yahoo


def yahoo_finance_headlines(headers=None):
    """Get headlines from Yahoo Finance."""
    from bs4 import BeautifulSoup

    url = 'https://finance.yahoo.com/news/'
    response = requests.get(url, headers=headers or dflt_headers)
    if response.status_code != 200:
        print(
            f"Error {response.status_code}. "
            f"Failed to retrieve data: {response.content=}"
        )
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags that contain 'href' attribute and 'h3' tag inside them
    news_items = soup.find_all('a', href=True)

    for item in news_items:
        # Check if the 'a' tag contains an 'h3' tag with text
        headline_tag = item.find('h3')
        if headline_tag:
            headline = headline_tag.text.strip()
            if headline:
                yield headline


def yahoo_finance_news_search(
    query, *, quotesCount=0, newsCount=10, listsCount=0, headers=None, **kwargs
):
    """
    Search Yahoo Finance using the unofficial query endpoint.

    Parameters:
        query (str): The search term to look for.
        quotesCount (int): Number of quote results to return (default: 0).
        newsCount (int): Number of news results to return (default: 10).
        listsCount (int): Number of list results to return (default: 0).
        headers (dict): Optional HTTP headers for the request.
        **kwargs: Additional parameters to include in the request.

    Returns:
        dict: The JSON response from the Yahoo Finance search API.
    """
    headers = headers or dflt_headers
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": query,
        "quotesCount": quotesCount,
        "newsCount": newsCount,
        "listsCount": listsCount,
    }
    params.update(kwargs)

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()


# Note: This didn't work for me: Is the news endpoint deprecated?
def yahoo_finance_news_for_ticker(ticker_symbol, *, session=None, timeout=None):
    """
    Retrieve news for a specific ticker using yfinance, with optional control over the underlying HTTP request.

    Parameters:
        ticker_symbol (str): The ticker symbol (e.g., "AAPL") for which to retrieve news.
        session (requests.Session, optional): A custom requests session to use for making HTTP requests.
        timeout (int or float, optional): An optional timeout (in seconds) to use for the HTTP request.

    Returns:
        list: A list of news items (each a dictionary) as returned by Yahoo Finance.

    Note:
        Currently, yfinance's built-in `news` property does not support query filtering or additional parameters.
        This function merely provides a thin wrapper around yf.Ticker(ticker_symbol).news, with the option to
        control HTTP session and timeout settings.
    """
    import yfinance as yf

    # Create the ticker object, optionally with a custom session
    ticker = yf.Ticker(ticker_symbol, session=session)

    # If a timeout is provided, update the ticker's internal timeout (yfinance uses this when making requests)
    if timeout is not None:
        ticker._timeout = timeout

    # Simply return the news items as provided by yfinance; no post-processing is done here.
    return ticker.news


# --------------------------------------------------------------------------------------

# alias for forwards compatibility
# (might get our headlines from somewhere else (possibly multiple places) in the future)
headlines = yahoo_finance_headlines
