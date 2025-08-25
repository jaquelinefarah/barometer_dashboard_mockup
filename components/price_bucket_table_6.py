import streamlit as st

def show_price_bucket_table(df_filtered, period_label, end_date):

   # Checks if the essential columns exist
    required_columns = ["price_bucket", "volume", "bid_volume", "ask_volume"]
    missing_cols = [col for col in required_columns if col not in df_filtered.columns]
    if missing_cols:
        st.error(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
        return

    # Remove price buckets null
    df_filtered = df_filtered[df_filtered["price_bucket"].notna()]


    df_filtered["check_sum"] = df_filtered["bid_volume"] + df_filtered["ask_volume"]
    #=== st.dataframe(df_filtered[["volume", "check_sum"]].head(10))

    # Grouping
    grouped = (
        df_filtered.groupby("price_bucket")
        .agg(
            total_volume=("volume", "sum"),
            total_bid=("bid_volume", "sum"),
            total_ask=("ask_volume", "sum"),
            transactions=("volume", "count")
        )
        .reset_index()
    )

    if grouped.empty:
        st.info("Not enough data for this period.")
        return

    # Order by volume and later by price
    grouped["Price Range"] = grouped["price_bucket"].astype(float)
    grouped = grouped.sort_values(by="total_volume", ascending=False).head(5)
    grouped = grouped.sort_values(by="Price Range", ascending=True)
    grouped["Price Range"] = grouped["Price Range"].map(lambda x: f"{x:.3f}")

    # Change the name for view
    grouped.rename(columns={
        "total_volume": "Total Volume",
        "total_bid": "Bid Volume",
        "total_ask": "Ask Volume",
        "transactions": "Transactions"
    }, inplace=True)

    # Format values
    for col in ["Total Volume", "Bid Volume", "Ask Volume"]:
        grouped[col] = grouped[col].apply(lambda x: f"{int(x):,}")

    # Show the table
    st.subheader(f"{period_label} ending on {end_date.strftime('%Y-%m-%d')}")
    st.dataframe(grouped[[ 
        "Price Range", "Total Volume", "Bid Volume", "Ask Volume", "Transactions"
    ]], use_container_width=True)
