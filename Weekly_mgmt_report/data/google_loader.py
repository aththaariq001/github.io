import pandas as pd
from data.gsheet_config import client
import logging

datasets = {
    "Boys": "1lrsRvkeYP3fLZC5O1zVjTlDdKw-2pU2BomUdN8HYq14",
    "Girls": "1SGuff5mWle-8Q4FZ4WBp4jl71hrC0zUIvwALytTgKh8",
    "Technology": "1KLbYL_aDUkBhU5Skd_-RTDr01jJIiak6qz1Rn3MSyUQ",
    "Properties": "1px3xBX7PO1k5mHoXoThU3g6LOSoCUYQSkdqeROUxn-s"
}

def load_data(spreadsheet_id, worksheet_name="Flattened", source_name=""):
    try:
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
        df = pd.DataFrame(sheet.get_all_records())
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce").fillna(0)
        df["Week Start Date"] = pd.to_datetime(df["Week Start Date"])
        df["Source"] = source_name
        logging.info(f"Successfully loaded data from '{spreadsheet_id}' - '{worksheet_name}'")
        return df
    except Exception as e:
        logging.error(f"Error loading {spreadsheet_id}: {e}")
        return pd.DataFrame()

data_boys = load_data(datasets["Boys"], source_name="Boys")
data_girls = load_data(datasets["Girls"], source_name="Girls")
data_tech = load_data(datasets["Technology"], source_name="Technology")
data_properties = load_data(datasets["Properties"], source_name="Properties & Investment")
