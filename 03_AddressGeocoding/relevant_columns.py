"""
Name: Justin Ho
Get relevant columns for Census Geocoding API
"""

import pandas as pd
import sys

if __name__ == '__main__':
    file = sys.argv[1]

    df = pd.read_csv(file, encoding='utf-8')

    df = df[["CASE_ID", "STREET", "CITY", 'STATE', "ZIP"]]

    df.to_csv("../Data/geocodable.csv", index=None, header=False)