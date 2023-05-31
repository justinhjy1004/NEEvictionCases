"""
Author: Justin Ho
Date: May 7 2023

Python script to request the Geocoding service from the Census Bureau
"""

import requests
import sys
from os import listdir

if __name__ == '__main__':
    
    # First command line input is the input directory of split files
    input_directory = "./" + sys.argv[1] + "/"
    # Second for the output directory
    output_directory = "./" + sys.argv[2] + "/"

    # All of the geocodables
    geocodables = listdir(input_directory)

    # Looping for the geocodables
    for geocodable in geocodables:

        print("Starting " + geocodable)

        # Get file and use 2020 Census as benchmark 
        files = {
        'addressFile': open(input_directory + geocodable, 'rb'),
        'benchmark': (None, '2020'),
        }

        # Post Request with given file
        # Obtains the geocoded data in return!
        response = requests.post('https://geocoding.geo.census.gov/geocoder/locations/addressbatch', files=files)

        # Writest to the output directory
        with open(output_directory + geocodable, 'wb') as f:
            f.write(response.content)

        print(geocodable + " done!")