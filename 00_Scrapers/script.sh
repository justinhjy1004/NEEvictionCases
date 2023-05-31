#!/bin/bash

# Create Directories
mkdir -p targeted_scrape
mkdir -p bruteforce_scrape

# Targeted Scrape from the file CourtCaseInfo.csv for 
# Lancaster County from years 2011 to 2012
python3 targeted_scraper.py Lancaster 11 12

# Brute Force Scrape of ALL Civil Court Cases in Lancaster County
# in the year 2021 from Case Number 1 to 15,000
# utilizing 4 cores and save in a separate file every 300 cases
python3 bruteforce_scraper.py Lancaster 21 1 15000 4 300