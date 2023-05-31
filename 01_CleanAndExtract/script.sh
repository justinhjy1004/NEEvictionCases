#!/bin/bash

# Converts the scraped json files into csv with some relevant 
# information. 
# Utilizes multithreading for performance
ls ../Data/CourtCases/*.json | xargs -P 8 -n 1 python3 extract.py 

# Concatenate the CSV files
# For targeted scrapes
cat ../Data/CourtCases/*_lancaster.csv ../Data/CourtCases/*_douglas.csv > ../Data/targeted_cases.csv
# For brute force scrapes
cat ../Data/CourtCases/*_Lancaster_*.csv ../Data/CourtCases/*_Douglas_*.csv > ../Data/bruteforce_cases.csv

# Clean the bindings
Rscript binders.R

# Further cleans and extract relevant information
# Terrible choice of names in this section but I am sticking with them!
python3 clean.py ../Data/targeted_cases.csv
python3 clean.py ../Data/bruteforce_cases.csv
# Combines both the cleaned sets of data and writing a separate file
# AllEvictionCases.csv
python3 combiner.py

# Remove Placeholder files
rm ../Data/targeted_cases.csv
rm ../Data/bruteforce_cases.csv

