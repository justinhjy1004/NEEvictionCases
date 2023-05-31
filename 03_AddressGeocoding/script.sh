#!/bin/bash

# Making relevant directories
mkdir -p ../Data/geocoderesult
mkdir -p ../Data/geocode


python3 address.py ../Data/AllEvictionCases.csv

# Take Relevant Columns
python3 relevant_columns.py ../Data/AllEvictionCases.csv

# Split files into 10,000 each, this is to not the make Census angry
split -dl 10000 --additional-suffix=.csv ../Data/geocodable.csv part_  

# Move the split files into the input directory
mv part_* ../Data/geocode

# python3 geocode.py [INPUT DIR] [OUTPUT DIR]
# To request geocoding service file by file
python3 geocode.py ../Data/geocode ../Data/geocoderesult

# Concatenate all files into one
cat ../Data/geocoderesult/*.csv > ../Data/geocoderesult/geocoderesult.csv
# Get the Matches
grep -hr "Exact" ../Data/geocoderesult/geocoderesult.csv > ../Data/geocoderesult/matches.csv
# And the failures
grep -hr "No_Match" ../Data/geocoderesult/geocoderesult.csv > ../Data/geocoderesult/no_match.csv

# Remove placeholding files
rm -r ../Data/geocoderesult
rm -r ../Data/geocode
rm ../Data/geocodable.csv


