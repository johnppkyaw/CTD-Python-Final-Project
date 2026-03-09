from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load CSV files
hitters = pd.read_csv("hitting_player_stats.csv")
pitchers = pd.read_csv("pitching_player_stats.csv")

#Remove the only 1 row with statistics named "Batting Average *"
print(hitters.info())
rows_to_delete = hitters[hitters["Statistic"] == "Batting Average *"].index
hitters.drop(rows_to_delete, inplace=True)
print(hitters.info())

#Add roles and combine
hitters['Role'] = 'Hitter'
pitchers['Role'] = 'Pitcher'
combined_df = pd.concat([hitters, pitchers], ignore_index=True)

#Get unique statistics and year bounds
statistics = combined_df['Statistic'].dropna().unique()
min_year = combined_df['Year'].min()
max_year = combined_df['Year'].max()

app = Dash(__name__)

#For Render
server = app.server

app.layout = html.Div([
    # Dashboard Header
    html.H1("Historical Baseball League Leaders Dashboard", style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    html.P("Explore historical data of American League hitting and pitching leaders from 1901 to 2024.", 
           style={'textAlign': 'center', 'fontFamily': 'Arial', 'color': '#555'}),
    
    #Dropdown and slider section
    html.Div([
        html.H3("Dashboard Controls", style={'fontFamily': 'Arial'}),
        
        # Dropdown
        html.Label("Select a Statistic:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id="statistics-dropdown",
            options=[{"label": symbol, "value": symbol} for symbol in statistics],
            value="Home Runs",
            style={'marginBottom': '20px'}
        ),
        
        # Range Slider
        html.Div([
            html.Label("Select Year Range:", style={'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='year-slider',
                min=min_year, max=max_year, step=1,
                value=[1990, max_year], 
                marks={int(year): str(year) for year in range(min_year, max_year + 1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'marginBottom': '10px', 'padding': '0 20px'}),
        
    ], style={'padding': '20px', 'backgroundColor': '#e8f4f8', 'borderRadius': '10px', 'marginBottom': '30px'}),

    # Visualizations Section ---
    html.Div([
        dcc.Graph(id="trend-chart"),
        dcc.Graph(id="team-chart"),
        dcc.Graph(id="player-chart")
    ], style={
        'padding': '5%', 
        'backgroundColor': '#f9f9f9', 
        'borderRadius': '10px',
        'display': 'flex',           
        'flexDirection': 'column',   
        'gap': '20px'
    })
], style={'maxWidth': '1200px', 'margin': '0 auto'})

#Callbacks
@app.callback(
    [Output("trend-chart", "figure"),
     Output("team-chart", "figure"),
     Output("player-chart", "figure")],
    [Input("statistics-dropdown", "value"),
     Input("year-slider", "value")]
)
def update_graphs(symbol, year_range):
    #Filter the dataset by the chosen Statistic and Year Range
    start_year, end_year = year_range
    filteredDF = combined_df[
        (combined_df['Statistic'] == symbol) & 
        (combined_df['Year'] >= start_year) & 
        (combined_df['Year'] <= end_year)
    ]
    
    #Trend Line
    #Group by year and get the max value (the ultimate league leader for that year)
    trend_data = filteredDF.groupby('Year', as_index=False)['Value'].max()
    fig_trend = px.line(
        trend_data, x="Year", y="Value", 
        title=f"Evolution of League Leading {symbol} ({start_year} - {end_year})",
        markers=True, labels={'Value': symbol}
    )
    fig_trend.update_traces(line_color='crimson')
    
    #Top Teams
    #Count how many times each team had a leader in the year range chosen by the user.
    team_counts = filteredDF.groupby('Team').size().reset_index(name='Leader_Count')
    team_counts = team_counts.sort_values('Leader_Count', ascending=False).head(10)
    
    fig_teams = px.bar(
        team_counts, x='Team', y='Leader_Count', 
        title=f"Top 10 Teams in {symbol} ({start_year} - {end_year})",
        labels={'Leader_Count': 'Count'},
        color='Leader_Count', color_continuous_scale='Viridis'
    )
    
    #Top 10 Players
    #Count how many times each player led the league in the year range chosen by the user.
    player_counts = filteredDF.groupby('Name').size().reset_index(name='Leader_Count')
    player_counts = player_counts.sort_values('Leader_Count', ascending=False).head(10)
    
    fig_players = px.bar(
        player_counts, x='Leader_Count', y='Name', orientation='h', 
        title=f"Top 10 Players in {symbol} ({start_year} - {end_year})",
        labels={'Leader_Count': 'Count'},
        color='Leader_Count', color_continuous_scale='Magma'
    )
    #Sort horizontal bar
    fig_players.update_layout(yaxis={'categoryorder':'total ascending'}) 
    
    #Return all three figures to the layout
    return fig_trend, fig_teams, fig_players

if __name__ == "__main__":
    app.run(debug=True)
