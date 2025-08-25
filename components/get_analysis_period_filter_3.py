import streamlit as st
import pandas as pd
from components.get_last_closed_week_2 import get_last_closed_week  # função auxiliar

def get_analysis_period_filter(df_full):
    # Garante que a coluna 'date' esteja em datetime
    df_full["date"] = pd.to_datetime(df_full["date"])
    max_date = df_full["date"].max()

    # Dropdown para escolher período
    option = st.selectbox("Select analysis period", ["Week", "Month", "Quarter", "Year"])

    if option == "Week":
        analysis_df, label, analysis_start, analysis_end = get_last_closed_week(df_full)
        analysis_label = f"Last business week: {label}"
    else:
        days_map = {"Month": 21, "Quarter": 63, "Year": 252}
        days_back = days_map.get(option, 21)

        # Define intervalo de datas úteis
        analysis_start = max_date - pd.tseries.offsets.BDay(days_back - 1)
        analysis_end = max_date

        analysis_df = df_full[df_full["date"] >= analysis_start].copy()
        analysis_label = f"Last {option.lower()}"

    # Agora retornando também o option (period_key)
    return analysis_df, analysis_label, analysis_start, analysis_end, option