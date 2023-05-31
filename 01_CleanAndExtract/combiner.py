"""
Name: Justin Ho
Combines the cleaned targeted and brute force scrapes
and removing duplicates in the process
"""

import pandas as pd

if __name__ == '__main__':

    print("Combining targeted and brute force eviction cases...")

    # Load brute force cases
    bruteforce = pd.read_csv("../Data/bruteforce_cases.csv")

    # Load targeted cases
    targeted = pd.read_csv("../Data/targeted_cases.csv")

    # Remove repeated Case IDs
    bruteforce = bruteforce[~bruteforce["CASE_ID"].isin(targeted["CASE_ID"])]

    # Concatenate both dataframes
    all = pd.concat([targeted, bruteforce], axis=0)
    all = all.reset_index().drop("index", axis = 1)

    # Write All Eviction Cases
    all.to_csv("../Data/AllEvictionCases.csv", index=None)

    print("Written AllEvictionCases.csv!")
