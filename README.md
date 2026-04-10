Cricket Performance Dashboard
An interactive IPL cricket analytics dashboard built with Python and Streamlit. Analyse team performance across venues, years and opponents using real match data.

What It Does
This dashboard takes raw IPL match data and turns it into an interactive visual tool. You can filter by team, venue and year — and every chart, table and metric updates instantly based on your selection.

Features
Team Dashboard

Key metrics — Matches, Wins, Losses, Win Rate, Avg Runs, Avg Strike Rate
Recent match cards showing Opponent, Venue, Runs, Strike Rate, Economy, Wickets and Result
Runs per match bar chart (green = win, red = loss)
Avg runs vs each opponent
Strike rate trend over matches
Win/Loss pie chart
Runs vs Strike Rate scatter plot
Correlation heatmap
Runs distribution histogram

Venue Analysis

Performance stats table by venue
Avg runs by venue
Win rate % by venue
All matches listed for a selected venue
All teams win rate heatmap across every venue

Year Timeline

Click any year to filter
Monthly avg runs trend
Monthly win rate chart
Year on year wins vs losses comparison
Avg runs and strike rate by year (dual axis)
Full match timeline scatter plot

Match Log

Searchable full match table
Head to head record vs every opponent
Win/Loss bar chart per opponent


Tech Stack
ToolPurposePythonCore languageStreamlitWeb app interfacePandasData loading, filtering, aggregationMatplotlibCharts and plotsSeabornHeatmapsNumPyNumerical operations

Dataset
The dataset (data.csv) contains 500 IPL matches across 2024 and 2025 seasons with the following columns:
ColumnDescriptionMatchIDUnique match identifierDateMatch dateTeamBatting teamOpponentOpposition teamVenueStadium / cityRunsTotal runs scoredWicketsWickets lostOversOvers facedStrikeRateBatting strike rateEconomyBowling economyResultWin or Loss
Teams covered: MI, CSK, RCB, KKR, RR, SRH, DC, PBKS
Venues covered: Mumbai, Chennai, Kolkata, Bangalore, Hyderabad, Delhi, Jaipur, Mohali

Project Structure
project/
│
├── app.py          # Main Streamlit dashboard
├── analysis.py     # Standalone analysis and charts script
├── data.csv        # IPL match dataset
└── README.md       # This file

Installation
Step 1 — Clone or download the project folder
Step 2 — Install required libraries
bashpip install streamlit pandas matplotlib seaborn numpy
Step 3 — Run the dashboard
bashpython -m streamlit run app.py
Step 4 — Open in browser
The app will open automatically at:
http://localhost:8501

How To Use

Open the app in your browser
Use the sidebar to select a Team, Venue and Year
Navigate between the four tabs to explore different views
In the Year Timeline tab, click the year buttons to jump between seasons
In the Match Log tab, type an opponent name to search specific matches


Key Insight
The correlation heatmap reveals a -0.73 correlation between Runs and Wickets — the strongest signal in the dataset. Teams that protect their wickets consistently score bigger totals. This is the single most important performance indicator across all 500 matches.
