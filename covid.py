import dash
from dash import Dash, dash_table, Input, Output, dash_table
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from numerize import numerize

# Read in data
df = pd.read_csv("owid-covid-data.csv", usecols=["date", "iso_code", "total_cases", "new_cases", "location", "total_deaths", "continent", "new_deaths"])
df_line = df[df.iso_code == 'USA']
nRow, nCol = df.shape
print('There are {nRow} rows and {nCol} columns')

# Create line graph
fig_line = px.line(df_line, x="date", y=["new_cases", "total_deaths"], title = "Daily COVID-19 Cases/Cumalative Deaths",
              color_discrete_map={"new_cases": "gold", "total_deaths": "silver"})

# Changing names of legend
newnames = {"new_cases" : "New Cases", "total_deaths" : "Total Deaths"}
fig_line.for_each_trace(lambda t: t.update(name = newnames[t.name]))

fig_line.update_layout(
    template="plotly_dark",
    yaxis_title="Cases"
)

def my_value(number):
    return ("{:,}".format(number))  

df_new_cases = my_value(df["new_cases"].sum())
df_new_deaths = my_value(df["new_deaths"].sum())

# Pie chart
# Initialized with USA, IND, MEX
countries = ['USA', 'IND', 'MEX']
df_pie = df[df.iso_code.isin(countries)].groupby('iso_code', as_index=False)['new_cases'].sum()
fig_pie = px.pie(df_pie, values='new_cases', names='iso_code', title="Total COVID-19 Cases Global Comparison")
fig_pie.update_layout(
    template="plotly_dark"
)

fig_bar = px.bar(df_pie, y='new_cases', x = 'iso_code', title = "Total COVID-19 Cases Global Comparison", color = "iso_code")
fig_bar.update_layout(
    template="plotly_dark"
)

# Map chart
df_map = df[~df.continent.isnull()].groupby('iso_code', as_index=False)['new_cases'].sum()
fig_map = px.choropleth(df_map, locations="iso_code",
                    color="new_cases", # lifeExp is a column of gapminder
                    hover_name="iso_code", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title = "Worldwide COVID-19 Cases",
                    )
fig_map.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0}, title_text = 'Worldwide COVID-19 Case')


# Read USA data
df_usa = pd.read_csv("USA Covid Data.csv", usecols=["State", "Total Cases", "Total Deaths"])

df_states = pd.read_csv("csvData.csv", usecols=["State", "Code"])

df_usa_data = pd.merge(df_usa, df_states, on='State', how='inner')

# USA Map
fig_usa = px.choropleth(df_usa_data, locations="Code",
                    locationmode = "USA-states",
                    color = "Total Cases",
                    color_continuous_scale=px.colors.sequential.Jet,
                    hover_name="State",
                    scope="usa",
                    title="USA COVID-19 Cases")
fig_usa.update_layout(template="plotly_dark", margin={"r":0,"t":0,"l":0,"b":0})

df_usa_cases = my_value(df_usa["Total Cases"].sum())
df_usa_deaths = my_value(df_usa["Total Deaths"].sum())

app = dash.Dash(__name__)
app.title = "COVID-19 Data"

