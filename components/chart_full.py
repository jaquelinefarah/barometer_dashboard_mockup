import streamlit as st
import altair as alt
import pandas as pd

def show_exchange_bar_chart(df, period_label):
    """
    Displays a simple bar chart showing the number of trades by exchange.
    """
    st.markdown("## 📊 Exchange Trade Count (Bar Chart)")

    # 1. Agrupar os dados
    exchange_counts = df["exchange"].value_counts().rename_axis("exchange").reset_index(name="num_trades")

    # 2. Gráfico de barras
    chart = alt.Chart(exchange_counts).mark_bar().encode(
        y=alt.Y("exchange:N", title="Exchange", sort="-x"),
        x=alt.X("num_trades:Q", title="Number of Trades"),
        color=alt.Color("exchange:N", legend=None),
        tooltip=[
            alt.Tooltip("exchange:N", title="Exchange"),
            alt.Tooltip("num_trades:Q", title="Trades")
        ]
    ).properties(
        title=f"Number of Trades per Exchange – {period_label}",
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
