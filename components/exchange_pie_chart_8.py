import streamlit as st
import altair as alt
import pandas as pd


def show_exchange_pie_chart_altair(df, period_label, period_key, end_date):
    # 1. Filter valid data
    df = df[df["volume"] > 0].copy()

    if df.empty:
        st.warning(f"No trades available for {period_label}")
        return

    # 2. Aggregate by exchange (using volume instead of row counts)
    exchange_counts = (
        df.groupby("exchange")["volume"]
        .sum()
        .reset_index(name="total_volume")
    )
    total = exchange_counts["total_volume"].sum()
    exchange_counts["percent"] = (exchange_counts["total_volume"] / total) * 100
    exchange_counts["label"] = exchange_counts.apply(
        lambda row: f"{row['exchange']} ({row['percent']:.1f}%)", axis=1
    )

    # 3. Base chart
    base = alt.Chart(exchange_counts).encode(
        theta=alt.Theta("total_volume:Q", stack=True),
        color=alt.Color(
            "exchange:N",
            title="Exchange",
            legend=alt.Legend(labelFontSize=14, titleFontSize=16)
        )
    )

    pie = base.mark_arc(innerRadius=60, outerRadius=120)

    text = base.mark_text(radius=140, size=16, fontWeight="bold").encode(
        text=alt.Text("label:N"),
        color=alt.value("black")
    )

   # 4. Render
    st.markdown(f"""
    <div style="text-align: left; padding-bottom: 10px;">
        <h3 style='margin-bottom:5px; font-size:20px;'>Exchange Distribution</h3>
        <p style='color:gray; font-size:20px;'>
            Last {period_key.lower()} ending on {end_date.strftime('%Y-%m-%d')}
        </p>
    </div>
""", unsafe_allow_html=True)

    st.markdown(f"**Total Volume:** {total:,.0f}")

    st.altair_chart(pie + text, use_container_width=True)