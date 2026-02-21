import re

DEFAULT_TICKER = "AAPL"
DEFAULT_PERIOD = "3mo"

NAME_TO_TICKER = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "nvidia": "NVDA",
    "meta": "META",
    "facebook": "META",
    "spy": "SPY",
    "qqq": "QQQ",
}

def normalize_period(text: str) -> str:
    t = text.lower()

    # direct yfinance formats like 3mo, 6mo, 1y
    m = re.search(r"\b(\d+)\s*(d|day|days|mo|month|months|y|year|years)\b", t)
    if m:
        num = int(m.group(1))
        unit = m.group(2)

        if unit in ["d", "day", "days"]:
            return f"{num}d"
        if unit in ["mo", "month", "months"]:
            # yfinance supports 1mo,3mo,6mo etc.
            if num in [1, 3, 6]:
                return f"{num}mo"
            if num == 12:
                return "1y"
            return "6mo"  # safe fallback
        if unit in ["y", "year", "years"]:
            if num in [1, 2, 5, 10]:
                return f"{num}y"
            return "1y"

    # phrases
    if "last 30 days" in t:
        return "1mo"
    if "last 7 days" in t:
        return "7d"
    if "last 3 months" in t:
        return "3mo"
    if "last 6 months" in t:
        return "6mo"
    if "last year" in t or "past year" in t:
        return "1y"

    return DEFAULT_PERIOD

def extract_tickers(text: str) -> list[str]:
    # tickers like AAPL, MSFT
    # find potential tickers
    tickers = re.findall(r"\b[A-Z]{1,5}\b", text.upper())

    # remove common English words mistakenly detected as tickers
    ignore_words = {
        "AND", "OR", "THE", "A", "AN", "TO", "FOR", "WITH", "SHOW", "LAST",
        "TREND", "PRICE", "BUY", "SELL", "NOW", "SHOULD", "ME", "MY", "YOU", "I"
    }
    tickers = [t for t in tickers if t not in ignore_words]

    tickers = list(dict.fromkeys(tickers))  # unique

    # map common company names to tickers
    t = text.lower()
    for name, ticker in NAME_TO_TICKER.items():
        if name in t and ticker not in tickers:
            tickers.append(ticker)

    if not tickers:
        tickers = [DEFAULT_TICKER]

    return tickers

def parse_query(text: str) -> dict:
    t = text.lower().strip()
    tickers = extract_tickers(text)
    period = normalize_period(text)

    # intents
    if ("correlation" in t or "compare" in t) and len(tickers) >= 2:
        intent = "CORRELATION"
    elif "volatility" in t or "risk" in t:
        intent = "VOLATILITY"
    elif "rsi" in t:
        intent = "RSI"
    elif "moving average" in t or "ma" in t:
        intent = "MOVING_AVG"
    elif "return" in t or "profit" in t or "performance" in t:
        intent = "RETURN"
    else:
        intent = "TREND"

    return {"intent": intent, "tickers": tickers, "period": period, "raw": text}
