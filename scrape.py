from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Enable headless mode
options.add_argument('--disable-gpu')  # Optional, recommended for Windows
options.add_argument('--window-size=1920x1080')  # Optional, set window size

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)

results = []
year_links = []
hitting_player_stats = []
pitching_player_stats = []
team_standings = []
hitting_team_stats = []
pitching_team_stats = []

#The helper function that grabs the text of the columns in each row and convert them to an object and append in into the target list.
def row_data_grabber(rows, driver, target_list):
    #Keep track of previous column data in the event that the next row does not have the data for that column
    previous_col1 = ''
    previous_col2 = ''
    previous_col3 = ''
    previous_col4 = ''

    for row in rows[2: -2]:
        driver.implicitly_wait(0)

        col1 = row.find_elements(By.CSS_SELECTOR, '.datacolBlue')
        if len(col1) > 0:
            col1_text = col1[0].text
            previous_col1 = col1_text
        else:
            col1_text = previous_col1

        #Unfortunately, col2 and col3 have the same class name.
        col2_3 = row.find_elements(By.CSS_SELECTOR, '.datacolBox')
        col2_only = row.find_elements(By.CSS_SELECTOR, '.datacolBox a')

        #both col2 and 3 available
        if len(col2_3) > 1:
            col2_text = col2_3[0].text
            col3_text = col2_3[1].text
            previous_col2 = col2_text
            previous_col3 = col3_text

        #col2 is available but col3 is not
        if len(col2_3) == 1 and len(col2_only) == 1:
            col2_text = col2_only[0].text
            previous_col2 = col2_text
            col3_text = previous_col3

        #col3 is available but col2 is not
        if len(col2_3) == 1 and len(col2_only) == 0:
            col3_text = col2_3[0].text
            previous_col3 = col3_text        
            col2_text = previous_col2

        col4 = row.find_elements(By.CSS_SELECTOR, '.datacolBoxR')
        if len(col4) > 0:
            col4_text = col4[0].text
            previous_col4 = col4_text
        else:
            col4_text = previous_col4

        each_data_row = {
            "Year" : each_year,
            "Statistic" : col1_text,
            "Name" : col2_text,
            "Team" : col3_text,
            "Value" : col4_text 
        }
        target_list.append(each_data_row)


#The main function
try:
    main_url = "https://www.baseball-almanac.com/yearmenu.shtml"
    driver.get(main_url)
    body = driver.find_element(By.CSS_SELECTOR,'body')

    if body:
        search_results = body.find_elements(By.CSS_SELECTOR, 'table[class="ba-sub"]')
        print(len(search_results))
        american_league = search_results[0]
        years = american_league.find_elements(By.CSS_SELECTOR, 'td[class="datacolBox"] a')
        for year in years[:-1]:
          year_data = {}
          year_url = year.get_attribute('href')
          year_data['year'] = year.text
          year_data['url'] = year_url
          year_links.append(year_data)

    if year_links:
        #Loop thru each year link
        for each_link in year_links:
          each_url = each_link['url']
          each_year = each_link['year']
          driver.get(each_url)
          driver.implicitly_wait(10)
          year_body = driver.find_element(By.CSS_SELECTOR,'body')
          if body:
             tables = driver.find_elements(By.CSS_SELECTOR, '.boxed')
             print(f'Currently scraping the {each_year} page.')

             #Looping thru all 5 tables in each year page
             for each_table in tables:
                rows = each_table.find_elements(By.CSS_SELECTOR, 'tr')

                #Scrape Hitting Player Stats
                if "Hitting Statistics" in rows[0].text and "Player Review" in rows[0].text:
                   row_data_grabber(rows, driver, hitting_player_stats)
                
                #Scrape Pitching Player Stats
                if "Pitching Statistics" in rows[0].text and "Pitcher Review" in rows[0].text:
                    row_data_grabber(rows, driver, pitching_player_stats)
                   

    hitting_player_stats_df = pd.DataFrame(hitting_player_stats)
    pitching_player_stats_df = pd.DataFrame(pitching_player_stats)

    #save as CSV
    hitting_player_stats_df.to_csv('hitting_player_stats.csv')
    pitching_player_stats_df.to_csv('pitching_player_stats.csv')

except Exception as e:
    print("couldn't get the web page")
    print(f"Exception: {type(e).__name__} {e}")
finally:
    driver.quit()
