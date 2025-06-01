import os
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# Load Excel data
df = pd.read_excel("CPG_Sales_Data_1000_Records.xlsx")

# Aggregated Data
revenue_by_product = df.groupby("Product Line")["Revenue ($)"].sum().reset_index()
units_by_region = df.groupby("Sales Region")["Units Sold"].sum().reset_index()
returns_vs_revenue = df.groupby("Product Line").agg({
    "Revenue ($)": "sum", "Returns (%)": "mean"
}).reset_index()
discount_by_product = df.groupby("Product Line")["Avg Discount (%)"].mean().reset_index()

# Summary metrics
total_revenue = df["Revenue ($)"].sum()
total_units = df["Units Sold"].sum()
avg_return = df["Returns (%)"].mean()
avg_discount = df["Avg Discount (%)"].mean()

# Dash App Setup with server attribute
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # <-- This is the important line you asked for

app.title = "CPG Sales Dashboard"

app.layout = dbc.Container([
    # ... all your layout code remains unchanged ...
], fluid=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
