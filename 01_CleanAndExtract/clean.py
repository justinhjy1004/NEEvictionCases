"""
Name: Justin Ho
Given court cases in JSON format, extract relevant information
and save it as a CSV file
"""


import pandas as pd
import cleaner
import sys
import numpy as np

classification = ["Real", "Chapter"]

if __name__ == '__main__':
    file = sys.argv[1]

    df = pd.read_csv(file, on_bad_lines='skip',encoding='utf-8')

    print("Reading " + file + "...")

    df['flagCol'] = np.where(df["CLASSIFICATION"].str.contains('|'.join(classification)),1,0)
    df = df[df["flagCol"] == 1]
    df = df.drop(['flagCol'], axis=1)

    print("Extracting relevant information...")

    df["COURT"], df["YEAR"], df["CASE_NUM"] = zip(*df.CASE_ID.apply(cleaner.case_information))
    df["JUDGMENT"] = df.JUDGEMENT_INFO.apply(cleaner.judgement_of_restitution)
    df["VACATED_JUDGMENT"] = df.ACTIONS.apply(cleaner.judgement_vacated)
    df["PLAINTIFF"], df["PLAINTIFF_ATTORNEY"] = zip(*df.PARTIES.apply(cleaner.plaintiff_and_attorney))
    df["DEFENDANT"], df["DEFENDANT_ATTORNEY"] = zip(*df.PARTIES.apply(cleaner.defendant_and_attorney))
    df["HAS_LIMITED_REPRESENTATION"], df["LIMITED_REPRESENTATION_STATUS"], df["LIMITED_REP_ATTORNEY"] = zip(*df.apply(lambda x: cleaner.limited_rep_attorney(x.PARTIES, x.ACTIONS), axis=1))
    df["WRIT"] = df.ACTIONS.apply(cleaner.writ_of_restitution)
    df["WRIT_SERVED"], df["WRIT_SERVED_DATE"] = zip(*df.apply(lambda x: cleaner.writ_served(x.WRIT, x.ACTIONS), axis=1))
    df["DISMISSED"], df["DISMISSAL_DATE"] = zip(*df.ACTIONS.apply(cleaner.order_dismissal))
    df["CHANGED_LOCKS"], df["CHANGED_LOCKS_DATE"] = zip(*df.ACTIONS.apply(cleaner.changed_locks))
    df["CONTINUED"] = df.ACTIONS.apply(cleaner.continued)
    df["LIEN"] = df.ACTIONS.apply(cleaner.lien)
    df["GARNISHMENT"] = df.ACTIONS.apply(cleaner.garnishment)
    df["REMAINING_CAUSES"] = df.ACTIONS.apply(cleaner.remaining_causes)
    df["DEFENDANTS_ADDRESS"] = df.apply(lambda x: cleaner.get_address(x.DEFENDANT, x.DEFENDANT_ATTORNEY, x.PARTIES), axis=1)

    df["HEARINGS"] = df["ACTIONS"].apply(cleaner.hearings)
    df["NUM_HEARINGS"] = df["HEARINGS"].apply(lambda x: len(x))
    df["FIRST_HEARING"] = df["HEARINGS"].apply(lambda x: x[-1] if len(x) != 0 else None)

    print("Writing to " + file)

    df.to_csv(file, index=None)

    print("Done cleaning " + file)