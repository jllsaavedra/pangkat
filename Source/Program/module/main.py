import pangkat

# Initialize PANGKAT, as it is implemented as a Python Class
PANGKAT = pangkat.PANGKAT()

# To use PANGKAT, call its labelTokens function
# Its parameter is the file containing the data to be tokenized
# The labelTokens function returns the arrays of the resulting tokens and their labels
# Results are stored in independent arrays for both short and longer unit tokenization
tokenList, labelList, longerTokenList, longerLabelList = PANGKAT.labelTokens("input.txt")



print("\nShort Unit Tokenization Results: \n")
print(tokenList)
print(labelList)

print("\nLonger Unit Tokenization Results: \n")
print(longerTokenList)
print(str(longerLabelList) + "\n")

