import pandas as pd

def calculate_kpis(df):
    if df.empty:
        return None, None, None, None, None
    sorted_df = df.sort_values("Week Start Date")
    unique_weeks = sorted_df["Week Start Date"].unique()

    current_week_value = sorted_df[sorted_df["Week Start Date"] == unique_weeks[-1]]["Value"].sum() if len(unique_weeks) >= 1 else None
    previous_week_value = sorted_df[sorted_df["Week Start Date"] == unique_weeks[-2]]["Value"].sum() if len(unique_weeks) >= 2 else None

    percent_change = ((current_week_value - previous_week_value) / previous_week_value * 100) if (previous_week_value and previous_week_value != 0) else None
    overall_average = df["Value"].mean() if not df.empty else None
    max_value = df["Value"].max() if not df.empty else None
    min_value = df["Value"].min() if not df.empty else None

    return current_week_value, percent_change, overall_average, max_value, min_value
