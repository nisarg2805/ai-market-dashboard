import plotly.graph_objects as go

def price_chart(df, title: str):
    x = df["Date"]
    y = df["Close"]

    # force 1-D
    if hasattr(x, "values"): x = x.values
    if hasattr(y, "values"): y = y.values

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Close"))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Price")
    return fig


def ma_chart(df, title: str, short=50, long=200):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df[f"MA{short}"], mode="lines", name=f"MA{short}"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df[f"MA{long}"], mode="lines", name=f"MA{long}"))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="Price")
    return fig

def rsi_chart(df, title: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["RSI"], mode="lines", name="RSI"))
    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="RSI")
    return fig
