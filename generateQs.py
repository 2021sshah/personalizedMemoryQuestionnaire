# AUTHOR :: Siddharth Shah 2/25/22

from operator import ge
import sys 
from dataHelper import *
from random import choices, randrange

# Compile dictionaries from dataHelper.py
nameToID, idToInfo = extractDataStructures("info.csv")

# Retrieve dictionary specific to user id
user_id = sys.argv[1] if len(sys.argv) > 1 else "1"
userDct = idToInfo[user_id]

# Retrieve dictionary of all general questions --> answers
numGenQuestions, genQAll = pullGeneralQuestions("general.csv")
genTar = 3

# Randomly select questions to prompt
# genSet = set()
# while len(genSet) < genTar:
#     genSet.add(randrange(numGenQuestions))

questIdxLst = list(genQAll.keys())
genQToAns = {questIdxLst[q]: genQAll[ questIdxLst[q] ] for q in range(numGenQuestions)}

# QUESTIONAIRE PROMPTS
#print(genQToAns)
for ques, ans in genQToAns.items():
    print(ques)
    print(ans)

# Lookup Table of Personal Questions
pTABLE = {
    "age": "How old are you?",
    "job": "What is your current or last job?",
    "color": "What is your favorite color?",
    "movie": "What is your favorite movie?",
    "birthmonth": "In which month were you born?"
}

# Retrieve dictionary of all personal questions
featToAns = {}
for key, val in userDct.items():
    # Naming convention :: personal headers in format "user_detail"
    if "user" not in key: continue
    if "name" in key: continue
    featDetail = key[key.find("_")+1:]
    featToAns[featDetail] = val
numUserFeat = len(featToAns)
#print(featToAns)

# Randomly select questions to prompt
# perTar = 2
# pRandSet = set()
# while(len(pRandSet) < perTar):
#     pRandSet.add(randrange(numUserFeat))

# Convert pRandSet into prompting questions
featArr = list( featToAns.keys() )
perQToAns = {}
for idx in range(numUserFeat):
    specPerFeat = featArr[idx]
    perQToAns[ pTABLE[specPerFeat] ] = featToAns[specPerFeat]

# QUESTIONAIRE PROMPTS
#print(perQToAns)
for ques, ans in perQToAns.items():
    print(ques)
    print(ans)

# Lookup Table of Relational Questions
qTABLE = {
    "relation": "How is [insert] related to you?",
    "age": "How old is [insert]?",
    "job": "What job does [insert] perform?",
    "sport": "What sport does [insert] like to play?",
    "movie": "What is [insert]'s favorite movie?",
}

# Generate relational data structures from user_dct
buck = {}
numToName = {}
for key, val in userDct.items():
    # Naming convention :: relational headers in format "fam#_detail"
    if "fam" not in key: continue
    numStr = key[3: key.find("_")] # gives str representation of number
    detail = key[key.find("_")+1:]  # detail remainder of str
    if numStr not in buck:
        buck[numStr] = {}
    if "name" in key:
        numToName[numStr] = val
    else:
        buck[numStr][detail] = val

# Pull statistics
numRels = len(buck)
numFeatures = len(buck["1"])
totalChoose = numRels*numFeatures
relTar = 5

# Choose random questions for dictionary
# randSet = set()
# while(len(randSet) < relTar):
#     randSet.add(randrange(totalChoose))

# Convert randset into questions dictionary
# relQues = []
# for prop in randSet:
#     specRelBuc = str( (prop//numFeatures)+1 )
#     specFeatNum = prop % numFeatures
#     specFeat = list( buck[specRelBuc].keys() )[specFeatNum]
#     relQues.append( (specRelBuc, specFeat, buck[specRelBuc][specFeat]) )

relQues = []
for i in range(numRels):
    specBuc = str(i+1)
    relFeatLst = list( buck[specBuc].keys() )
    for j in range(numFeatures):
        specFeat = relFeatLst[j]
        relQues.append( (specBuc, specFeat, buck[specBuc][specFeat]) )
#print(relQues) # List of Tuples to iterate over

relQToAns = {}
for famBucIdx, featName, featAns in relQues:
    specName = numToName[famBucIdx]
    quesGenStr = qTABLE[featName]
    nameSpecStr = quesGenStr.replace("[insert]", specName)
    relQToAns[nameSpecStr] = featAns

# QUESTIONAIRE PROMPTS
#print(relQToAns)
for ques, ans in relQToAns.items():
    print(ques)
    print(ans)
print("PLACEHOLDER")
print("PLACEHOLDER")

# Print features for Backend Randomization
print(numGenQuestions)
print(numUserFeat)
print(totalChoose)
sys.stdout.flush() # Send out data

# Merge to full dictionary
# compQToA = {}
# compQToA.update(genQToAns)
# compQToA.update(perQToAns)
# compQToA.update(relQToAns)