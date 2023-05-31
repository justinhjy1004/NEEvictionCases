"""
Name: Justin Ho
Get defendant's address, specifically, the first named defendant
Then, the address is split into fields for geocoding in terms of
Street, City, ZIP Code and state being NE
"""


import pandas as pd
import sys
import re

"""
Obtain Defendant's Address
Input: Defendant, Attorney and Parties
Output: Defendant's address
"""
def get_address(defendant, defendant_attorney, parties):

    # Flag for attorney
    has_attorney = True

    # Type checking
    if type(defendant) != str:
        return None
    
    if type(defendant_attorney) != str:
        defendant_attorney = ""
        has_attorney = False

    if type(parties) != str:
        return None
    
    try:
        # Base matching format
        pattern = defendant + r"[^\S\r\n]{2,}" + defendant_attorney + r"[\S\s]* NE \d{5}"
        pattern = re.sub("\(", "\(", pattern)
        pattern = re.sub("\)", "\)", pattern)

        x = re.search(pattern, parties)

        # Match on different specifications
        if x is None:
            # Without ZIP Code
            pattern = defendant + "[^\S\r\n]{1,}" + defendant_attorney + "[\S\s]* NE"
            pattern = re.sub("\(", "\(", pattern)
            pattern = re.sub("\)", "\)", pattern)
            
            x = re.search(pattern, parties)

            if x is None:
                # One line address with ZIP
                pattern = defendant + "(.*?) NE \d{5}"
                pattern = re.sub("\(", "\(", pattern)
                pattern = re.sub("\)", "\)", pattern)

                x = re.search(pattern, parties)

                if x is None:
                    # One line address withOUT ZIP
                    pattern = defendant + "(.*?) NE"
                    pattern = re.sub("\(", "\(", pattern)
                    pattern = re.sub("\)", "\)", pattern)


                    x = re.search(pattern, parties)
                    if x is None:
                        return None

        # Remove defendant and attorney from address
        address = x.group(0)

        defendant = re.sub("\(", "\(", defendant)
        defendant = re.sub("\)", "\)", defendant)

        defendant_attorney = re.sub("\(", "\(", defendant_attorney)
        defendant_attorney = re.sub("\)", "\)", defendant_attorney)

        address = re.sub(defendant, "", address).strip()
        address = re.sub(defendant_attorney, "", address).strip()

        # If has attorney, roughly get half
        if has_attorney:
            address = "".join(list(map(get_half,address.split("\n"))))

        address = re.sub("[\\s]{3,}", ", ", address)
    
        address = address.split(", Defendant ACTIVE, ")[0]
        address = address.split(", Witness ACTIVE, ")[0]
        address = address.split(", owes")[0]
        address = address.split(", Limited Representation Attorney")[0]
        
        return address  
    
    except:
        return None

"""
Writing address for normies
Input: address
Output: still address, but for the census
"""
def splitting_field(address):

    if type(address) != str:
        return None, None, None, None

    address = address.split(", ")
    
    if len(address) < 3:
        return None, None, None, None
    
    street = address[0]
    city = address[-2]
    state_zip = address[-1]

    state_zip = state_zip.split(" ")

    if len(state_zip) == 2:
        state = state_zip[0]
        zip = state_zip[1]
    else:
        state = state_zip[0]
        zip = None

    return street, city, state, zip


if __name__ == '__main__':
    file = sys.argv[1]

    df = pd.read_csv(file, encoding='utf-8')

    print("Extracting address information from " + file + "...")

    df["DEFENDANTS_ADDRESS"] = df.apply(lambda x: get_address(x.DEFENDANT, x.DEFENDANT_ATTORNEY, x.PARTIES), axis=1)
    df["STREET"], df["CITY"], df["STATE"], df["ZIP"] = zip(*df["DEFENDANTS_ADDRESS"].apply(splitting_field))
    
    df.to_csv(file, index=None)

    print("Complete and written " + file)