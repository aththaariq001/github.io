import pandas as pd
from data.google_loader import data_boys, data_girls, data_tech, data_properties

combined_data = pd.concat([data_boys, data_girls], ignore_index=True)

def create_category_metric_map(df):
    if df.empty:
        return {}
    return df.groupby("Category")["Metric"].unique().apply(list).to_dict()

category_metric_map_combined = create_category_metric_map(combined_data)
category_metric_map_tech = create_category_metric_map(data_tech)
category_metric_map_properties = create_category_metric_map(data_properties) if not data_properties.empty else {}

categories_combined = combined_data["Category"].drop_duplicates().tolist() if not combined_data.empty else []
categories_tech = data_tech["Category"].drop_duplicates().tolist() if not data_tech.empty else []
categories_properties = data_properties["Category"].drop_duplicates().tolist() if not data_properties.empty else []
