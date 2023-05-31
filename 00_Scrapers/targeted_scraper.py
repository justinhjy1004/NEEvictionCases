"""
Name: Justin Ho
Scraper for court cases given URL access 

This is a targeted scraper
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from credentials import url
from selenium.common.exceptions import TimeoutException
import pandas as pd
import sys
import json

if __name__ == "__main__":

    # Relevant Case Information
    df = pd.read_csv("./CourtCaseInfo.csv")

    county = sys.argv[1]
    start_year = int(sys.argv[2])
    end_year = int(sys.argv[3])

    # Only Douglas
    df = df[(df["COUNTYNAME"] == county)].reset_index()

    browser = webdriver.Chrome("./chromedriver")

    for year in range(start_year, end_year):

        this_year = df[(df["CASEYR"] == year) & (df["COUNTYNAME"] == county)].reset_index()

        print("==============================================================================")
        print("Year: 20" + str(year))

        # Number of cases
        num_obs = len(this_year.index)

        # Empty dictionaries
        scraped_cases = {}

        # For every court case, include a dictionary and its corresponding HTML response
        for i in range(0, num_obs):
            try:
                case_id = this_year.loc[i]["CASETYPE"] + " 0" + str(this_year.loc[i]["COUNTY_NUM"]) + " " + str(this_year.loc[i]["CASEYR"]) + "-" + str(this_year.loc[i]["CASENUM"])

                print(str(i) + " of " + str(num_obs) + " : " + case_id)

                browser.get(url)

                browser.find_element(By.ID, "court_type").send_keys("C")
                browser.find_element(By.ID, "county_num").send_keys(this_year.loc[i]["COUNTYNAME"])
                browser.find_element(By.ID, "case_type").send_keys(this_year.loc[i]["CASETYPE"])
                browser.find_element(By.ID, "case_year").send_keys(str(this_year.loc[i]["CASEYR"]))
                browser.find_element(By.ID, "case_id").send_keys(str(this_year.loc[i]["CASENUM"]))

                browser.find_element(By.ID, "search").click()

                scraped_cases[case_id] = browser.page_source

            except TimeoutException as ex:
                print("Timeout! for " + case_id )

        written_file = str(year) + "_" + county + ".json"

        print("==============================================================================")

        # Write
        with open("./targeted_scrape/" + written_file, "w") as outfile:
            json.dump(scraped_cases, outfile)
