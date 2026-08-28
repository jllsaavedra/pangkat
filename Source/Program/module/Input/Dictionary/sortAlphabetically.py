import re

# Using readlines()
fileReader = open('NE-ORG.txt', 'r', encoding="utf-8")
lines = fileReader.readlines()
fileWriter = open('NE-ORG-sorted.txt', 'w', encoding="utf-8")
textList = []

# Check for duplicates
for line in lines:
    if re.match(r"\s", line):
        continue
    else:
        if len(textList) == 0:
            textList.append(line.lower().strip())
        else:
            if line.lower().strip() in textList:
                continue
            else:
                textList.append(line.lower().strip())

# Sort the list and store results in a text file
textList.sort()

for text in textList:
    fileWriter.write(text + "\n")

fileReader.close()
fileWriter.close()

