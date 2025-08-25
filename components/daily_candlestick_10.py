import streamlit as st
import plotly.graph_objects as go

def show_candlestick_with_neutral(df_filtered, start_date, end_date, period_label="Selected Period"):
    # 1. Filtrar período
    df_period = df_filtered.copy()
    df_period = df_period[(df_period["date"] >= start_date) & (df_period["date"] <= end_date)]

    if df_period.empty:
        st.warning("⚠️ No data available for the selected period.")
        return

    # 2. Agregar por dia (OHLC)
    df_daily = df_period.groupby("date").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    }).reset_index()

    # 3. Definir variação e classificar
    tolerance = 0.03  # 2% tolerance
    df_daily["variation"] = (df_daily["close"] - df_daily["open"]) / df_daily["open"]
    df_daily["type"] = df_daily["variation"].apply(
        lambda x: "neutral" if abs(x) <= tolerance else ("up" if x > 0 else "down")
    )

    # 4. Separar datasets
    df_up = df_daily[df_daily["type"] == "up"]
    df_down = df_daily[df_daily["type"] == "down"]
    df_neutral = df_daily[df_daily["type"] == "neutral"]

    # 5. Criar figura
    fig = go.Figure()

    # Alta (verde)
    if not df_up.empty:
        fig.add_trace(go.Candlestick(
            x=df_up["date"], open=df_up["open"], high=df_up["high"],
            low=df_up["low"], close=df_up["close"],
            increasing_line_color="green", decreasing_line_color="green",
            showlegend=False
        ))

    # Baixa (vermelho)
    if not df_down.empty:
        fig.add_trace(go.Candlestick(
            x=df_down["date"], open=df_down["open"], high=df_down["high"],
            low=df_down["low"], close=df_down["close"],
            increasing_line_color="red", decreasing_line_color="red",
            showlegend=False
        ))

    # Neutro (cinza)
    if not df_neutral.empty:
        fig.add_trace(go.Candlestick(
            x=df_neutral["date"], open=df_neutral["open"], high=df_neutral["high"],
            low=df_neutral["low"], close=df_neutral["close"],
            increasing_line_color="gray", decreasing_line_color="gray",
            showlegend=False
        ))

    fig.update_layout(
    title=dict(
        text=f"Price Candlestick – {period_label} ending on {end_date.strftime('%Y-%m-%d')}",
        font=dict(size=20)
    ),
    xaxis_title="Date",
    yaxis_title="Price ($ CAD)",
    xaxis_rangeslider_visible=False,
    height=500
)


    # 6. Exibir no Streamlit
    
    st.plotly_chart(fig, use_container_width=True)
