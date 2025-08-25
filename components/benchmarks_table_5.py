import streamlit as st
import pandas as pd
from utils.variation_utils import calculate_variation_arrow
from utils.get_period_data import get_period_data
from components.get_last_closed_week_2 import get_last_closed_week

# Mapping of business days for each time period
DAYS_MAP = {
    "% Week": 5,
    "% Month": 21,
    "% Quarter": 63,
    "% Year": 252
}

# Mapping of business days for each time period
DAYS_MAP = {
    "Week": 5,
    "Month": 21,
    "Quarter": 63,
    "Year": 252
}

def format_val(val, is_volume=False):
    if pd.isna(val):
        return "—"
    if is_volume:
        return f"{val:,.0f}"  # sem $
    return f"${val:.4f}"

def show_benchmarks_table(df_full):
    # === Initialize table structure ===
    table_data = {
        "Price": {"Selected Period": "—"},
        "Total Volume": {"Selected Period": "—"},
        "VWAP": {"Selected Period": "—"},
        "TWAP": {"Selected Period": "—"}
    }

    # === Compute current values (last closed week) ===
    if not df_full.empty:
        table_data["Price"]["Selected Period"] = format_val(df_full["close"].ffill().iloc[-1])
        table_data["Total Volume"]["Selected Period"] = format_val(df_full["volume"].sum(), is_volume=True)
        table_data["VWAP"]["Selected Period"] = format_val(
            (df_full["close"] * df_full["volume"]).sum() / df_full["volume"].sum()
        )
        table_data["TWAP"]["Selected Period"] = format_val(df_full["close"].mean())

    # === Compute variation vs. previous period for each time horizon ===
    for label, business_day in DAYS_MAP.items():
        cur_df, prev_df = get_period_data(
            df_filtered=df_full.copy(),
            period_label=label,
            start_week=df_full["date"].max(),  # usa a última data disponível
            end_week=df_full["date"].max(),
            business_day=business_day
        )

        if cur_df.empty or prev_df.empty:
            table_data["Price"][label] = "—"
            table_data["Total Volume"][label] = "—"
            table_data["VWAP"][label] = "—"
            table_data["TWAP"][label] = "—"
            continue

        # Current values
        current_price = cur_df["close"].ffill().iloc[-1]
        current_vol = cur_df["volume"].sum()
        current_vwap = (cur_df["close"] * cur_df["volume"]).sum() / cur_df["volume"].sum()
        current_twap = cur_df["close"].mean()

        # Previous values
        prev_price = prev_df["close"].ffill().iloc[-1]
        prev_vol = prev_df["volume"].sum()
        prev_vwap = (prev_df["close"] * prev_df["volume"]).sum() / prev_df["volume"].sum()
        prev_twap = prev_df["close"].mean()

        # Variations
        table_data["Price"][label] = calculate_variation_arrow(current_price, prev_price)
        table_data["Total Volume"][label] = calculate_variation_arrow(current_vol, prev_vol)
        table_data["VWAP"][label] = calculate_variation_arrow(current_vwap, prev_vwap)
        table_data["TWAP"][label] = calculate_variation_arrow(current_twap, prev_twap)

    # === Convert to DataFrame ===
    df_benchmarks = pd.DataFrame(table_data).T
    df_benchmarks.columns.name = None

  # === Render styled table with title ===

    st.markdown(df_benchmarks.to_html(escape=False, index=True, classes="wide-table"), unsafe_allow_html=True)