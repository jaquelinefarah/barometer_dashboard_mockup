import streamlit as st
import pandas as pd
from utils.get_period_data import get_period_data

# === Mapeamento de dias úteis por período ===
DAYS_MAP = {
    "Week": 5,
    "Month": 21,
    "Quarter": 63,
    "Year": 252
}

# === Função de formatação ===
def format_val(val, is_volume=False, is_price=False, is_pct=False):
    if pd.isna(val):
        return "—"
    if is_volume:
        return f"{val:,.0f}"
    if is_price:
        return f"${val:.4f}"
    if is_pct:
        return f"{val:.2%}"
    return f"{val:,.0f}"

# === Função de variação ===
def calculate_variation_arrow(current, previous, is_pct=True, is_price=False, is_volume=False):
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return "—"

    variation = current - previous
    percent_change = variation / abs(previous)

    if variation > 0:
        arrow = "⬆️"
        color = "green"
    elif variation < 0:
        arrow = "⬇️"
        color = "red"
    else:
        arrow = "➖"
        color = "gray"

    if is_pct:
        value_str = f"{percent_change:.1%}"
    elif is_price:
        value_str = f"${variation:,.4f}"
    elif is_volume:
        value_str = f"{variation:,.0f}"
    else:
        value_str = f"{variation:,.0f}"

    return f"<span style='color:{color}; font-weight:bold;'>{arrow} {value_str}</span>"

def show_exchange_summary_table(df_filtered, df_full, period_label, start_date, end_date, period_key):
    exchanges = df_full["exchange"].unique()
    cols = st.columns(2)  # duas tabelas por linha
    col_index = 0

    for exch in exchanges:
        table_data = {
            "Total Volume": {"Current": "—", "Δ vs Previous": "—"},
            "VWAP": {"Current": "—", "Δ vs Previous": "—"},
            "Short Interest": {"Current": "—", "Δ vs Previous": "—"},
        }

        # === Período atual ===
        current_df = df_filtered[df_filtered["exchange"] == exch].copy()
        if not current_df.empty:
            cur_vol = current_df["volume"].sum()
            cur_vwap = (current_df["close"] * current_df["volume"]).sum() / current_df["volume"].sum()
            cur_short = current_df["short_interest"].sum()

            table_data["Total Volume"]["Current"] = format_val(cur_vol, is_volume=True)
            table_data["VWAP"]["Current"] = format_val(cur_vwap, is_price=True)
            table_data["Short Interest"]["Current"] = format_val(cur_short)

        # === Período anterior (para variações) ===
        business_day = DAYS_MAP.get(period_key, 5)
        cur_df, prev_df = get_period_data(
            df_filtered=df_full[df_full["exchange"] == exch].copy(),
            period_label=period_key,
            start_week=start_date,
            end_week=end_date,
            business_day=business_day
        )

        if not cur_df.empty and not prev_df.empty:
            cur_vol = cur_df["volume"].sum()
            cur_vwap = (cur_df["close"] * cur_df["volume"]).sum() / cur_df["volume"].sum()
            cur_short = cur_df["short_interest"].sum()

            prev_vol = prev_df["volume"].sum()
            prev_vwap = (prev_df["close"] * prev_df["volume"]).sum() / prev_df["volume"].sum()
            prev_short = prev_df["short_interest"].sum()

            table_data["Total Volume"]["Δ vs Previous"] = calculate_variation_arrow(cur_vol, prev_vol, is_pct=False, is_volume=True)
            table_data["VWAP"]["Δ vs Previous"] = calculate_variation_arrow(cur_vwap, prev_vwap)
            table_data["Short Interest"]["Δ vs Previous"] = calculate_variation_arrow(cur_short, prev_short, is_pct=False)

        # === Renderização em colunas ===
        df_summary = pd.DataFrame(table_data).T
        with cols[col_index]:
            st.markdown(f"**{exch}**")
            st.caption(f"Reference Period: {period_label}")
            st.markdown(df_summary.to_html(escape=False, index=True), unsafe_allow_html=True)

        col_index = (col_index + 1) % 2
