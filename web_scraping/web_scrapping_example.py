# Import required libraries
import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# footbal results
results = []

# define the url base url
url = "https://www.livescore.com/en/football/2021-02-08/"

# Make the request
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.get(url)
time.sleep(3)
page = driver.page_source
driver.quit()

# Process the response and save it as BeautifulSoup object
soup = BeautifulSoup(page, "html.parser")
# Looping all the div tags that have "styled__FootballWrapper-sc-1bf0dw1-1 foNXQM" class
# From the website analysis resulted that the above mentioned class has game data
for match_tag in soup.findAll(
    "div", {"class": "styled__FootballWrapper-sc-1bf0dw1-1 foNXQM"}
):
    # retrive the div that contain actual data
    match_info = match_tag.find_all("span", {"class": "middle"})

    # retrive the home team name
    home_team = match_info[0].find("span", {"class": "team-name"}).string
    # retrive the home team name
    away_team = match_info[0].find("span", {"class": "team-name"}).string

    # retrive the score
    home_team_score = match_info[0].find("span", {"class": "score__home"}).string
    away_team_score = match_info[0].find("span", {"class": "score__away"}).string

    # printing formated info
    print(
        home_team
        + " "
        + home_team_score
        + " - "
        + away_team_score
        + " "
        + away_team
        + "\n"
    )

    # adding info to results
    results.append([home_team, away_team, home_team_score, away_team_score])

with open("footbal.csv", "w", newline="") as f:
    # create the csv writer
    csv_writer = csv.writer(f)
    # write the headers
    csv_writer.writerow(
        ["Home Team", "Away Team", "Home Team Score", "Away Team Score"]
    )
    # add result to the file
    for row in results:
        csv_writer.writerow(row)
