import streamlit as st
import pandas as pd
from utils.format_variation_for_metrics import format_variation_for_metric

def show_highlights_block(df_full, df_filtered, period_label, start_week, end_week, kpi):
    # === KPIs atuais ===
    total_volume = df_filtered["volume"].sum()
    vwap = (df_filtered["close"] * df_filtered["volume"]).sum() / total_volume if total_volume > 0 else 0

    # Top bucket atual
    if "price_bucket" in df_filtered.columns:
        top_bucket = df_filtered["price_bucket"].mode()[0] if not df_filtered["price_bucket"].mode().empty else "N/A"
    else:
        top_bucket = "N/A"

    # === KPIs do período anterior ===
    business_days = 5
    prev_end = start_week - pd.Timedelta(days=1)
    prev_start = pd.bdate_range(end=prev_end, periods=business_days)[0]
    df_prev = df_full[(df_full["date"] >= prev_start) & (df_full["date"] <= prev_end)]

    prev_total_volume = df_prev["volume"].sum()
    prev_vwap = (df_prev["close"] * df_prev["volume"]).sum() / prev_total_volume if prev_total_volume > 0 else 0

    if "price_bucket" in df_prev.columns:
        prev_top_bucket = df_prev["price_bucket"].mode()[0] if not df_prev["price_bucket"].mode().empty else None
    else:
        prev_top_bucket = None

    # === Variações formatadas (volume, vwap)
    vol_delta, vol_emoji, _ = format_variation_for_metric(total_volume, prev_total_volume)
    vwap_delta, vwap_emoji, _ = format_variation_for_metric(vwap, prev_vwap)

    # === Variação do bucket (numérica e formatada)
    try:
        bucket_delta_value = float(top_bucket) - float(prev_top_bucket)
    except:
        bucket_delta_value = None

    try:
        top_bucket_str = f"${float(top_bucket):.3f}"
    except:
        top_bucket_str = str(top_bucket)

    # === KPIs individualizados ===
    if kpi == "volume":
        st.metric(
            label="📦 Total Volume",
            value=f"{total_volume:,.0f}",
            delta=f"{vol_emoji} {vol_delta}"
        )

    elif kpi == "bucket":
        if bucket_delta_value is not None:
            st.metric(
                label="🎯 Top Price Bucket",
                value=top_bucket_str,
                delta=f"{bucket_delta_value:.3f}"
            )
        else:
            st.metric(
                label="🎯 Top Price Bucket",
                value=top_bucket_str,
                delta="(no previous data)"
            )

    elif kpi == "vwap":
        st.metric(
            label="📊 VWAP",
            value=f"${vwap:.4f}",
            delta=f"{vwap_emoji} {vwap_delta}"
        )