import numpy as np
import pandas as pd
import yfinance as yf

def fetch_prices(ticker: str, period: str = "3mo") -> pd.DataFrame:
    ticker = ticker.strip().upper()

    df = yf.download(
        tickers=ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False
    )

    if df is None or df.empty:
        return pd.DataFrame()

    #  Force index -> Date column safely (no duplicate Date columns)
    df = df.copy()
    df.index = pd.to_datetime(df.index, errors="coerce")
    df = df.reset_index()
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)

    #  If yfinance ever returns multi-index columns, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    #  Keep only what we need and ensure types
    if "Close" not in df.columns:
        return pd.DataFrame()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df = df.dropna(subset=["Date", "Close"]).sort_values("Date")
    df["Return"] = df["Close"].pct_change()

    return df



def total_return(df: pd.DataFrame) -> float:
    return (df["Close"].iloc[-1] / df["Close"].iloc[0]) - 1

def annualized_volatility(df):
    if "Return" not in df.columns:
        df["Return"] = df["Close"].pct_change()

    r = df["Return"].dropna()
    if r.empty:
        return float("nan")

    return float(r.std() * np.sqrt(252))

def moving_averages(df: pd.DataFrame, short=50, long=200) -> pd.DataFrame:
    out = df.copy()
    out[f"MA{short}"] = out["Close"].rolling(short).mean()
    out[f"MA{long}"] = out["Close"].rolling(long).mean()
    return out

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    out = df.copy()
    delta = out["Close"].diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss
    out["RSI"] = 100 - (100 / (1 + rs))
    return out


def correlation(t1: str, t2: str, period: str) -> float:
    df1 = fetch_prices(t1, period)
    df2 = fetch_prices(t2, period)

    r1 = df1["Close"].pct_change().dropna()
    r2 = df2["Close"].pct_change().dropna()

    # ensure they are Series
    r1 = r1.squeeze()
    r2 = r2.squeeze()

    joined = (
        r1.rename("a")
        .to_frame()
        .join(r2.rename("b").to_frame(), how="inner")
    )

    return float(joined["a"].corr(joined["b"]))

def ai_signal(df):
    import numpy as np

    # moving averages
    df["MA50"] = df["Close"].rolling(50).mean()
    df["MA200"] = df["Close"].rolling(200).mean()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100/(1+rs))

    last = df.iloc[-1]

    signal = "HOLD"
    reason = []

    if last["MA50"] > last["MA200"]:
        reason.append("Trend bullish (MA50 > MA200)")
        signal = "BUY"

    if last["RSI"] > 70:
        reason.append("Overbought RSI")
        signal = "SELL"

    if last["RSI"] < 30:
        reason.append("Oversold RSI")
        signal = "BUY"

    return signal, ", ".join(reason)
