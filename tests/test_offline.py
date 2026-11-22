"""Offline tests: every network or API-key dependency is replaced by a fake."""

import sys
import types

import pytest

from scoopy import base, data_sources, util


class _Resp:
    def __init__(self, status_code=200, text="", payload=None):
        self.status_code, self.text, self._payload = status_code, text, payload
        self.content = text.encode()

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_get_config(monkeypatch):
    monkeypatch.setenv("SCOOPY_X", "v")
    assert util.get_config("SCOOPY_X") == "v"
    monkeypatch.delenv("SCOOPY_X")
    with pytest.raises(ValueError, match="SCOOPY_X"):
        util.get_config("SCOOPY_X")


def test_app_dir_exists_and_djoin():
    import os

    assert os.path.isdir(util.app_data_dir)
    assert util.djoin("f").startswith(util.app_data_dir)


HTML = """
<a href="/1"><h3> First headline </h3></a>
<a href="/2"><h3>   </h3></a>
<a href="/3"><span>no h3</span></a>
<a href="/4"><h3>Second</h3></a>
"""


def test_yahoo_headlines_parse(monkeypatch):
    seen = {}

    def fake_get(url, headers=None, **kw):
        seen["headers"] = headers
        return _Resp(text=HTML)

    monkeypatch.setattr(data_sources.requests, "get", fake_get)
    assert list(data_sources.yahoo_finance_headlines()) == ["First headline", "Second"]
    assert seen["headers"] is data_sources.dflt_headers
    assert list(data_sources.headlines(headers={"X": "1"})) == [
        "First headline",
        "Second",
    ]


def test_yahoo_headlines_http_error(monkeypatch, capsys):
    monkeypatch.setattr(
        data_sources.requests, "get", lambda *a, **k: _Resp(status_code=503)
    )
    assert (
        list(data_sources.yahoo_finance_headlines()) == []
    )  # error path yields nothing
    assert "Error 503" in capsys.readouterr().out


def test_yahoo_news_search_params(monkeypatch):
    seen = {}

    def fake_get(url, params=None, headers=None):
        seen.update(url=url, params=params)
        return _Resp(payload={"news": []})

    monkeypatch.setattr(data_sources.requests, "get", fake_get)
    out = data_sources.yahoo_finance_news_search("aapl", newsCount=3, region="US")
    assert out == {"news": []}
    assert seen["params"] == {
        "q": "aapl",
        "quotesCount": 0,
        "newsCount": 3,
        "listsCount": 0,
        "region": "US",
    }


def test_yahoo_news_search_raises_on_error(monkeypatch):
    monkeypatch.setattr(
        data_sources.requests, "get", lambda *a, **k: _Resp(status_code=500)
    )
    with pytest.raises(RuntimeError):
        data_sources.yahoo_finance_news_search("x")


def _fake_newsdata(monkeypatch, response):
    class Client:
        def __init__(self, apikey):
            self.apikey = apikey

        def latest_api(self, query, **kw):
            return response

    mod = types.ModuleType("newsdataapi")
    mod.NewsDataApiClient = Client
    monkeypatch.setitem(sys.modules, "newsdataapi", mod)
    monkeypatch.setenv("NEWSDATA_API_KEY", "k")
    data_sources._newsdata_client.cache_clear()


def test_newsdata_search(monkeypatch):
    _fake_newsdata(monkeypatch, {"status": "success", "results": [{"title": "t"}]})
    assert data_sources.newsdata_search("q") == [{"title": "t"}]
    data_sources._newsdata_client.cache_clear()


def test_newsdata_search_bad_status(monkeypatch):
    _fake_newsdata(monkeypatch, {"status": "error"})
    with pytest.raises(ValueError, match="success"):
        data_sources.newsdata_search("q")
    data_sources._newsdata_client.cache_clear()


def test_yfinance_wrapper(monkeypatch):
    class Ticker:
        def __init__(self, sym, session=None):
            self.sym, self.session, self.news = sym, session, [{"n": sym}]

    mod = types.ModuleType("yfinance")
    mod.Ticker = Ticker
    monkeypatch.setitem(sys.modules, "yfinance", mod)
    assert data_sources.yahoo_finance_news_for_ticker("AAPL", timeout=3) == [
        {"n": "AAPL"}
    ]


def test_search_news_dispatch(monkeypatch):
    monkeypatch.setattr(base, "newsdata_search", lambda q, **k: ("nd", q, k))
    monkeypatch.setattr(base, "yahoo_finance_news_search", lambda q, **k: ("yf", q, k))
    monkeypatch.setattr(base, "yahoo_finance_headlines", lambda: iter(["h1", "h2"]))
    assert base.search_news("q", n=1) == ("nd", "q", {"n": 1})
    assert base.search_news("q", source="yahoo_finance") == ("yf", "q", {})
    assert base.search_news(source="yahoo_finance_headlines") == ["h1", "h2"]
    with pytest.raises(AssertionError):
        base.search_news(source="yahoo_finance_headlines", query="x")
    with pytest.raises(AssertionError):
        base.search_news("")
    with pytest.raises(ValueError, match="Unknown news source"):
        base.search_news("q", source="nope")
