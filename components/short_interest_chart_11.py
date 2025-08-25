import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def show_short_interest_chart(df_full, start_date, end_date, period_label):
    # Copia e garante formato
    df = df_full.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Filtra pelo intervalo de tempo
    df_filtered = df[(df["date"] >= start_date) & (df["date"] <= end_date)].copy()

    # Verifica se as colunas essenciais existem
    required_cols = {"date", "short_interest", "short_interest_ratio"}
    if not required_cols.issubset(df_filtered.columns):
        st.error(f"Missing columns in dataset: {', '.join(required_cols - set(df_filtered.columns))}")
        return

    # Agregar por dia (caso tenha granularidade por exchange ainda)
    df_daily = df_filtered.groupby(df_filtered["date"].dt.date).agg({
        "short_interest": "sum",
        "short_interest_ratio": "mean"   # média do ratio diário
    }).reset_index()
    df_daily["date"] = pd.to_datetime(df_daily["date"])

    # Cria o gráfico
    fig = go.Figure()

    # Short Interest (barras)
    fig.add_trace(go.Bar(
        x=df_daily["date"],
        y=df_daily["short_interest"],
        name="Short Interest",
        marker_color="royalblue",
        yaxis="y"
    ))

    # Short Interest Ratio (linha)
    fig.add_trace(go.Scatter(
        x=df_daily["date"],
        y=df_daily["short_interest_ratio"],
        name="Short Interest Ratio",
        mode="lines+markers",
        line=dict(color="firebrick"),
        yaxis="y2"
    ))

    # Layout do gráfico
    fig.update_layout(
    title=dict(
        text=f"Short Interest & Short Ratio – {period_label} ending on {end_date.strftime('%Y-%m-%d')}",
        font=dict(size=20)
    ),
    xaxis=dict(
        title=dict(text="Date", font=dict(size=16)),
        tickfont=dict(size=14),
        tickformat="%b %d\n%Y",
        showgrid=False   # ❌ remove grid do eixo X
    ),
    yaxis=dict(
        title=dict(text="Short Interest", font=dict(size=16, color="royalblue")),
        tickfont=dict(size=14, color="royalblue"),
        showgrid=True,   # ✅ mantém grid do eixo da esquerda
        gridcolor="lightgray",
        zeroline=False
    ),
    yaxis2=dict(
        title=dict(text="Short Interest Ratio", font=dict(size=16, color="firebrick")),
        tickfont=dict(size=14, color="firebrick"),
        anchor="x",
        overlaying="y",
        side="right",
        showgrid=False   # ❌ desliga grid do eixo da direita
    ),
    legend=dict(
        orientation="h",
        y=-0.2,
        font=dict(size=14)
    ),
    height=500,
    plot_bgcolor='white',
    margin=dict(t=50, b=100)
)

    st.plotly_chart(fig, use_container_width=True)
