# components/top_traders.py
from __future__ import annotations
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

def _to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    if "date" in data.columns:
        data["date"] = pd.to_datetime(data["date"], errors="coerce")
    for c in ["buy_volume", "sell_volume"]:
        data[c] = _to_num(data[c]) if c in data.columns else 0
    if "broker" not in data.columns:
        if "investor" in data.columns:
            data = data.rename(columns={"investor": "broker"})
        else:
            data["broker"] = "Unknown"
    return data

def _bar_h(df: pd.DataFrame, x_col: str, y_col: str, title: str, color: str) -> go.Figure:
    fig = go.Figure(go.Bar(
        x=df[x_col],
        y=df[y_col],
        orientation="h",
        marker=dict(color=color),
        text=df[x_col].map(lambda v: f"{v:,.0f}"),
        textposition="outside"
    ))
    h = max(260, 48 * len(df))
    fig.update_layout(
        title=title,
        height=h,
        margin=dict(l=10, r=20, t=40, b=10),
        xaxis_title="Volume",
        yaxis_title=None
    )
    return fig

def render_top_buyers_sellers(cur_df: pd.DataFrame, top_n: int = 5, show_tables: bool = False) -> None:
    """Render two side-by-side bar charts: Top-N Buyers and Top-N Sellers by accumulated volume."""
    if cur_df is None or cur_df.empty:
        st.info("No data in the selected period.")
        return

    data = _normalize(cur_df)

    buyers = (data.groupby("broker", as_index=False)["buy_volume"].sum()
                    .sort_values("buy_volume", ascending=False)
                    .head(top_n))
    sellers = (data.groupby("broker", as_index=False)["sell_volume"].sum()
                     .sort_values("sell_volume", ascending=False)
                     .head(top_n))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 🟢 Top {top_n} Buyers (by Volume)")
        st.plotly_chart(
            _bar_h(buyers, "buy_volume", "broker", f"Top {top_n} Buyers – Accumulated Volume", "#2ecc71"),
            use_container_width=True
        )
    with col2:
        st.markdown(f"### 🔴 Top {top_n} Sellers (by Volume)")
        st.plotly_chart(
            _bar_h(sellers, "sell_volume", "broker", f"Top {top_n} Sellers – Accumulated Volume", "#e74c3c"),
            use_container_width=True
        )

    if show_tables:
        with st.expander("🔎 See data tables"):
            c1, c2 = st.columns(2)
            with c1:
                st.dataframe(buyers.rename(columns={"buy_volume":"volume"}), use_container_width=True)
            with c2:
                st.dataframe(sellers.rename(columns={"sell_volume":"volume"}), use_container_width=True)
