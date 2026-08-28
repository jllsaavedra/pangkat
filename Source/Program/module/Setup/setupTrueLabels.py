import re

# Function to set-up the true lables to be used for performance evaluation
# Parameters include the raw trueLabels and the arrays where its tokens and labels are to be stored
def setupTrueLabels (trueLabels, trueTokenList, trueLabelList):
    # Temporary arrays to be appended in trueTokenList and trueLabelList, following the arrays of arrays format
    tokenTempList = []
    labelTempList = []
    
    # Traverse each trueLabel
    for trueLabel in trueLabels:
        # Detecting a new line indicates the end of a sentence
        if re.match(r"\s", trueLabel):
            # Store data to their respective arrays and reset temporary arrays
            trueTokenList.append(tokenTempList)
            trueLabelList.append(labelTempList)

            tokenTempList = []
            labelTempList = []

        # trueLabels are formatted in CSV format: <TOKEN>, <LABEL>
        # Split data and store them in their respective arrays
        else:
            tempList = trueLabel.strip().split(", ")
            # print(tempList)
            tokenTempList.append(tempList[0])
            labelTempList.append(tempList[1])