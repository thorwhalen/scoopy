# scoopy.data_sources

Data sources.

### Functions

| [`headlines`](#scoopy.data_sources.headlines)([headers])                             | Get headlines from Yahoo Finance.                                                                           |
|---------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `newsdata_search`(query, \*[, \_egress])                                                          |                                                                                                             |
| [`yahoo_finance_headlines`](#scoopy.data_sources.yahoo_finance_headlines)([headers])               | Get headlines from Yahoo Finance.                                                                           |
| [`yahoo_finance_news_for_ticker`](#scoopy.data_sources.yahoo_finance_news_for_ticker)(ticker_symbol, \*) | Retrieve news for a specific ticker using yfinance, with optional control over the underlying HTTP request. |
| [`yahoo_finance_news_search`](#scoopy.data_sources.yahoo_finance_news_search)(query, \*[, ...])      | Search Yahoo Finance using the unofficial query endpoint.                                                   |

### scoopy.data_sources.headlines(headers=None)

Get headlines from Yahoo Finance.

### scoopy.data_sources.yahoo_finance_headlines(headers=None)

Get headlines from Yahoo Finance.

### scoopy.data_sources.yahoo_finance_news_for_ticker(ticker_symbol, , session=None, timeout=None)

Retrieve news for a specific ticker using yfinance, with optional control over the underlying HTTP request.

* **Parameters:**
  * **ticker_symbol** ([*str*](https://docs.python.org/3/builtins/stdtypes.html#str)) – The ticker symbol (e.g., “AAPL”) for which to retrieve news.
  * **session** (*requests.Session* *,* *optional*) – A custom requests session to use for making HTTP requests.
  * **timeout** ([*int*](https://docs.python.org/3/builtins/functions.html#int) *or* [*float*](https://docs.python.org/3/builtins/functions.html#float) *,* *optional*) – An optional timeout (in seconds) to use for the HTTP request.
* **Returns:**
  A list of news items (each a dictionary) as returned by Yahoo Finance.
* **Return type:**
  [*list*](https://docs.python.org/3/builtins/stdtypes.html#list)

#### NOTE
Currently, yfinance’s built-in `news` property does not support query filtering or additional parameters.
This function merely provides a thin wrapper around yf.Ticker(ticker_symbol).news, with the option to
control HTTP session and timeout settings.

### scoopy.data_sources.yahoo_finance_news_search(query, , quotesCount=0, newsCount=10, listsCount=0, headers=None, \*\*kwargs)

Search Yahoo Finance using the unofficial query endpoint.

* **Parameters:**
  * **query** ([*str*](https://docs.python.org/3/builtins/stdtypes.html#str)) – The search term to look for.
  * **quotesCount** ([*int*](https://docs.python.org/3/builtins/functions.html#int)) – Number of quote results to return (default: 0).
  * **newsCount** ([*int*](https://docs.python.org/3/builtins/functions.html#int)) – Number of news results to return (default: 10).
  * **listsCount** ([*int*](https://docs.python.org/3/builtins/functions.html#int)) – Number of list results to return (default: 0).
  * **headers** ([*dict*](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Optional HTTP headers for the request.
  * **\*\*kwargs** – Additional parameters to include in the request.
* **Returns:**
  The JSON response from the Yahoo Finance search API.
* **Return type:**
  [*dict*](https://docs.python.org/3/builtins/stdtypes.html#dict)
