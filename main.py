# main.py
from __future__ import annotations
import pandas as pd
from pathlib import Path
import streamlit as st

from utils.load_data import load_broker_data
from components.layout import set_global_styles, render_sidebar_brand
from utils.periods_sidebar import render_period_sidebar

from components.metrics import compute_metrics
from components.cards import render_metric_cards
from components.short_interest import render_short_interest
from components.general_profile import render_general_profile
from components.top_buyers_sellers import render_top_buyers_sellers
from components.weekly_top5_interleaved import render_weekly_trading_demo # << use a função de alto nível

def main():
    # 1) Page + global CSS
    st.set_page_config(page_title="Broker Trading Barometer", layout="wide")
    set_global_styles()

    # 2) Brand na sidebar
    win_logo = Path(r"C:\Projects\valore_dashboard_brokers\assets\logo.png")
    logo_path = str(win_logo) if win_logo.exists() else "assets/logo.png"
    render_sidebar_brand(title="Broker Trading Barometer", logo_path=logo_path)

    # 3) Carrega base
    df = load_broker_data()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 4) Sidebar → seção + períodos
    section, preset, start_date, end_date, cur_df, prev_df, period_label = render_period_sidebar(
        df,
        date_col="date",
        sections=[
            "Company View",
            "Short Interest",
            "General Profile",
            "Top Buyers & Sellers",
            "Weekly Trading (demo)",  # <- nome padronizado
        ],
        show_filters_title=False,
    )

    # 5) Conteúdo principal
    if section == "Company View":
        metrics = compute_metrics(cur_df, prev_df)
        render_metric_cards(metrics, cols_per_row=4, title=section)

    elif section == "Short Interest":
        render_short_interest(cur_df)

    elif section == "General Profile":
        render_general_profile(cur_df, prev_df)

    elif section == "Top Buyers & Sellers":
        render_top_buyers_sellers(cur_df, top_n=5, show_tables=False)


    elif section == "Weekly Trading (demo)":
        render_weekly_trading_demo()    
        


    else:
        st.info("Select a section in the sidebar.")

if __name__ == "__main__":
    main()
