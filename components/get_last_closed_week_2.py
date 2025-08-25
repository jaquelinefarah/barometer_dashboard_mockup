from datetime import timedelta
import pandas as pd

def get_last_closed_week(df_full):
    """
    Retorna a última semana fechada (segunda a sexta) e o dataframe filtrado.
    """
    df_full["date"] = pd.to_datetime(df_full["date"])
    max_date = pd.to_datetime(df_full["date"].max())  # garante tipo datetime

    # Encontra a última sexta-feira <= max_date
    weekday = max_date.weekday()
    last_friday = max_date - timedelta(days=(weekday - 4) % 7)
    last_monday = last_friday - timedelta(days=4)

    mask = (df_full["date"] >= last_monday) & (df_full["date"] <= last_friday)
    filtered_df = df_full.loc[mask].copy()

    label = f"{last_monday.strftime('%b %d')} - {last_friday.strftime('%b %d, %Y')}"
    return filtered_df, label, last_monday, last_friday