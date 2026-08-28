# Function for grouping short unit tokens into their longer unit tokens counterpart
# Parameters passed include the tokenList and labelList of the short unit tokens data, and
# the longerTokenList and longerLabelList where the longer unit tokens data are to be stored
def groupLongerTokenUnits(tokenList, labelList, longerTokenList, longerLabelList):

    # Both tokenList and labelList are arrays of arrays. Traversing them requires the outerIndex and innerIndex variables
    outerIndex = 0
    innerIndex = 0
    # Temporary arrays to be appended in longerTokenList and longerLabelList, following the arrays of arrays format
    tempTokenList = []
    tempLabelList = []

    # Traverse each array in tokenList
    while outerIndex < len(tokenList):
        # Traverse each element in the arrays
        while innerIndex < len(tokenList[outerIndex]):
            
            # Longer tokens will be formed by concatenating them together in the token variable 
            token = ""

            # Check if the current token is the beginning of an entity
            if labelList[outerIndex][innerIndex] in ["B-PER", "B-LOC", "B-ORG", "B-MWE"]:
                # Label longer tokens based on their short token label
                match labelList[outerIndex][innerIndex]:
                    case "B-PER":
                        tempLabelList.append("NE-PER")
                    case "B-LOC":
                        tempLabelList.append("NE-LOC")
                    case "B-ORG":
                        tempLabelList.append("NE-ORG")
                    case "B-MWE":
                        tempLabelList.append("MWE")

                # Store the beginning of entity in token
                token = tokenList[outerIndex][innerIndex]
                innerIndex += 1

                # Check if the next token is located at the end of a sentence 
                if innerIndex + 1 == len(tokenList[outerIndex]):
                    # If part/inside of the entity, concatenate to token
                    if labelList[outerIndex][innerIndex] == "I":
                        # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                        if tokenList[outerIndex][innerIndex] in ["-", "/", "'", ")", "]", "}", ".", ":"] or tokenList[outerIndex][innerIndex-1] in ["-", "/", "'", "’", "‘", "″", ":"]:
                            token += tokenList[outerIndex][innerIndex]
                        # Else, include a space character
                        else:
                            token += " " + tokenList[outerIndex][innerIndex]

                        # Append entity to tempTokenList and reset token
                        tempTokenList.append(token)
                        token = ""
                        innerIndex += 1

                    # Else, append entity to tempTokenList, reset token, and append last token as simply a word
                    else:
                        tempTokenList.append(token)
                        token = ""
                        tempTokenList.append(tokenList[outerIndex][innerIndex])
                        tempLabelList.append("W")
                        innerIndex += 1  
                
                # If entity is located at the end of a sentence 
                elif innerIndex == len(tokenList[outerIndex]):
                    tempTokenList.append(token)
                    token = ""  
                    innerIndex += 1

                else:                        
                    # Uncomment to check
                    # print("innerIndex: " + str(innerIndex))
                    # print("length of list: " + str(len(tokenList[outerIndex])))
                    # print(tokenList[outerIndex])

                    # While current token is part/inside of the entity, concatenate it to token
                    while labelList[outerIndex][innerIndex] == "I":
                            # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                        if tokenList[outerIndex][innerIndex] in [".", ",", "-", "/", "'", "’", "‘", "″", ")", "]", "}", ":"] or tokenList[outerIndex][innerIndex-1] in [".", ",", "(", "[", "{", "-", "/", "'", "’", "‘", "″", ":"]:
                        # if (re.search(r"\W", tokenList[outerIndex][innerIndex]) or re.search(r"\W", tokenList[outerIndex][innerIndex-1])):
                            token += tokenList[outerIndex][innerIndex]
                            innerIndex += 1

                            # For detecting the end of array 
                            if innerIndex == len(tokenList[outerIndex]):
                                break
                        
                        # Else, include a space character
                        else:
                            token += " " + tokenList[outerIndex][innerIndex]
                            innerIndex += 1

                            # For detecting the end of array 
                            if innerIndex == len(tokenList[outerIndex]):
                                break
                
                    # Append entity to tempTokenList and reset token
                    tempTokenList.append(token)
                    token = ""

            # Else, current token is simply a word. 
            else:
                tempTokenList.append(tokenList[outerIndex][innerIndex])
                tempLabelList.append("W")
                innerIndex += 1       

        # Store data to their respective arrays and update needed variables 
        longerTokenList.append(tempTokenList)
        longerLabelList.append(tempLabelList)
        tempTokenList = []
        tempLabelList = []
        innerIndex = 0
        outerIndex += 1

    # Uncomment to check
    # print(longerTokenList)
    # print(longerLabelList)