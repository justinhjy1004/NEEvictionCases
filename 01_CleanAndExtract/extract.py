"""
Name: Justin Ho
Given court cases in JSON format, extract relevant information
and save it as a CSV file
"""

from bs4 import BeautifulSoup
import json
import pandas as pd
import sys
import re
import extractors

relevant_panels = ['Case Summary', 'Parties/Attorneys to the Case', 'Judgment Information', 'Register of Actions']

if __name__ == '__main__':

    # Takes the first argument as a json file
    json_file = sys.argv[1]

    with open(json_file) as file:
        data = json.load(file)

    # Creates the list of Case IDs
    case_ids = list(data.keys())
    data_csv = []

    for c in case_ids:
        x = data[c]
        soup = BeautifulSoup(x)
        information = soup.find_all("div", {"class":"panel panel-default"})
        panels = list(map(lambda x: x.find_all("h3"), information))

        panel_titles = list(map(lambda x : re.search(">(.*?)<",str(x)), panels))
        panel_titles = list(map(lambda x : None if (x is None) else x.group(1), panel_titles))
        
        case_information = [c]
        for relevant_panel in relevant_panels:
            try:
                index = panel_titles.index(relevant_panel)
                case_information.append(information[index].find_all("pre")[0].text)
            except ValueError:
                case_information.append(None)
        
        data_csv.append(case_information)

    # Covert data into a DataFrame
    df = pd.DataFrame(data_csv, columns=["CASE_ID", "CASE_SUMMARY", "PARTIES", "JUDGEMENT_INFO", "ACTIONS"])
    df = df[df.CASE_SUMMARY.notna()]
    df = df[df.PARTIES.notna()]
    df = df[df.ACTIONS.notna()]

    # Extract relevant information
    df["CASE_NAME"], df["PLAINTIFF"], df["DEFENDANT"] = zip(*df.CASE_SUMMARY.map(extractors.case_name))
    df["JUDGE"] = df.CASE_SUMMARY.apply(extractors.judge)
    df["CLASSIFICATION"] = df.CASE_SUMMARY.apply(extractors.classification)
    df["PLAINTIFF"], df["PLAINTIFF_ATTORNEY"] = zip(*df.apply(lambda x: extractors.plaintiff_information(x.PARTIES, x.PLAINTIFF), axis=1))
    df["DEFENDANT"], df["DEFENDANT_ATTORNEY"] = zip(*df.apply(lambda x: extractors.defendant_information(x.PARTIES, x.DEFENDANT), axis=1))
    df["NUM_DEFENDANTS"] = df.PARTIES.apply(extractors.num_defendants)
    df["DEFENDANTS_ADDRESS"] = df.apply(lambda x: extractors.defendant_address(x.PARTIES, x.DEFENDANT), axis=1)
    df["FILING_DATE"] = df.CASE_SUMMARY.apply(extractors.filing_date)
    df["CLOSING_DATE"] = df.CASE_SUMMARY.apply(extractors.closing_date)
    df["DECISION"] = df.CASE_SUMMARY.apply(extractors.decision)

    # Write to CSV
    csv_file = re.sub(".json", ".csv", json_file)
    df.to_csv(csv_file, index=False)