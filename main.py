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

# Dash App Setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "CPG Sales Dashboard"

app.layout = dbc.Container([
    html.H1("CPG Sales Data Dashboard", style={'textAlign': 'center', 'color': 'green'}),

    # Summary Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Revenue", className="text-white bg-success"),
            dbc.CardBody(html.H5(f"${total_revenue:,.2f}", className="card-title"))
        ], className="mb-4"), md=3),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Units Sold", className="text-white bg-success"),
            dbc.CardBody(html.H5(f"{total_units:,}", className="card-title"))
        ], className="mb-4"), md=3),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Average Return (%)", className="text-white bg-success"),
            dbc.CardBody(html.H5(f"{avg_return:.2f}%", className="card-title"))
        ], className="mb-4"), md=3),

        dbc.Col(dbc.Card([
            dbc.CardHeader("Average Discount (%)", className="text-white bg-success"),
            dbc.CardBody(html.H5(f"{avg_discount:.2f}%", className="card-title"))
        ], className="mb-4"), md=3),
    ]),

    # Graphs
    dcc.Graph(
        figure=px.bar(revenue_by_product, x="Product Line", y="Revenue ($)", 
                      title="Total Revenue by Product Line", template="plotly_white")
        .update_layout(title_font_color='green')
    ),

    dcc.Graph(
        figure=px.bar(units_by_region, x="Sales Region", y="Units Sold", 
                      title="Units Sold by Sales Region", template="plotly_white")
        .update_layout(title_font_color='green')
    ),

    dcc.Graph(
        figure=px.scatter(returns_vs_revenue, x="Returns (%)", y="Revenue ($)", text="Product Line",
                          title="Returns vs. Revenue by Product Line", template="plotly_white")
        .update_traces(textposition='top center')
        .update_layout(title_font_color='green')
    ),

    dcc.Graph(
        figure=px.bar(discount_by_product, x="Product Line", y="Avg Discount (%)", 
                      title="Average Discount by Product Line", template="plotly_white")
        .update_layout(title_font_color='green')
    ),

    # Data Table with Pagination
    html.Div([
        html.H3("Sales Records (Paginated)", style={'color': 'green'}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_current=0,
            page_size=10,
            page_action='native',
            style_header={
                'backgroundColor': 'darkgreen',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'center',
                'padding': '8px',
                'backgroundColor': '#f4fff4',
                'color': '#003300'
            },
            style_table={
                'overflowX': 'auto',
                'border': '1px solid #aaffaa',
                'borderRadius': '8px',
                'marginTop': '20px'
            }
        )
    ]),

    # Strategic Recommendations
    html.Div([
        html.H3("Strategic Recommendations", style={'color': 'green'}),
        html.Ul([
            html.Li("Invest in top-performing product lines."),
            html.Li("Develop region-specific strategies for underperforming areas."),
            html.Li("Address product quality to reduce high return rates."),
            html.Li("Evaluate discount effectiveness and refine pricing strategies."),
            html.Li("Make data-driven decisions for ongoing growth.")
        ])
    ], style={'backgroundColor': '#e6ffe6', 'padding': '20px', 'borderRadius': '10px'}),

    # Overall Summary
    html.Div([
        html.H3("Overall Summary & Strategic Recommendations", style={'color': 'green'}),
        html.H5("Key Takeaways", style={'color': 'darkgreen'}),
        html.Ul([
            html.Li("Revenue is likely concentrated in a few key product lines."),
            html.Li("Sales performance varies significantly by region, indicating untapped potential."),
            html.Li("High returns on certain products may impact profitability and satisfaction."),
            html.Li("Some products may be over-reliant on discounts, eroding brand value.")
        ]),
        html.H5("Actionable Strategies", style={'color': 'darkgreen'}),
        html.Ul([
            html.Li("Focused Growth: Invest in high-performing product lines and replicate success."),
            html.Li("Regional Expansion/Optimization: Tailor strategies for underperforming regions."),
            html.Li("Product Quality & Communication: Reduce returns with quality and clear messaging."),
            html.Li("Strategic Pricing: Optimize pricing and promotions to boost margins."),
            html.Li("Data-Driven Decisions: Monitor and adapt regularly for sustained growth.")
        ])
    ], style={'backgroundColor': '#ccffcc', 'padding': '20px', 'borderRadius': '10px', 'marginTop': '20px'})
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)
app.run_server(host='0.0.0.0', port=int(os.environ.get("PORT", 8050)))