# Function for evaluating the performance of PANG-KAT based on Accuracy, Precision, Recall, and F1-Score
# Parameters passed include the tokens and labels formed through PANG-KAT and their respective, manually-annotated true values
def performanceEvaluationMetrics(tokenList, labelList, trueTokenList, trueLabelList):
    # Initialize variables for traversing the arrays of arrays
    outerIndex = 0
    innerIndex = 0
    errorIndex = 0
    # Initialize counters needed for evaluating performance
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0

    # Successfully labeling entities correctly (based on values of the labels variable) = true positive
    # Successfully labeling non-entities correctly (based on the "O" or "WORD" labels) = true negative
    labels = ["B-PER", "B-LOC", "B-ORG", "B-MWE", "NE-PER", "NE-LOC", "NE-ORG", "MWE", "I",]
    
    # Traverse each array in tokenList
    while outerIndex < len(trueTokenList):
        # Traverse each element in the arrays
        # print(len(trueTokenList[outerIndex]))
        while innerIndex < len(trueTokenList[outerIndex]):

            # Uncomment to check
            # print(tokenList[outerIndex])
            # print(trueTokenList[outerIndex])
            # print((labelList[outerIndex]))
            # print((trueLabelList[outerIndex]))
            # print(errorIndex)
            # print(innerIndex)

            # Check if PANG-KAT correctly identified a token based on its true value
            if tokenList[outerIndex][errorIndex].lower() == trueTokenList[outerIndex][innerIndex].lower():

                # Check if PANG-KAT labelled a token correctly based on its true value
                if labelList[outerIndex][errorIndex] == trueLabelList[outerIndex][innerIndex]:

                    # Increment truePositives when successfully labeling entities
                    if trueLabelList[outerIndex][innerIndex] in labels:
                        truePositives += 1
                    # Increment trueNegatives for successfully detecting outside or word tokens
                    else:
                        trueNegatives += 1

                    innerIndex += 1
                    errorIndex += 1

                # Label mismatch detected! 
                else:
                    # Increment falseNegatives when an entity is labelled as an outside or word token
                    if trueLabelList[outerIndex][innerIndex] in labels and labelList[outerIndex][errorIndex] in ["O", "W"]:
                        falseNegatives += 1

                        # Uncomment to check
                        # print(tokenList[outerIndex])
                        # print(trueTokenList[outerIndex])
                        # print(len(tokenList[outerIndex]))
                        # print(innerIndex)
                        # print('false negative: ' + tokenList[outerIndex][innerIndex] + ": " + trueTokenList[outerIndex][innerIndex])
                        # print('false negative: ' + labelList[outerIndex][innerIndex] + ": " + trueLabelList[outerIndex][innerIndex])
                    
                    else:
                        falsePositives += 1

                        # Uncomment to check
                        # print(tokenList[outerIndex])
                        # print(trueTokenList[outerIndex])
                        # print(len(tokenList[outerIndex]))
                        # print(innerIndex)
                        # print('false positive: ' + tokenList[outerIndex][innerIndex] + ": " + trueTokenList[outerIndex][innerIndex])
                        # print('false positive: ' + labelList[outerIndex][innerIndex] + ": " + trueLabelList[outerIndex][innerIndex])

                    innerIndex += 1
                    errorIndex += 1

            # Token mismatch is detected, could occur due to incorrect labelling
            else:
                if trueLabelList[outerIndex][innerIndex] in labels:
                    # If length of trueToken is greater, PANG-KAT was not able to catch the whole token
                    if len(tokenList[outerIndex][errorIndex]) < len(trueTokenList[outerIndex][innerIndex].lower()):

                        errorTraverser = tokenList[outerIndex][errorIndex].lower()
                        errorIndex += 1

                        # Traverse the improperly labelled tokens to match with trueToken, then increment falseNegatives 
                        while errorTraverser != trueTokenList[outerIndex][innerIndex].lower():
                            
                            # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                            if tokenList[outerIndex][errorIndex] in [".", ",", "-", "/", "'", "’", "‘", "″", ")", "]", "}", ":"] or (errorIndex > 0 and tokenList[outerIndex][errorIndex-1] in [".", ",", "(", "[", "{", "-", "/", "'", "’", "‘", "″", ":"]):
                                errorTraverser += tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1
                            elif errorIndex > 0 and tokenList[outerIndex][errorIndex-1].endswith((".", ",")):
                                errorTraverser += tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1
                            # Else, include a space character
                            else:
                                errorTraverser += " " + tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1

                        falseNegatives += 1
                        innerIndex += 1

                    else:
                        # If length of trueToken is shorter, PANG-KAT possibly overgeneralized a token's label
                        errorTraverser = trueTokenList[outerIndex][innerIndex].lower()
                        innerIndex += 1
                        counter = 1

                        # Traverse the improperly labelled tokens to match with trueToken, then increment falsePositives 
                        while errorTraverser != tokenList[outerIndex][errorIndex].lower():
                            # print(errorTraverser)
                            # print(tokenList[outerIndex][errorIndex].lower())

                            # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                            if trueTokenList[outerIndex][innerIndex] in [".", ",", "-", "/", "'", "’", "‘", "″", ")", "]", "}", ":"] or (innerIndex > 0 and trueTokenList[outerIndex][innerIndex-1] in [".", ",", "(", "[", "{", "-", "/", "'", "’", "‘", "″", ":"]):
                                errorTraverser += trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1
                            elif innerIndex > 0 and trueTokenList[outerIndex][innerIndex-1].endswith((".", ",")):
                                errorTraverser += trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1
                            # Else, include a space character
                            else:
                                errorTraverser += " " + trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1


                        falsePositives += counter
                        errorIndex += 1

                else:
                    # If length of trueToken is shorter, PANG-KAT possibly overgeneralized a token's label
                    if len(tokenList[outerIndex][errorIndex]) > len(trueTokenList[outerIndex][innerIndex].lower()):
                        errorTraverser = trueTokenList[outerIndex][innerIndex].lower()
                        innerIndex += 1
                        counter = 1

                        # Traverse the improperly labelled tokens to match with trueToken, then increment falsePositives 
                        while errorTraverser != tokenList[outerIndex][errorIndex].lower():
                            
                            # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                            if trueTokenList[outerIndex][innerIndex] in [".", ",", "-", "/", "'", "’", "‘", "″", ")", "]", "}"] or (innerIndex > 0 and trueTokenList[outerIndex][innerIndex-1] in [".", ",", "(", "[", "{", "-", "/", "'", "’", "‘", "″"]):
                                errorTraverser += trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1
                            elif innerIndex > 0 and trueTokenList[outerIndex][innerIndex-1].endswith((".", ",")):
                                errorTraverser += trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1
                            # Else, include a space character
                            else:
                                errorTraverser += " " + trueTokenList[outerIndex][innerIndex].lower()
                                counter += 1
                                innerIndex += 1

                        falsePositives += counter
                        errorIndex += 1

                    else:
                        # If length of trueToken is greater, PANG-KAT was not able to catch the whole token
                        errorTraverser = tokenList[outerIndex][errorIndex].lower()
                        errorIndex += 1
                        
                        # Traverse the improperly labelled tokens to match with trueToken, then increment falseNegatives 
                        while errorTraverser != trueTokenList[outerIndex][innerIndex].lower():

                            # If token is not consisting of alphanumeric characters, don't concatenate with a space character 
                            if tokenList[outerIndex][errorIndex] in [".", ",", "-", "/", "'", "’", "‘", "″", ")", "]", "}"] or (errorIndex > 0 and tokenList[outerIndex][errorIndex-1] in [".", ",", "(", "[", "{", "-", "/", "'", "’", "‘", "″"]):
                                errorTraverser += tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1
                            elif errorIndex > 0 and tokenList[outerIndex][errorIndex-1].endswith((".", ",")):
                                errorTraverser += tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1
                            # Else, include a space character
                            else:
                                errorTraverser += " " + tokenList[outerIndex][errorIndex].lower()
                                errorIndex += 1

                        falseNegatives += 1
                        innerIndex += 1

        outerIndex += 1
        innerIndex = 0
        errorIndex = 0

    # Uncomment to check
    # print("\ntruePositives: " + str(truePositives))
    # print("trueNegatives: " + str(trueNegatives))
    # print("falsePositives: " + str(falsePositives))
    # print("falseNegatives: " + str(falseNegatives))

    # Compute for the performance evaluation metric's values based on their respective formulas
    accuracy = (truePositives + trueNegatives) / (truePositives + trueNegatives + falsePositives + falseNegatives)
    precision = truePositives / (truePositives + falsePositives)
    recall = truePositives / (truePositives + falseNegatives)
    F1Score = (2 * precision * recall) / (precision + recall)

    # Return performance evaluation metric's values
    return accuracy, precision, recall, F1Score