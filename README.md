# CTD-Python-Final-Project
## Historical Data of American League Hitting and Pitching Players

## Project Summary
This repository contains the extracted data and interactive web dashboard built to analyze historical American League baseball statistics. 

Using Selenium, raw statistical leaderboards for the top hitters and pitchers are scraped directly from the [website](https://www.baseball-almanac.com/yearmenu.shtml), exported to CSV files. This data is then imported into a local SQLite database, establishing a relational structure between the hitter and pitcher table. A custom command-line interface allows users to execute flexible database queries to compare the league's top players. Finally, a fully deployed Dash web application provides users with interactive visualizations—featuring dynamic dropdowns and range sliders—to explore the data.

## Tech Stack
* **Web Scraping:** Python, Selenium WebDriver
* **Data Manipulation & Cleaning:** pandas
* **Database:** SQLite3
* **Visualization & Deployment:** Dash, Plotly, Render

## Setup and Installation

**Prerequisites:**
* Python 3.8 or higher installed on your machine.
* Google Chrome browser (required for the Selenium WebDriver).
* Git installed for cloning the repository.

**Installation Steps:**

1. **Clone the repository:**
   Open your terminal or command prompt and run the following commands:
   ```bash
   git clone [insert_your_github_repo_url_here]
   cd [insert_your_repository_folder_name]
   ```
2. **Create a virtual environment:**
   Keep dependencies isolated by creating a virtual environment:
   ```bash
   python -m venv venv
   ```
3. **Activate the virtual environment:**

   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   source venv\Scripts\activate
   ```
4. **Install the required packages:**
   Install all necessary external libraries using the included requirements file:
   ```bash
   pip install -r requirements.txt
   ```
**How to Run the Programs:**

The files, `hitting_player_stats.csv`, `pitching_player_stats.csv` and `db/baseball.db` are included in this repo for your reference but you can delete them and run the programs below to recreate them.

1. **Web Scraping:**
   ```bash
   python3 scrape.py
   ```
2. **Database Importing:**
   ```bash
   python3 import.py
   ```
3. **Database Querying:**
   ```bash
   python3 query.py
   ```
4. **Interactive Dashboard:**
   ```bash
   python3 app.py
   ```
   Once the server starts, open your web browser and navigate to http://127.0.0.1:8050/ to view the app. Use the dropdowns and sliders to filter the historical data.

   The interactive dashboard has been deployed to the web for public access.
   View the Live App [Here](https://ctd-python-final-project-john-kyaw.onrender.com/)