app.layout = html.Div([

    # Header
    html.H1("COVID-19 Dashboard", style={'textAlign': 'center', "font-family" : "Verdana, sans-serif", "font-size" : "30px", "color": "blue"}),

    # First row. Line graph
    html.Div([
        dcc.Dropdown(df.location.unique(), 'United States', id='country-dropdown', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(
            id="covid-chart",
            figure=fig_line,
            config={"displayModeBar": False}
        )
    ]),

    html.Br(),

    html.Div([
        dcc.Dropdown(df.iso_code.unique(), id='country-dropdown3', value=['USA', 'IND', 'MEX', 'GBR', 'ITA', 'JPN', 'CAN', 'AUS', 'RUS', 'FRA', 'DNK', 'DEU', 'ISR', 'BRA', 'ARG', 'ESP', 'UKR'], multi=True),
        dcc.Graph(
            id = "covid-bar",
            figure = fig_bar,
            config={"displayModeBar": False}
        )
    ]),

    # Line Break
    html.Br(),

    # Second row. Pie chart and stats.
    html.Div([    
            html.Div(children = [

                dcc.Dropdown(df.iso_code.unique(), id='country-dropdown2', value=['USA', 'IND', 'MEX'], multi=True),
                dcc.Graph(
                    id="covid-pie",
                    figure=fig_pie,
                    config={"displayModeBar": False}
                )
            ],style={'width': '48%', 'display': 'inline-block'}),

            html.Div(
                children = [
                html.Div(children = [

                    html.H1("Total Cases", style={'textAlign': 'center'}),
                    html.H1(df_new_cases, style={'textAlign': 'center'})
                    ], style={ 
                    'display' : 'inline-block', 
                    "border" : "2px black solid", 
                    "background-color" : "lightgreen",
                    "width" : "300px",
                    "height" : "100px",
                    "font-size" : "12px",
                    "font-family" : "Verdana, sans-serif",
                    "border-radius" : "10px",
                    "margin" : "20px"
                    }),

                html.Div(children = [

                    html.H1("Total Deaths", style={'textAlign': 'center'}),
                    html.H1(df_new_deaths, style={'textAlign': 'center'})
                    ], style={ 
                    'display' : 'inline-block', 
                    "border" : "2px black solid", 
                    "background-color" : "lightcoral",
                    "width" : "300px",
                    "height" : "100px",
                    "font-size" : "12px",
                    "font-family" : "Verdana, sans-serif",
                    "border-radius" : "10px",
                    "margin" : "20px"
                    }),
                
                html.Div(children = [

                    html.H1("Total US Cases", style={'textAlign': 'center'}),
                    html.H1(df_usa_cases, style={'textAlign': 'center'})
                    ], style={
                    'display' : 'inline-block', 
                    "border" : "2px black solid", 
                    # "margin-top": "10px",
                    # "margin-bottom": "10px",
                    # "margin-right": "100px",
                    # "margin-left": "375px",
                    "background-color" : "lightblue",
                    "width" : "300px",
                    "height" : "100px",
                    "font-size" : "12px",
                    "font-family" : "Verdana, sans-serif",
                    "border-radius" : "10px",
                    "margin" : "20px"
                    }),
                
                html.Div(children = [

                    html.H1("Total US Deaths", style={'textAlign': 'center'}),
                    html.H1(df_usa_deaths, style={'textAlign': 'center'})
                    ], style={ 
                    'display' : 'inline-block', 
                    "border" : "2px black solid", 
                    "background-color" : "lightyellow",
                    "width" : "300px",
                    "height" : "100px",
                    "font-size" : "12px",
                    "font-family" : "Verdana, sans-serif",
                    "border-radius" : "10px",
                    "margin" : "20px"
                    }),
                ], style={'width': '48%', 'display': 'inline-block', 'margin': 'auto', 'textAlign': 'center'} 
            ),
    ]),

    # Line Break
    html.Br(),

    # Third row. World covid map
    
    html.Div([
        html.H3("Worldwide COVID-19 Cases", style={"background-color" : "white", "color": "black"}),
        dcc.Graph(
            id="covid-map",
            figure=fig_map,
            config={"displayModeBar": False}
        )
    ]),

    # Line Break
    html.Br(),

    # Fourth Row. USA covid map
    html.Div([
        html.H3("USA COVID-19 Cases", style={"background-color" : "white", "color": "black"}),
        dcc.Graph(
            id="covid-USA-map",
            figure=fig_usa,
            config={"displayModeBar": False}
        )
    ]),
])


@app.callback(
    Output('covid-bar', 'figure'),
    Input('country-dropdown3', 'value')
)
def update_barchart(value):
    if value is None:
        value = ['USA']
    df_bar = df[df.iso_code.isin(value)].groupby('iso_code', as_index=False)['new_cases'].sum()
    fig_bar = px.bar(df_bar, y='new_cases', x = 'iso_code', title = "Total COVID-19 Cases Global Comparison", color = "iso_code")
    fig_bar.update_layout(
        template="plotly_dark"
    )
    return fig_bar

@app.callback(
    Output('covid-pie', 'figure'),
    Input('country-dropdown2', 'value')
)
def update_piechart(value):
    if value is None:
        value = ['USA']
    df_pie = df[df.iso_code.isin(value)].groupby('iso_code', as_index=False)['new_cases'].sum()
    fig_pie = px.pie(df_pie, values='new_cases', names='iso_code', title="Total COVID-19 Cases Global Comparison", hole=.5)
    fig_pie.update_layout(
        template="plotly_dark"
    )
    return fig_pie


@app.callback(
    Output('covid-chart', 'figure'),
    Input('country-dropdown', 'value')
)
def update_output(value):
    df_line = df[df.location == value]
    fig_line = px.line(df_line, x="date", y=["new_cases", "total_deaths"], title="Daily COVID-19 Cases/Cumalative Deaths",
                  color_discrete_map={"new_cases": "gold", "total_deaths": "silver"})
    fig_line.for_each_trace(lambda t: t.update(name = newnames[t.name]))
    fig_line.update_layout(
        template="plotly_dark",
        yaxis_title="Cases"
    )

    return fig_line

if __name__ == "__main__":
    app.run_server(debug=True)