from dash import Dash, dcc, html, Input, Output # Dash components you need
import plotly.express as px # Dash relies on Plotly to actually do the plotting.  Plotly creates an HTML page with lots of JavaScript.
import pandas as pd

#Load CSV files and convert them into a dataframe
hitter_df = pd.read_csv("hitting_player_stats.csv")
pitcher_df = pd.read_csv("pitching_player_stats.csv")

#Get unique players
statistics = pd.Series(hitter_df['Statistic']).unique()

#Initialize Dash app
app = Dash(__name__)

#For deploying to Render.com
server = app.server

#HTML component layout
app.layout = html.Div([
  dcc.Dropdown(
    id="statistics-dropdown",
    options = [{"label": symbol, "value": symbol} for symbol in statistics],
    value="Base on Balls"
  ),
  dcc.Graph(id="hitters-statistics")
])

@app.callback(
  Output("hitters-statistics", "figure"),
  [Input("statistics-dropdown", "value")]
)
def update_graph(symbol):
  filteredDF = hitter_df[hitter_df['Statistic'] == symbol]
  fig = px.line(
        filteredDF, 
        x="Year", 
        y="Value", 
        color="Name", 
        title=f"Average {symbol} per Year",
        markers=True
    )
  return fig

if __name__ == "__main__":
  app.run(debug=True)
