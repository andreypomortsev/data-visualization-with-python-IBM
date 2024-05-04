#!/usr/bin/env python
# coding: utf-8


import dash

# import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/\
IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)
# Change vehicle type names
data["Vehicle_Type"] = data["Vehicle_Type"].apply(
    lambda x: x.replace("familiy", "family")
    .replace("family", " family")
    .replace("car", " car")
    .replace("Sports", "Sports car")
)


# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# ---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]
# List of years
year_list = list(range(1980, 2024))
# ---------------------------------------------------------------------------------------
# Dropdown style
dropdown_style = {
    "width": "80%",
    "padding": "2px",
    "fontSize": "20px",
    "textAlign": "center",
    "flexWrap": "wrap",
    "justifyContent": "center",
}

# Create the layout of the app
app.layout = html.Div(
    [
        # TASK 2.1 Add title to the dashboard
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 24},
        ),
        html.Div(
            [  # TASK 2.2: Add two dropdown menus
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    placeholder="Select a report type.",
                    style=dropdown_style,
                ),
            ]
        ),
        html.Div(
            [
                html.Label("Select a Year:"),
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": str(year), "value": year} for year in year_list],
                    placeholder="Select a year.",
                    style=dropdown_style,
                ),
            ]
        ),
        html.Div(
            [  # TASK 2.3: Add a division for output display
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={"display": "flex"},
                ),
            ]
        ),
    ]
)


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(statistics: str) -> bool:
    return statistics != "Yearly Statistics"


# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="select-year", component_property="value"),
        Input(component_id="dropdown-statistics", component_property="value"),
    ],
)
def update_output_container(input_year, selected_statistics):
    if selected_statistics == "Recession Period Statistics":
        # Filter the data for recession periods
        recession_data = data[data["Recession"] == 1]

        # TASK 2.5: Create and display graphs for Recession Report Statistics

        # Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        title_one = "Average Automobile Sales fluctuation over Recession Period"
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                markers="o",
                title=title_one,
            )
            .update_layout(
                title_x=0.5, xaxis_title="Year", yaxis_title="Automobile Sales"
            )
            .update_traces(line=dict(dash="dot"))
        )

        # Plot 2 Calculate the average number of vehicles sold by vehicle type
        # use groupby to create relevant data for plotting
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.pie(
                average_sales,
                values="Automobile_Sales",
                names="Vehicle_Type",
                title="Average Automobile Sales by Vehicle Type",
            ).update_layout(title_x=0.5)
        )

        # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .mean()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Expenditure Share by Vehicle Type",
            ).update_layout(title_x=0.5)
        )

        # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unempl_vt_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
            .sort_values(by="Automobile_Sales", ascending=False)
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unempl_vt_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Sales by Vehicle Type",
            ).update_layout(
                title_x=0.5, xaxis_title="Vehicle Type", yaxis_title="Automobile Sales"
            )
        )

        return [
            # First row with two plots
            html.Div(
                [
                    html.Div(children=R_chart1, className="chart-item"),
                    html.Div(children=R_chart3, className="chart-item"),
                ],
                className="chart-row",
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            # Second row with two plots
            html.Div(
                [
                    html.Div(children=R_chart2, className="chart-item"),
                    html.Div(children=R_chart4, className="chart-item"),
                ],
                className="chart-row",
                style={
                    "display": "flex",
                },
            ),
        ]

    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots
    elif input_year and selected_statistics == "Yearly Statistics":
        yearly_data = data[data["Year"] == input_year]

        # TASK 2.5: Creating Graphs Yearly data

        # plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales"
            ).update_layout(
                title_x=0.5, xaxis_title="Year", yaxis_title="Automobile Sales"
            )
        )

        # Plot 2 Total Monthly Automobile sales using line chart.
        mas = (
            yearly_data.groupby("Month", sort=False)["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title=f"Monthly Automobile Sales in {input_year}",
            ).update_layout(
                title_x=0.5, xaxis_title="Month", yaxis_title="Automobile Sales"
            )
        )

        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type", sort=False)["Automobile_Sales"]
            .mean()
            .reset_index()
            .sort_values(by="Automobile_Sales", ascending=False)
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=f"Average Vehicles Sold by Vehicle Type in {input_year}",
            ).update_layout(
                title_x=0.5, xaxis_title="Vehicle Type", yaxis_title="Automobile Sales"
            )
        )

        # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title=f"Total Advertisement Expenditure by Vehicle Type in {input_year}",
            ).update_layout(title_x=0.5)
        )

        # TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            # First row with two plots
            html.Div(
                [
                    html.Div(children=Y_chart2, className="chart-item"),
                    html.Div(children=Y_chart4, className="chart-item"),
                ],
                className="chart-row",
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                },
            ),
            # Second row with two plots
            html.Div(
                [
                    html.Div(children=Y_chart1, className="chart-item"),
                    html.Div(children=Y_chart3, className="chart-item"),
                ],
                className="chart-row",
                style={"display": "flex", "flexWrap": "wrap"},
            ),
        ]


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
