import pandas as pd
import numpy as np
import re

def documents(actions):

    pattern = "The document number is (.*?)\n"
    x = re.findall(pattern, actions)
    attached_docs = [d.strip() for d in x]

    return attached_docs

def images(actions):

    pattern = "Image ID (.*?)\n"
    x = re.findall(pattern, actions)
    attached_img = [i.strip() for i in x]

    return attached_img

if __name__ == '__main__':

    print("Getting Attached Documental Evidece...")

    df = pd.read_csv("../Data/AllEvictionCases.csv")

    df["DOCS"] = df["ACTIONS"].apply(documents)
    df["IMG"] = df["ACTIONS"].apply(images)

    # Get Relevant Documents
    docs = df[["CASE_ID", "COURT", "YEAR", "CASE_NUM", "DOCS"]]
    imgs = df[["CASE_ID", "COURT", "YEAR", "CASE_NUM", "IMG"]]

    # Transform list into named rows
    docs = docs.explode("DOCS")
    imgs = imgs.explode("IMG")

    # Write list
    docs.to_csv("../Data/Documents.csv", index=None)
    imgs.to_csv("../Data/Images.csv", index=None)

    print("Wrote the relevant files!")