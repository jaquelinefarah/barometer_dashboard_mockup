# components/weekly_trading_demo.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_weekly_trading_demo() -> None:
    st.subheader("🔎 Weekly Trading Activity – Top 5 Buyers and Sellers (Interleaved)")

    buyers = [
        "Interactive Brokers",
        "The Depository Trust Co.",
        "CIBC Mellon",
        "RBC 01",
        "Citibank 16",
    ]
    sellers = [
        "Questrade Inc.",
        "BMO Nesbitt",
        "RBC Capital Mkts",
        "Fidelity Canada",
        "Ventum Financial",
    ]
    weeks = ["Week 4", "Week 3", "Week 2", "Week 1"]

    # --- simulação com leve variação por semana ---
    rng = np.random.default_rng(42)
    data = []
    for w_idx, week in enumerate(weeks):
        for i in range(5):
            buy_vol  = 100_000 - i*10_000 + rng.integers(-4_000, 4_000) + w_idx*1_000
            sell_vol =  60_000 + i*5_000  + rng.integers(-3_000, 3_000) + w_idx*800
            data.append({"week": week, "broker": buyers[i],  "volume": int(max(1, buy_vol)),  "type": "Buy"})
            data.append({"week": week, "broker": sellers[i], "volume": int(max(1, sell_vol)), "type": "Sell"})

    df = pd.DataFrame(data)

    week_figs = []
    for week in weeks:
        week_df = df[df["week"] == week].copy()
        buy_df  = week_df[week_df["type"] == "Buy"].reset_index(drop=True)
        sell_df = week_df[week_df["type"] == "Sell"].reset_index(drop=True)

        bars = []
        for i in range(5):
            bars.append({"label": buy_df.loc[i, "broker"],  "volume": buy_df.loc[i, "volume"],  "type": "Buy"})
            bars.append({"label": sell_df.loc[i, "broker"], "volume": sell_df.loc[i, "volume"], "type": "Sell"})
        wdf = pd.DataFrame(bars)

        order = wdf["label"].tolist()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=wdf.loc[wdf["type"]=="Buy","label"],
            y=wdf.loc[wdf["type"]=="Buy","volume"],
            name="Buy", marker_color="green"
        ))
        fig.add_trace(go.Bar(
            x=wdf.loc[wdf["type"]=="Sell","label"],
            y=wdf.loc[wdf["type"]=="Sell","volume"],
            name="Sell", marker_color="red"
        ))
        fig.update_xaxes(categoryorder="array", categoryarray=order, tickangle=-40)
        fig.update_layout(
            title=week, xaxis_title=None, yaxis_title="Volume",
            barmode="group", template="simple_white", showlegend=False,
            height=400, margin=dict(l=20, r=20, t=40, b=20),
        )
        week_figs.append(fig)

    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.plotly_chart(week_figs[i], use_container_width=True)
