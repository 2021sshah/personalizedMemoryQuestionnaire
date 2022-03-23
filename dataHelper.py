# AUTHOR :: Siddharth Shah 2/25/22

import pandas as pd

def pullGeneralQuestions(filename):
    df = pd.read_csv(filename)
    tmpDct = df.to_dict("list")
    qToA = {}
    # Naming convention :: question && answer as column headers
    numQuestions = len( tmpDct["question"] )
    for i in range(numQuestions):
        qToA[ tmpDct["question"][i] ] = tmpDct["answer"][i]
    # print(qToA)
    return numQuestions, qToA

def extractDataStructures(filename):
    # Create DataFrame Object
    df = pd.read_csv(filename,
        dtype = {"subject_id": str, "user_age": str, "fam1_age": str, "fam2_age": str,
                    "fam3_age": str, "fam3_age": str} )
    #print(df.to_string()) 

    # Establish Concrete Data Structures
    tmpDct = df.to_dict("index")
    idToInfo = {} # Dictionary of info dictionaries
    nameToID = {} # Username to subject id dictionary
    for subDct in tmpDct.values():
        # Naming convention :: subject_id && user_name as headers
        idToInfo[ subDct["subject_id"] ] = {}
        nameToID[ subDct["user_name"] ] = subDct["subject_id"]
        for key, val in subDct.items():
            idToInfo[ subDct["subject_id"] ].update( {key:val} )
    return (nameToID, idToInfo)

# for idx, row in df.iterrows():
#     for val in row:
#         print(val)
#     print()