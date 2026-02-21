import streamlit as st


from src.parser import parse_query
from src.finance import (
    fetch_prices,
    total_return,
    annualized_volatility,
    moving_averages,
    correlation,
    add_rsi,
    ai_signal,
)
from src.charts import price_chart, ma_chart, rsi_chart
from src.report import build_pdf_report
# ----------------------------
# Watchlist state
# ----------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = ["AAPL", "TSLA", "MSFT"]

def add_to_watchlist(t):
    t = (t or "").strip().upper()
    if t and t not in st.session_state.watchlist:
        st.session_state.watchlist.append(t)

def remove_from_watchlist(t):
    if t in st.session_state.watchlist:
        st.session_state.watchlist.remove(t)

# ----------------------------
# Page setup (professional)
# ----------------------------
st.set_page_config(
    page_title="AI Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# Minimal header
st.markdown("## 📈 AI Market Dashboard")
st.caption("For analysis/education only (not financial advice).")

# ----------------------------
# Sidebar controls (pro feel)
# ----------------------------
with st.sidebar:
    st.markdown("### Watchlist")

    new_ticker = st.text_input("Add ticker", placeholder="e.g., NVDA", key="wl_add")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Add", use_container_width=True, key="wl_add_btn"):
            add_to_watchlist(new_ticker)
    with c2:
        if st.button("🧹 Clear", use_container_width=True, key="wl_clear_btn"):
            st.session_state.watchlist = ["AAPL", "TSLA", "MSFT"]

    watch_choice = st.selectbox(
        "Select from watchlist",
        st.session_state.watchlist,
        index=0,
        key="wl_select"
    )

    remove_choice = st.selectbox(
        "Remove ticker",
        ["(select)"] + st.session_state.watchlist,
        key="wl_remove_select"
    )
    if st.button("🗑 Remove selected", use_container_width=True, key="wl_remove_btn") and remove_choice != "(select)":
        remove_from_watchlist(remove_choice)

    st.markdown("---")
    st.markdown("### Defaults")
    default_ticker = st.text_input("Ticker (fallback)", value=watch_choice, key="fallback_ticker")
    default_period = st.selectbox(
        "Timeframe (fallback)",
        ["1mo", "3mo", "6mo", "1y", "2y"],
        index=1,
        key="fallback_period"
    )

    st.markdown("---")
    st.markdown("### Quick Commands")
    st.code("trend for TSLA 6 months")
    st.code("volatility of AAPL 1 year")
    st.code("moving average for SPY 1 year")
    st.code("RSI for NVDA 6 months")
    st.code("correlation AAPL and MSFT 6 months")

# ----------------------------
# Main input
# ----------------------------
colA, colB = st.columns([3, 1])
with colA:
    text = st.text_input(
        "Command",
        placeholder="Example: correlation AAPL and MSFT 6 months"
    )
with colB:
    run = st.button("Run", use_container_width=True)

# ----------------------------
# Helpers
# ----------------------------
def safe_pick_ticker(tickers: list[str]) -> str:
    # your earlier fix: pick last (most likely real)
    if tickers and isinstance(tickers, list):
        return tickers[-1]
    return default_ticker

def safe_pick_period(period: str) -> str:
    return period if period else default_period

# ----------------------------
# Run logic
# ----------------------------
if run and text:
    try:
        q = parse_query(text)
        intent = q.get("intent")
        tickers = q.get("tickers", [])
        period = safe_pick_period(q.get("period"))

        # Header row
        st.success(f"Command: {text}")
        st.write(f"**Intent:** {intent} | **Period:** {period} | **Tickers:** {tickers}")

        # ----------------------------
        # Correlation view
        # ----------------------------
        if intent == "CORRELATION" and len(tickers) >= 2:
            t1, t2 = tickers[0], tickers[-1]
            corr = correlation(t1, t2, period)

            m1, m2, m3 = st.columns(3)
            m1.metric("Ticker 1", t1)
            m2.metric("Ticker 2", t2)
            m3.metric("Correlation", f"{corr:.2f}")

            st.info("Tip: correlation near 1 = move together, near -1 = move opposite.")

        # ----------------------------
        # Single-ticker views
        # ----------------------------
        else:
            ticker = safe_pick_ticker(tickers)
            df = fetch_prices(ticker, period)

            if df is None or df.empty:
                st.error("No data downloaded. Try a valid ticker like AAPL, TSLA, MSFT, SPY and a timeframe like 6mo/1y.")
                st.stop()

            # Top metrics row (looks pro)
            r = total_return(df)
            v = annualized_volatility(df)

            signal, reason = ai_signal(df)

            # ----------------------------
            # PDF Export
            # ----------------------------
            report_lines = [
                f"Command: {text}",
                f"Ticker(s): {tickers}",
                f"Selected ticker: {ticker}",
                f"Period: {period}",
                f"Total Return: {r * 100:.2f}%",
                f"Annualized Volatility: {v * 100:.2f}%",
                f"AI Signal: {signal}",
                f"AI Reason: {reason}",
            ]

            pdf_bytes = build_pdf_report(
                title=f"AI Market Report — {ticker} ({period})",
                lines=report_lines
            )

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"{ticker}_{period}_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Ticker", ticker)
            k2.metric("Total Return", f"{r*100:.2f}%")
            k3.metric("Volatility", f"{v*100:.2f}%")
            k4.metric("AI Signal", signal)

            # Tabs for clean UI
            tab1, tab2, tab3 = st.tabs(["Price", "Indicators", "AI Summary"])

            with tab1:
                st.plotly_chart(price_chart(df, f"{ticker} Price ({period})"), use_container_width=True)

            with tab2:
                left, right = st.columns(2)

                with left:
                    # RSI chart
                    df_rsi = add_rsi(df)
                    rsi_value = float(df_rsi["RSI"].iloc[-1])
                    st.metric("RSI", f"{rsi_value:.1f}")
                    st.plotly_chart(rsi_chart(df_rsi, f"{ticker} RSI ({period})"), use_container_width=True)

                with right:
                    # Moving averages
                    df_ma = moving_averages(df, 50, 200)
                    st.plotly_chart(ma_chart(df_ma, f"{ticker} MA50 vs MA200 ({period})"), use_container_width=True)

            with tab3:
                st.subheader("🤖 AI Summary")
                st.write(f"**Signal:** {signal}")
                st.write(f"**Reason:** {reason}")

                st.markdown("#### What this means")
                st.write(
                    "- **BUY**: trend/indicator combination looks favorable\n"
                    "- **SELL**: indicators show overbought / weakness\n"
                    "- **HOLD**: mixed signals"
                )

            # Optional debug (hidden, professional)
            with st.expander("Debug (optional)"):
                st.write("Parsed:", q)
                st.dataframe(df.head(20))

    except Exception as e:
        st.error(f"Error: {e}")
