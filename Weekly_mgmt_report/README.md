# Management Report Dashboard

This project is a management reporting dashboard built with [Dash](https://dash.plotly.com/) and [Plotly](https://plotly.com/python/) for visualizing performance metrics from multiple data sources, including Google Sheets. The dashboard allows you to:

- View metrics related to Boys & Girls centers, Technology initiatives, and Properties & Investments.
- Filter data by categories, metrics, and date ranges.
- Explore KPIs and visualizations (line charts, bubble charts, radar charts).
- Download filtered data as a CSV file.

## Features

- **Dynamic Filtering**: Choose datasets, categories, metrics, and custom date ranges.
- **KPI Cards**: View current-week values, percentage changes, averages, max/min values.
- **Interactive Visualizations**: Line charts with rolling averages, bubble charts for aggregate metric values, and radar charts to compare metrics.
- **Google Sheets Integration**: Data is fetched from Google Sheets using service account credentials.
- **Modular Structure**: Code is split into multiple files for components, data loading, preprocessing, and utilities.
- **Theming**: Custom styling with `custom.css` and a Plotly template for consistent look & feel.

## Project Structure

project/
├── app.py
├── assets/
│   ├── custom.css
│   └── fonts/
├── components/
│   ├── sidebar.py
│   ├── filters.py
│   ├── graphs.py
│   ├── kpis.py
│   ├── tables.py
│   └── layouts/
│       ├── boys_girls.py
│       ├── technology.py
│       └── properties.py
├── data/
│   ├── gsheet_config.py
│   ├── google_loader.py
│   ├── preprocess.py
│   └── sample_data.csv (optional)
├── utils/
│   ├── auth.py (empty if no additional auth logic)
│   └── kpi_calculations.py
├── templates/
│   └── plotly_custom.json
└── README.md

**Key Folders:**
- `app.py`: Main entry point; initializes Dash app, layout, and callbacks.
- `assets/`: Contains CSS and fonts for styling.
- `components/`: Reusable UI components (filters, graphs, tables, KPI cards), plus page layouts.
- `data/`: Scripts to configure Google Sheets client (`gsheet_config.py`), load data (`google_loader.py`), and preprocess it (`preprocess.py`).
- `utils/`: Utility functions such as KPI calculations.
- `templates/`: Plotly templates in JSON format.

## Prerequisites

1. Python 3.7+ installed.
2. A Google Cloud service account JSON file with appropriate permissions to read the specified Google Sheets.  
   - Save it as `service_account.json` in the project root or set the `SERVICE_ACCOUNT_FILE` environment variable.
   
3. Install required dependencies:
   ```bash
   pip install dash dash_bootstrap_components plotly gspread google-auth

## Customization
- Data Sources: Update datasets in data/google_loader.py with your Google Sheet IDs.
- Layout & Styling: Modify assets/custom.css and templates/plotly_custom.json to change the look and feel.
- Additional Metrics or Pages: Add new layout files under components/layouts/ and incorporate them into app.py routing and sidebar.py.

## Troubleshooting
- If data is not loading, ensure the service account has the correct permissions on the target Google Sheets.
- Check the console/logs for errors related to data fetching or callbacks.
- Make sure your date formats and categories match the data in the Sheets.