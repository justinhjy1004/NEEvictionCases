import re
import pandas as pd

# Function for creating a dictionary of named defendants and 
# their corresponding case ids
def named_defendants(parties):

    pattern = "Defendant (.*?)[\s]{3,}(.*?)[^\S\r\n]{2,}(.*?)\n"
    x = re.findall(pattern, parties)
    all_defendants = [d[1] for d in x]

    return all_defendants

if __name__ == '__main__':

    print("Getting all defendants ...")

    # Load all court cases
    df = pd.read_csv("../Data/AllEvictionCases.csv")

    # Get all of the named defendants on the list
    df["NAMED_DEFENDANTS"] = df["PARTIES"].apply(named_defendants)

    # Subset relevant columns
    defendants = df[["CASE_ID", "NAMED_DEFENDANTS"]]

    # Transform list into named rows
    defendants = defendants.explode("NAMED_DEFENDANTS")

    # Write list of named defendants
    defendants.to_csv("../Data/NamedDefendants.csv", index=None)

    print("Written NamedDefendants.csv!")
