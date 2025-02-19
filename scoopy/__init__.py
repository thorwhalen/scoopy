"""
Access to news data


Sentiment analysis for stock market data.

>>> from scoopy import headlines
>>> headlines()  # doctest: +SKIP
["Yaccarino shakes up X amid Musk's pressure on costs, FT says",
 'Coup-hit Niger was betting on a China-backed oil pipeline as a lifeline. Then the troubles began',
 'A Mexico City neighborhood keeps the iconic Volkswagen Beetle alive',
 ...
 "Here's the Average Social Security Benefit at Age 62 -- and Why It's Not the Best News for Retirees",
 'Analyst Report: Mitsubishi UFJ Financial Group, Inc.',
 'Forget NextEra Energy. Buy This Magnificent Dividend King Instead']

"""

from scoopy.data_sources import headlines, yahoo_finance_news_search
from scoopy.base import search_news
