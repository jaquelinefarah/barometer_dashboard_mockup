import pandas as pd
import os

def load_broker_data(file_path="data/Broker_Daily_Data.csv"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    df = pd.read_csv(file_path)

    # === Limpeza inicial ===
    df.columns = df.columns.str.strip().str.lower()  # padroniza colunas
    df['date'] = pd.to_datetime(df['date'])  # converte a coluna de data

    # === Criação da coluna anon_volume (se não existir) ===
    if 'anon_volume' not in df.columns:
        df['anon_volume'] = 0

    # === Criação da coluna boolean 'anonymous' ===
    df['anonymous'] = df['anon_volume'] > 0  # True se tiver volume anônimo

    return df