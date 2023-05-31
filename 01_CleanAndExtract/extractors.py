'''
Functions to extract information from HTML
Requires re library
'''

import re

"""
Given the case summary, obtain the case name
Input: text of case summary
Output: case name, plaintiff and defendant
"""
def case_name(case_summary):

    if case_summary is None:
        return None, None, None
    
    pattern = r"\n (.*?) v\. (.*?) \n"
    
    parties = re.search(pattern, case_summary)

    if parties is None:
        return None, None, None

    case_name = parties.group(0).strip()
    plaintiff = parties.group(1).strip()
    defendant = parties.group(2).strip()

    return case_name, plaintiff, defendant

"""
Given the case summary, obtain the judge
Input: text of case summary
Output: judge name
"""
def judge(case_summary):

    if case_summary is None:
        return None
    
    pattern = r"\n The Honorable (.*?), presiding."

    judge = re.search(pattern, case_summary)

    if judge is None:
        return None
    
    judge = judge.group(1).strip()
    
    return judge

"""
Given the text on the parties involved, extract the full plaintiff name
and the attorney for the plaintiff
Input: text of parties and plaintiff of case
Output: corrected plaintiff information and their attorney
"""
def plaintiff_information(parties, plaintiff):

    if parties is None or plaintiff is None:
        return None, None
    
    pattern = "(.*?)" + plaintiff + "(.*?) [\s]{3,} [a-zA-Z]* \n"
    pattern = re.sub("\(", "\(", pattern)
    pattern = re.sub("\)", "\)", pattern)
    
    plaintiff_detail = re.search(pattern, parties)

    if plaintiff_detail is None:
        return None, None
    
    attorney = plaintiff_detail.group(2).strip()
    plaintiff_full = re.sub(attorney, "", plaintiff_detail.group(0).strip()).strip()

    return plaintiff_full, attorney

"""
Given the text on the parties involved, extract the full defendant name
and the attorney for the defendant
Input: text of parties and defendant of case
Output: corrected defendant information and their attorney
"""
def defendant_information(parties, defendant):

    if parties is None or defendant is None:
        return None, None
    
    pattern = "(.*?)" + defendant + "(.*?) [\s]{3,} [a-zA-Z]* \n"
    pattern = re.sub("\(", "\(", pattern)
    pattern = re.sub("\)", "\)", pattern)

    defendant_detail = re.search(pattern, parties)

    if defendant_detail is None:
        return None, None

    attorney = defendant_detail.group(2).strip()
    defendant_full = re.sub(attorney, "", defendant_detail.group(0).strip()).strip()

    return defendant_full, attorney

"""
Counts the number of named defendants in the case
Input: text on the parties involved
Output: how many defendants are named
"""
def num_defendants(parties):
    
    if parties is None:
        return None

    num_defendants = re.findall("Defendant ACTIVE", parties)

    if num_defendants is None:
        return None

    return len(num_defendants)

"""
Extract address of defendant
Input: text of parties and defendant
Output: defendant's address
"""
def defendant_address(parties, defendant):

    if parties is None or defendant is None:
        return None
    
    pattern = defendant + " [\S\s]* NE \d{5} [\s]* \n"
    pattern = re.sub("\(", "\(", pattern)
    pattern = re.sub("\)", "\)", pattern)

    address = re.search(pattern, parties)

    if address is None:
        return None

    address = address.group(0)
    address = re.sub(defendant, "", address).strip()

    address = re.sub(" [\s]{3,}", ", ", address)
    address = address.split(", Defendant ACTIVE, ")[0]

    address = address.split(", owes")[0]

    return address

"""
Filing date of cases
Input: text of case summary
Output: filing date
"""
def filing_date(case_summary):

    if case_summary is None:
        return None
    
    pattern = r"Filed on (.*?) \n"

    filing_date = re.search(pattern, case_summary)

    if filing_date is None:
        return None

    filing_date = filing_date.group(1).strip()
    
    return filing_date

"""
Closing date of cases
Input: text of case summary
Output: closing date
"""
def closing_date(case_summary):

    if case_summary is None:
        return None
    
    pattern = r"This case is Closed as of (.*?) \n"
    
    closing_date = re.search(pattern, case_summary)

    if closing_date is None:
        return None 
    
    closing_date = closing_date.group(1).strip()
    
    return closing_date

"""
How the case was disposed
Input: text of case summary
Output: decision on how the case is disposed
"""
def decision(case_summary):

    if case_summary is None:
        return None

    pattern = r"It was disposed as  (.*?)\n"

    decision = re.search(pattern, case_summary)

    if decision is None:
        return None
    
    decision = decision.group(1).strip()

    return decision


"""
Classification of Case
Input: text of case summary
Output: classification
"""
def classification(case_summary):

    if case_summary is None:
        return None

    pattern = r"Classification: (.*?)\n"

    classification = re.search(pattern, case_summary)

    if classification is None:
        return None
    
    classification = classification.group(1).strip()

    return classification