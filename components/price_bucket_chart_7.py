import streamlit as st
import pandas as pd
import altair as alt

def show_price_bucket_chart_from_consolidated(df_consolidated, period_label, end_date):
    st.subheader(f"{period_label} ending on {end_date.strftime('%Y-%m-%d')}")

    if df_consolidated.empty:
        st.warning("⚠️ No data available to plot.")
        return

    # Derrete (melt) para formato longo
    df_melt = df_consolidated.melt(
        id_vars="category_price_bucket",
        value_vars=["bid_volume", "ask_volume"],
        var_name="Side",
        value_name="Volume"
    )

    df_melt["Side"] = df_melt["Side"].map({
        "bid_volume": "Bid",
        "ask_volume": "Ask"
    })

    df_melt["category_price_bucket"] = pd.Categorical(
        df_melt["category_price_bucket"],
        categories=df_consolidated["category_price_bucket"],
        ordered=True
    )

    # Gráfico Altair com ajustes visuais
    chart = alt.Chart(df_melt).mark_bar().encode(
        x=alt.X("category_price_bucket:N",
                title="**Price Bucket**",
                axis=alt.Axis(labelAngle=0, labelFontSize=18, titleFontSize=18, titleFontWeight='bold')),
        y=alt.Y("Volume:Q",
                title="Volume",
                axis=alt.Axis(titleFontSize=18, titleFontWeight='bold')),
        color=alt.Color("Side:N",
                        title="Side",
                        scale=alt.Scale(
                            domain=["Bid", "Ask"],
                            range=["#2ecc71", "#e74c3c"]
                        ))
    ).properties(
        width=600,
        height=400,
        title=alt.TitleParams(
            text=f"{period_label}: {end_date.strftime('%b %d, %Y')}",
            fontSize=18,
            fontWeight='bold'
        )
    )

    st.altair_chart(chart, use_container_width=True)
