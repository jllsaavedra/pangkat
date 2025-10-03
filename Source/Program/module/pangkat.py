# PANG-KAT: A Dedicated Tokenizer for the Tagalog Language
import re

# Class definition of PANG-KAT
class PANGKAT:
    def __init__(self):
        # Initialize the lists for both the short and longer unit tokens and their corresponding labels
        self.tokenList = []
        self.labelList = []
        self.longerTokenList = []
        self.longerLabelList = []
        print("PANGKAT is loaded")
        # print(__file__)

    # Function to set-up the dictionaries for the named entities (NE) and multi-word expressions (MWE)
    # Although it is called dictionaries, they are implemented as arrays for easier traversal of the entities
    # Morever, Python dictionary can't have duplicated keys that conflicts with the data of the NE and MWE dictionaries 
    # Parameters passed include NEs (for the raw list of entities), NEList (where the pre-process entities are to be stored),
    # NECountDict and NEKeysList are additional data for traversing the NEList
    # NECountDict is a Python Dict, holding the starting index of entities in the NEList for each letter of the alphabet.
    # NEKeysList holds the order of keys in NECountDict, crucial when no entity starting of a certain letter exists in the NEList
    def setupDictionaries(self, NEs, NEList, NECountDict, NEKeysList):

        # Initialize needed variables
        index = 0
        count = 0 
        # current holds the starting letter of the current entity
        current = ""

        # Traverse each entities in NEs 
        while index < len(NEs):
            # For the first entity 
            if current == "":
                # Save its starting letter in current, include in NEKeysList, store starting index in NECountDict, and store entity in NEList
                current = NEs[index][0]
                NEKeysList.append(current)
                NECountDict[current] = count
                count += 1
                NEList.append(NEs[index].strip().lower())
                index += 1
            # For detecting the last entity and storing all essential data from it
            elif index == len(NEs) - 1 and current not in NECountDict:
                current = NEs[index][0]
                NEKeysList.append(current)
                NECountDict[current] = count
                NEList.append(NEs[index].strip().lower())
                index += 1
            else:
                # If current entity starts with the current letter stored in current
                if NEs[index][0] == current:
                    count += 1
                    NEList.append(NEs[index].strip().lower())
                    index += 1
                    
                # Else, update based on the new starting letter
                else:
                    current = NEs[index][0]
                    NEKeysList.append(current)
                    NECountDict[current] = count
                    count += 1
                    NEList.append(NEs[index].strip().lower())
                    index += 1

        # For storing the ending index of the last letter saved in NECountDict
        NEKeysList.append("end")
        NECountDict["end"] = count-1

        # Uncomment to check 
        # for keys,values in NECountDict.items():
        #     print(keys + ": " + str(values)) 

        # print(NEList)

    # Function for grouping short unit tokens into their longer unit tokens counterpart
    # Parameters passed include the tokenList and labelList of the short unit tokens data, and
    # the longerTokenList and longerLabelList where the longer unit tokens data are to be stored
    def groupLongerTokenUnits(self, tokenList, labelList, longerTokenList, longerLabelList):

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


    def labelTokens(self, fileName):

        # Open selected file for reading and store data per lines
        fileReader = open(fileName, 'r', encoding="utf-8")
        lines = fileReader.readlines()

        # Beginning markers are common markers located at the beginning of multi-word expressions of both Tagalog and Taglish
        # Multi-word expressions of this format may be written with or without hypen, which is common in colloquial writing
        # (Ex. magpapa-pedicure, magpapa pedicure)
        beginningMarkers = ["mga", "mag", "magka", "magpa", "magkaka", "magpapa", "maka", "makaka", "makapag", "makakapag", "mapag",
                             "nag", "nagka", "nagpa", "nagkaka", "nagpapa", "naka", "napapa", "nakaka", "nakapag", "nakakapag", "napaka", "napag", 
                             "pag", "pagka", "pagpa", "pagkaka", "pagpapa", "paka", "papapa", "pakaka", "pina", "pinag",
                             "ipa", "ipag", "ipinag", "ipinagka", "ipinagpa", "ipinagkaka", "ipinagpapa"]
        conflictingPrefixes = ["na", "ka", "ma", "pa"]
        combinedPrefixes = beginningMarkers + conflictingPrefixes
        # This array includes words which starting syllable can be contracted with an apostrophe
        firstLetterContraction = ["to", "tong", "kong", "ko", "cause", "yon", "yun", "yan", "yong", "yung", "yang", "no", "nong", "pag", "pagkat"]
        # This array includes verbs paired with the contraction of the word not
        contractedNot = ["don", "isn", "aren", "wasn", "weren", "can", "couldn", "won", "wouldn", "shan", "shouldn", "mustn", "mayn", "mightn", "doesn", "didn", "haven", "hasn", "hadn"]
        # This array includes Tagalog time indicators for Tagalog time expressions
        # "hating" and "madaling" refers to the first half of "hating gabi" and "madaling araw"
        tagalogTimeIndicators = ["umaga", "hapon", "tanghali", "gabi", "dapithapon", "hatinggabi", "hating", "madaling"]
        # THis array includes the Tagalog and English names of the days of the week
        daysOfTheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                         "lunes", "martes", "miyerkules", "huwebes", "biyernes", "sabado", "linggo"]

        # File reading of necessary datasets
        fileReaderTitlesStart = open('Dictionary/daglat-titles-start.txt', 'r', encoding="utf-8")
        fileReaderTitlesEnd = open('Dictionary/daglat-titles-end.txt', 'r', encoding="utf-8")
        fileReaderBeModelVers = open('Dictionary/be-modal-verbs.txt', 'r', encoding="utf-8")
        fileReaderMonths = open('Dictionary/daglat-months.txt', 'r', encoding="utf-8")
        personNEDict = open('Dictionary/NE-PER-sorted.txt', 'r', encoding="utf-8")
        locationNEDict = open('Dictionary/NE-LOC-sorted.txt', 'r', encoding="utf-8")
        organizationNEDict = open('Dictionary/NE-ORG-sorted.txt', 'r', encoding="utf-8")
        MWEDict = open('Dictionary/MWE-sorted.txt', 'r', encoding="utf-8")
        
        titlesStart = fileReaderTitlesStart.readlines()
        titlesEnd = fileReaderTitlesEnd.readlines()
        months = fileReaderMonths.readlines()
        personNEs = personNEDict.readlines()
        locationNEs = locationNEDict.readlines()
        organizationNEs = organizationNEDict.readlines()
        MWEs = MWEDict.readlines()
        beModalVerbs = fileReaderBeModelVers.readlines()

        # Initialization of all needed arrays and dictonaries
        titleBeforeList = []
        titleAfterList = []
        monthsList = []
        beModalVerbsList = []

        personNEList = []
        personNECountDict = {}
        personNEKeysList = []

        locationNEList = []
        locationNECountDict = {}
        locationNEKeysList = []

        organizationNEList = []
        organizationNECountDict = {}
        organizationNEKeysList = []

        MWEList = []
        MWECountDict = {}
        MWEKeysList = []

        # Storing data in their respective arrays
        for title in titlesStart:
            titleBeforeList.append(title.strip().lower())

        for title in titlesEnd:
            titleAfterList.append(title.strip().lower())

        for month in months:
            monthsList.append(month.strip().lower())

        for verb in beModalVerbs:
            beModalVerbsList.append(verb.strip().lower())

        # Setting up of the named entities and multi-word expressions dictionaries
        self.setupDictionaries(personNEs, personNEList, personNECountDict, personNEKeysList)
        self.setupDictionaries(locationNEs, locationNEList, locationNECountDict, locationNEKeysList)
        self.setupDictionaries(organizationNEs, organizationNEList, organizationNECountDict, organizationNEKeysList)
        self.setupDictionaries(MWEs, MWEList, MWECountDict, MWEKeysList)

        # Traverse the each line in the selected file, which corresponds to the sentences in the file
        for line in lines:
            
            # Split the sentence into words and punctuations in tokenTempList
            tokenTempList = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", line)
            # Initialize the labelTempList based on the number of tokens in  tokenTempList
            labelTempList = ["O"] * len(tokenTempList)

            # Variable for detecting multiple dashes. Ex: PAG-BA-BAY-BAY
            isDashDetected = False
            # Variable for detecting grouping symbols, such as, (), {}, []
            groupingSymbols = ""
            # Variable for beginning markers + partial reduplication of combined word, no-hyphen
            prefix = ""
            prevPrefix = ""
            # Variable for detecting nicknames enclosed in ""
            beginningQuotesDetected = False

            # Index variable for traversing the tokenTempList
            i = 0

            # Traverse tokenTempList to properly label each of its token
            while i < len(tokenTempList):

                # Uncomment to check
                
                
                

                # Catch beginning markers + partial reduplication of combined word, no-hyphen (Ex. nagma marites)
                # Catches "nag", so we can split "ma" and check if it is a partial reduplication of "marites"
                for marker in beginningMarkers:
                    if tokenTempList[i].lower().startswith(marker):
                        prefix = marker
                        break
                    else:
                        prefix = ""
                        continue

                # Catch beginning markers
                if tokenTempList[i].lower() in beginningMarkers:
                    

                    # Check if within or the start of a MWE
                    if i !=0 and labelTempList[i-1] == "B-MWE":
                        labelTempList[i] = "I"
                    else:    
                        labelTempList[i] = "B-MWE"

                    # Checker for beginning marker + "<WORD/S>" format
                    quoteChecker = -1
                    if tokenTempList[i+1].lower().find('\"') != -1 or tokenTempList[i+1].lower() == '“':
                        quoteChecker = 1

                    # Checker for beginning marker + <WORD>-ng + <WORD> (Ex: mga nagdaang taon)
                    if (i + 1) < len(tokenTempList) and (re.search(r'(ng)$', tokenTempList[i+1].lower())) and (re.search(r'\w', tokenTempList[i+1])):
                        if (re.search(r'(ng)$', tokenTempList[i+1].lower())) and tokenTempList[i].lower() == "mga" and (i + 2) < len(tokenTempList):
                            labelTempList[i+1] = "I"
                            labelTempList[i+2] = "I"
                            i += 2
                        elif (i + 2) < len(tokenTempList) and tokenTempList[i+2].lower() in ["taon"]:
                            labelTempList[i+1] = "I"
                            labelTempList[i+2] = "I"
                            i += 3
                        else:
                            labelTempList[i+1] = "I"
                            i += 1
                    # Checker for beginning marker + partial reduplication of <WORD> + <WORD> (Ex. nag ma marites)
                    elif (i + 2) < len(tokenTempList) and tokenTempList[i+2].startswith(tokenTempList[i+1]):
                        labelTempList[i+1] = "I"
                        labelTempList[i+2] = "I"
                        i += 3
                    # Checker for beginning marker + "<WORD/S>" format
                    elif quoteChecker != -1:

                        labelTempList[i+1] = "I"
                        i += 2
                        isWithinQuotes = True

                        # Label word/s until the closing quotation mark is found
                        while isWithinQuotes == True:
                            if tokenTempList[i].lower().find('\"') != -1 or tokenTempList[i].lower() == '”':
                                isWithinQuotes = False
                            else:
                                labelTempList[i] = "I"
                                i += 1

                        # Label the closing quotation mark
                        labelTempList[i] = "I"
                        i += 1

                    else:
                        labelTempList[i+1] = "I"
                        # Increment with 1 only to check for entities preceeded by preliminary markers
                        # Ex: mga walang hiya
                        i += 1

                # Catching beginning markers + partial reduplication of combined word, no-hyphen (Ex. nagma marites)
                elif (prefix != "" and (re.search(r'\w', tokenTempList[i])) and i+1 < len(tokenTempList) and 
                    tokenTempList[i+1].lower().startswith(tokenTempList[i][len(prefix):]) and len(tokenTempList[i][len(prefix):]) > 1):
                    
                    
                    

                    # Check if start of within an entity (Ex. mga nagma marites)
                    if i !=0 and labelTempList[i-1] == "B-MWE":
                        labelTempList[i] = "I"
                    else:    
                        labelTempList[i] = "B-MWE"
                    labelTempList[i+1] = "I"
                    # prevPrefix is used for checking for named entities preceeded by a prefix
                    prevPrefix = prefix
                    i += 1

                # Check for spelled-out large numbers in Tagalog
                elif (re.search(r'^daa(n)?(ng)?$|^libo(n)?(ng)?$|^raa(n)?(ng)?$|^milyo(n)?(ng)?$|^bilyo(n)?(ng)?$|^trilyo(n)?(ng)?$', tokenTempList[i].lower())):  
                    

                    # Check if detected is a part or the start of a large number
                    # (Ex. limang libo anim na daan at pitumpu't walo)
                    if i > 0 and labelTempList[i-1] == "O":
                        if (i-1) == 0:
                            labelTempList[i-1] = "B-MWE"
                        elif i > 1 and labelTempList[i-2] == "I" and tokenTempList[i-2].lower() == ",":
                            labelTempList[i-1] = "I"
                        else:
                            labelTempList[i-1] = "B-MWE"
                    # Part of a large number
                    elif i > 1 and labelTempList[i-2] in ["B-MWE", "I"]:
                        labelTempList[i-1] = "I"

                    # For catching "daang/raang libo/milyon/bilyon"
                    if tokenTempList[i].lower() in ["daang", "raang"]:
                        labelTempList[i] = "I"
                        i += 1

                    # For catching daang/libong/milyong/bilyong
                    if (re.search(r'(ng)$', tokenTempList[i].lower())):
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 2
                    # The conjuection "na" is often used to indicate numerical classifiers
                    elif tokenTempList[i-1].lower() == "na":
                        # Ex: limang libo anim na daan
                        # Label "anim na daan" based if it is preeceded by a much larger value or not
                        if i - 2 == 0:
                            labelTempList[i-2] = "B-MWE"
                        elif i > 2 and labelTempList[i-3] == "O" :
                            labelTempList[i-2] = "B-MWE"
                        else:
                            labelTempList[i-2] = "I"

                        labelTempList[i-1] = "I"
                        labelTempList[i] = "I"
                        i += 1

                        # Comma may be present to seperate quantities, for better readability
                        if i < len(tokenTempList) and tokenTempList[i].lower() == ",":
                            labelTempList[i] = "I"
                            i += 1
                    else:
                        # For catching daan or libo only
                        labelTempList[i] = "I"
                        i += 1

                        # Comma may be present to seperate quantities, for better readability
                        if i < len(tokenTempList) and tokenTempList[i].lower() == ",":
                            labelTempList[i] = "I"
                            i += 1

                    # Conjunction "at" or its conjuncted form "'t" are used for more specific values
                    # (Ex. dalawang daan at sampu, walong daan at pitumpu’t anim na milyon)
                    if i < len(tokenTempList) and tokenTempList[i].lower() in ["at", "'", "’"]:
                        while True:
                            if i == len(tokenTempList):
                                break
                            else:   
                                # For catching the conjunction "at"
                                if tokenTempList[i].lower() == "at":
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2
                                # For catching the conjuncted form of at
                                elif tokenTempList[i].lower() in ["'", "’"] and tokenTempList[i+1].lower() == "t":
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    labelTempList[i+2] = "I"
                                    i += 3

                                else:
                                    break

                # Check for spelled-out large numbers in English
                elif (re.search(r'^hundred$|^thousand$|^million$|^billion$|^trillion$', tokenTempList[i].lower())): 
                    
                    singleWordNumbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                                         "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
                                         "fourty", "fifty", "sixty", "seventy", "eighty", "ninety"]
                    singleDigitNumbers = singleWordNumbers[0:9]
                    powerOfTens = singleWordNumbers[19:]

                    # Check for numeric form + spelled out numerical classifiers (Ex. P900 million)
                    if i > 0 and (re.search(r'^.?[0-9]+$', tokenTempList[i-1])):
                        # Check if within an entity or the start of an entity
                        if i > 1 and tokenTempList[i-2].lower() in [",", "."] and labelTempList[i-2] == "I":
                            labelTempList[i-1] = "I"
                        else:
                            labelTempList[i-1] = "B-MWE"

                        labelTempList[i] = "I"                        
                        i += 1

                    # Spelled out numbers in English
                    else:
                        # Comma is used to separate values (Ex. six hundred fifty-four thousand, three hundred twenty-one.)
                        if i > 1 and tokenTempList[i-2].lower() == "," and labelTempList[i-2] == "I":
                            labelTempList[i-1] = "I"
                            labelTempList[i] = "I"
                            i += 1
                        # Numbers connected with hyphen are catched by the hyphen rules (Ex. fifty-four thousand)
                        elif i > 1 and tokenTempList[i-2].lower() == "-" and labelTempList[i-1] == "I" and tokenTempList[i-1].lower() in singleWordNumbers:
                            labelTempList[i] = "I"
                            i += 1
                        # Start of an entity
                        else:
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            i += 1

                        # Catch comma used to separate values
                        if tokenTempList[i].lower() == "," and i+1 < len(tokenTempList) and tokenTempList[i+1].lower() in singleWordNumbers:
                            labelTempList[i] = "I"

                        # Catch numbers that are not connected with hyphen (Ex. twenty two)
                        if tokenTempList[i].lower() in powerOfTens:
                            if i+1 < len(tokenTempList) and tokenTempList[i+1].lower() in singleDigitNumbers:
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2
                            else:
                                labelTempList[i] = "I"
                                i += 1
                        # Catch single word numbers (Ex. Sixteen)
                        elif tokenTempList[i].lower() in singleWordNumbers:
                            labelTempList[i] = "I"
                            i += 1
                        # Catch hundred + <another numerical classifier" (Ex: 900,000 -> nine hundred thousand)
                        elif i > 0 and tokenTempList[i-1].lower() == "hundred" and tokenTempList[i].lower() in ["thousand", "million", "billion", "trillion"]:
                            labelTempList[i] = "I"
                            i += 1
                            
                            # Catch comma used to separate values
                            if tokenTempList[i].lower() == "," and i+1 < len(tokenTempList) and tokenTempList[i+1].lower() in singleWordNumbers:
                                labelTempList[i] = "I"

                # To catch Tagalog time expressions in “ala/alas [Spanish-number] ng [Tagalog-time-indicator]” format
                elif i+1 < len(tokenTempList) and tokenTempList[i].lower() in ["ala", "alas"]:
                    
                    # Spanish numbers from 1-12:
                    spanishHours = ["una", "dos", "tres", "kwatro", "kuwatro", "singko", "sais", "syete", "siyete", "otso", "nwebe", "nuwebe", "dyes", "diyes", "onse", "dose"]
                    spanish1to9 = spanishHours[0:9]

                    # If utilizes the dash format (Ex: ala-, alas-)
                    if tokenTempList[i+1].lower() == "-":
                        if i > 0 and tokenTempList[i-1].lower() == "pasado":
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                        else:
                            labelTempList[i] = "B-MWE"

                        labelTempList[i+1] = "I"
                        i += 1

                    # Catching spanish numbers, to assure that it is a time expression (Ex. alas tres)
                    if tokenTempList[i+1] in spanishHours or tokenTempList[i+1].isdigit(): 
                        # Catch "pasado", meaning "past" in "pasado alas dos". Can also be written after the Spanish-number.
                        if i > 0 and tokenTempList[i-1].lower() == "pasado":
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                        elif tokenTempList[i].lower() == "-":
                            labelTempList[i] = "I"
                        else:
                            labelTempList[i] = "B-MWE"
                        
                        labelTempList[i+1] = "I"
                        i += 2

                        # Impunto is used for exact time. (Ex. alas tres impunto for 3:00)
                        if i < len(tokenTempList) and tokenTempList[i].lower() in ["pasado", "impunto"]:
                            labelTempList[i] = "I"
                            i += 1

                        if i+1 < len(tokenTempList) and tokenTempList[i].lower() == ":":
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        
                        # For catching specific time written in Spanish (Ex. alas tres y medya)
                        if i+1 < len(tokenTempList) and tokenTempList[i].lower() == "y":
                            # Spanish numbers above 30 are written with "y" (Ex. treynta y kwatro)
                            # Spelling variations may occur and be written with "'y" (Ex. treynta'y kwatro)
                            if tokenTempList[i+1] in ["treynta", "trenta", "kwarenta", "singkwenta"]:
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2

                                # Catch spelling variation using "'y"
                                if i+1 < len(tokenTempList) and tokenTempList[i].lower() in ["'", "’"] and tokenTempList[i+1].lower() == "y":
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    labelTempList[i+2] = "I"
                                    i += 3
                                # Catch spelling following the Spanish format
                                elif i+1 < len(tokenTempList) and tokenTempList[i].lower() == "y":
                                    labelTempList[i] = "I"
                                    labelTempList[i] = "I"
                                    i += 2
                            
                            # Spanish numbers from 20-29 does not use "y" (Ex. beynte dos, bente dos)
                            elif tokenTempList[i+1].lower() in ["beynte", "bente"]:
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2

                                
                                # Catch numbers from 21-29
                                if i < len(tokenTempList) and tokenTempList[i].lower() in spanish1to9:
                                    labelTempList[i] = "I"
                                    i += 1

                            # Spanish numbers from 16-19 uses the prefix "dyesi-" or its modified "disi-" form in Tagalog (disi-otso)
                            # Spelling variations exist and may also be spelled as one word (Ex. disisyete)
                            elif tokenTempList[i+1].lower() in ["dyesi", "disi"] and i+2 < len(tokenTempList) and tokenTempList[i+2].lower() == "-":
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                labelTempList[i+2] = "I"
                                labelTempList[i+3] = "I"
                                i += 4

                            # Spanish numbers from 1 to 19 written in single words, "medya" is also catched here
                            else:
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2

                        # Time indicators may or may not be connected with "na"
                        if i+1 < len(tokenTempList) and tokenTempList[i].lower() == "na" and tokenTempList[i+1].lower() == "ng":
                            labelTempList[i] = "I"
                            i += 1

                        # Catching Tagalog time indicators, if present or not 
                        if i+1 < len(tokenTempList) and tokenTempList[i].lower() == "ng" and tokenTempList[i+1].lower() in tagalogTimeIndicators:
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"

                            # For catching the second word in "hating gabi" and "madaling araw"
                            if i+2 < len(tokenTempList) and tokenTempList[i+2].lower() in ["gabi", "araw"]:
                                labelTempList[i+2] = "I"
                                i += 3
                            else:
                                i += 2

                        # Abbreviated tagalog time formats
                        elif i+1 < len(tokenTempList) and tokenTempList[i].lower() == "n" and tokenTempList[i+1] == ".":
                            if i+3 < len(tokenTempList) and tokenTempList[i+2].lower() in ["u", "h", "g"] and tokenTempList[i+3] == ".":
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                labelTempList[i+2] = "I"
                                labelTempList[i+3] = "I"
                                i += 4
                            else:
                                i += 1
                    else:
                        i += 1

                # Time format without prefix and minutes (Ex. 9 ng umaga)
                elif tokenTempList[i].isdigit() and i+2 < len(tokenTempList) and tokenTempList[i+1].lower() == "ng" and tokenTempList[i+2].lower() in tagalogTimeIndicators:
                    
                    labelTempList[i] = "B-MWE"
                    labelTempList[i+1] = "I"
                    labelTempList[i+2] = "I"
                    i += 3

                    if i < len(tokenTempList) and tokenTempList[i] in ["araw", "gabi"]:
                        labelTempList[i] = "I"
                        i += 1

                # Catching months without the prefix "ika-" (Ex. sa 15 ng Abril)
                elif tokenTempList[i].lower() in monthsList and i > 1 and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i-2])):
                    
                    if tokenTempList[i-1].lower() == "ng":
                        
                        labelTempList[i-2] = "B-MWE"
                        labelTempList[i-1] = "I"
                        labelTempList[i] = "I"
                        i += 1
                    else:
                        i += 1

                # Catching uses of comma: 
                # (1) connecting titles after name, (2) as a number delimeter and
                # (3) to catch person entities of the format <Surname> , <Name>
                elif tokenTempList[i].lower() == "," and (i+1) < len(tokenTempList):
                    
                    # Catch titles added after a person's name (Ex, <Name> , PhD)
                    if tokenTempList[i+1].lower() in titleAfterList and i > 0 and labelTempList[i-1] in ["I", "B-PER"]:
                        # For the format: <Surname> , <Title>
                        if labelTempList[i-1] == "B-PER":
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        else:
                            iHolder = i - 1
                            # Else, traverse the entity to check if it is a person entity
                            # For format with <Name> <Surname> , <Title>
                            if iHolder == 0 and labelTempList[iHolder] == "B-PER":
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2
                            # Not a valid daglat of titles
                            elif iHolder == 0 and labelTempList[iHolder] != "B-PER":
                                i += 1
                            else:
                                # Traversing the entity
                                while labelTempList[iHolder] == "I":
                                    if iHolder > 0:
                                        iHolder -= 1
                                    else:
                                        break
                            
                                # If inside a person entity, label the comma and title
                                if labelTempList[iHolder] == "B-PER":
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2
                                else:
                                    i += 1

                    # For numbers delimited by comma
                    elif (re.search(r'^(P?[0-9]{1,3})$', tokenTempList[i-1])) and (re.search(r'^([0-9]{1,3})$', tokenTempList[i+1])):
                        if labelTempList[i-1] != "O":
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        else:
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2


                    # Catch Person entities in <Surname> , <First Name> ... format
                    else:
                        
                        # Check if the current word is in the list of Person Entities
                        word = tokenTempList[i+1].lower()
                        firstLetterOfWord = word[0]

                        # To reduce searching time, we only check on the indexes containing entities starting with the first letter of the current word
                        # The starting and ending indexes are stored in the personNECountDict
                        firstLetterStartIndex = personNECountDict.get(firstLetterOfWord, "Not found")
                        if firstLetterStartIndex != "Not found":
                        
                            nextLetterIndex = 0
                            succeddingLetter = ""

                            while nextLetterIndex < len(personNEKeysList):
                                if personNEKeysList[nextLetterIndex] == firstLetterOfWord:
                                    succeddingLetter = personNEKeysList[nextLetterIndex + 1]
                                    break
                                else:
                                    nextLetterIndex += 1
                                    continue
                                    
                            succeddingLetterStartIndex = personNECountDict.get(succeddingLetter, "Not found")

                            if succeddingLetterStartIndex != "Not Found":

                                # Check if the current word exists among the entites in the selected indexes of personNEList
                                while firstLetterStartIndex <= succeddingLetterStartIndex:
                                    entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", personNEList[firstLetterStartIndex])
                                    # If both first and last name matches, label them
                                    if word == entity[0] and entity[-1] == tokenTempList[i-1].lower():
                                        
                                        labelTempList[i-1] = "B-PER"
                                        labelTempList[i] = "I"
                                        labelTempList[i+1] = "I"
                                        
                                        surname = tokenTempList[i-1].lower()
                                        i += 2
                                        
                                        # Check for possible succeeding names for the entity
                                        if len(entity) >= 2 and i != len(tokenTempList):
                                            index = 1
                                            while index < len(entity) and i != len(tokenTempList):
                                                # Check for possible entities with the same first and last name, but different succeeding names
                                                if word == entity[0] and entity[-1] == surname:
                                                    if tokenTempList[i].lower() == entity[index]:
                                                        labelTempList[i] = "I"
                                                        i += 1
                                                        index += 1
                                                    # If succeeding names doesn't match with current entity, check for next entity
                                                    # Entities are sorted alphabetically to reduce searching time
                                                    else:
                                                        firstLetterStartIndex += 1
                                                        if firstLetterStartIndex < succeddingLetterStartIndex:
                                                            entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                        else:
                                                            break
                                                else:
                                                    i += 1
                                                    break

                                            # If no succeeding names found, decrement i to recheck the word for other possible rule match
                                            i -= 1
                                            break
                                            
                                        else:
                                            break
                                    else:
                                        firstLetterStartIndex += 1

                                # If current word != entity, move to next word. Always update i for any rule mismatch
                                i += 1
                            else:
                                i += 1
                        else:
                            i += 1
                            
                # English large numbers, numerical format, separated by spaces (Ex. 9 876 543 210)
                elif (re.search(r'^[0-9]{1,3}$', tokenTempList[i])) and i+1 < len(tokenTempList) and (re.search(r'^[0-9]{1,3}$', tokenTempList[i+1])):
                    
                    # Check if start of entity or inside the entity
                    if labelTempList[i] != "O":
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 1
                    else:
                        labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 1


                # For catching daglat of junior and senior added after a person's name (Ex. Saavedra Jr.)
                elif tokenTempList[i].lower() in ["jr", "sr"]:
                    
                    if i > 0 and labelTempList[i-1] in ["I", "B-PER"]:
                        labelTempList[i] = "I"
                        i += 1

                        if i < len(tokenTempList):
                            # The daglat Jr and Sr may be written with or without periods
                            if tokenTempList[i].lower() == ".":
                                labelTempList[i] = "I"
                                i += 1
                    
                    # The daglar Jr and Sr may be preceeded with a comma after a person's name (Saavedra, Jr.)
                    elif i > 1 and tokenTempList[i-1] == "," and labelTempList[i-2] in ["I", "B-PER"]:
                        labelTempList[i-1] = "I"
                        labelTempList[i] = "I"
                        i += 1

                        if i < len(tokenTempList):
                            # The daglat Jr and Sr may be written with or without periods
                            if tokenTempList[i].lower() == ".":
                                labelTempList[i] = "I"
                                i += 1

                    else:
                        i += 1

                # For catching daglat of Tagalog titles and honorifics placed before a person’s name
                elif tokenTempList[i].lower() in titleBeforeList and (i+2) < len(tokenTempList) and tokenTempList[i+1] == ".":
                    
                    # Multiple titles/honorifics in daglat form
                    if i > 1 and tokenTempList[i-1].lower() == "." and tokenTempList[i-2].lower() in titleBeforeList:
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 2
                    elif i > 0 and tokenTempList[i-1].lower() in ["dating", "former"]:
                        labelTempList[i-1] = "B-PER"
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 2
                    else:
                        # Multiple titles/honorifics, preceeding honorific is not in Daglat
                        backwardTraversal = i-1

                        while labelTempList[backwardTraversal] == "I":
                            if backwardTraversal == 0:
                                break
                            else:
                                backwardTraversal -= 1

                        if labelTempList[backwardTraversal] == "B-PER":
                            labelTempList[i] = "I"
                        elif labelTempList[backwardTraversal] == "B-ORG":
                            labelTempList[backwardTraversal] = "B-PER"
                            labelTempList[i] = "I"  
                        elif labelTempList[backwardTraversal] == "B-LOC":
                            labelTempList[backwardTraversal] = "B-PER"
                            labelTempList[i] = "I" 
                        # Starting titles/honorifics
                        else:
                            labelTempList[i] = "B-PER"

                        labelTempList[i+1] = "I"
                        labelTempList[i+2] = "I"
                        i += 2

                # Daglat with dots per letter
                elif i > 0 and tokenTempList[i] == "." and re.search(r'\b[a-zA-Z]\b', tokenTempList[i-1]):
                    
                    # For catching successive letter with dot. The time indicator a.m. and p.m. is also catched here.
                    if i > 1 and labelTempList[i-2] == "I" and (tokenTempList[i-2] == "." or re.search(r'\d', tokenTempList[i-2])):
                        labelTempList[i-1] = "I"
                        labelTempList[i] = "I"
                        i += 1
                    # Not a daglat
                    elif i > 1 and tokenTempList[i-2] in ["'", "’", "‘"] and tokenTempList[i-1].lower() == "t":
                        i += 1
                   
                    else:
                        # If after a person entity, should be preceeded with a comma
                        if i > 2 and tokenTempList[i-2].lower() == "," and labelTempList[i-3] == "I":
                            labelTempList[i-2] = "I"
                            labelTempList[i-1] = "I"
                        
                        elif i > 1 and re.search(r'\d', tokenTempList[i-2]) and tokenTempList[i-1].lower() in ["p", "a", "n"] and labelTempList[i-2] == "O":
                            labelTempList[i-2] = "B-MWE"
                            labelTempList[i-1] = "I"
                            labelTempList[i] = "I"

                        # Else, an independent daglat
                        else:
                            
                            backwardTraversal = i-2

                            while labelTempList[backwardTraversal] == "I":
                                if backwardTraversal == 0:
                                    break
                                else:
                                    backwardTraversal -= 1
                            
                            # Valid nickname
                            
                            

                            if labelTempList[backwardTraversal] == "B-PER":
                                labelTempList[i-1] = "I"
                            else:
                                labelTempList[i-1] = "B-MWE"
                        
                        labelTempList[i] = "I"
                        i += 1

                # For catching negated english be and model verbs
                elif tokenTempList[i].lower() in beModalVerbsList and tokenTempList[i+1] == "not":
                    
                    labelTempList[i] = "B-MWE"
                    labelTempList[i+1] = "I"
                    i += 2

                # Catching grouping symbols
                elif tokenTempList[i].lower() in ["(", "[", "{"]:
                    
                    groupingSymbols = tokenTempList[i]

                    # Checking if the content refers to an abbreviation of an entity (Ex. (DOH), (OFW))
                    if i > 0 and labelTempList[i-1] in ["B-PER", "B-ORG", "I"]:

                        # Traverse entity to check if it is within a Person entity, Organization entity or not
                        iHolder = i-1
                        if iHolder == 0 and labelTempList[iHolder] in ["B-PER", "B-ORG", "B-LOC", "B-MWE"]:
                            
                            labelTempList[i] = "I"
                            i += 1

                        # Not an abbreviation
                        elif iHolder == 0 and labelTempList[iHolder] not in ["B-PER", "B-ORG", "B-LOC", "B-MWE"]:
                            
                            labelTempList[i] = "B-MWE"
                            i += 1

                        else:
                            # Traverse the entity
                            while labelTempList[iHolder] == "I":
                                if iHolder > 0:
                                    iHolder -= 1
                                else:
                                    break

                            # Label if within a Person/Organization entity
                            if labelTempList[iHolder] in ["B-ORG", "B-LOC", "B-PER"]:
                                labelTempList[i] = "I"
                                i += 1
                            # Within a mathematical equation
                            elif labelTempList[iHolder] == "B-MWE" and i+1 < len(tokenTempList) and (re.search(r'\d|[a-z]{1,2}', tokenTempList[i+1])):
                                labelTempList[i] = "I"
                                i += 1
                            # Preceeded by a beginning marker
                            elif labelTempList[iHolder] == "B-MWE" and tokenTempList[iHolder].lower() in beginningMarkers:
                                labelTempList[i] = "I"
                                i += 1
                            else:
                                labelTempList[i] = "B-MWE"
                                i += 1

                    # Mathematical equation markers
                    elif tokenTempList[i-1].lower() in ["+", "-", "±", "ln", "log", "sqrt"]:
                        labelTempList[i] = "I"
                        i += 1

                    # Independent use of grouping symbols
                    else:
                        labelTempList[i] = "B-MWE"
                        i += 1

                    # Find the closing pair of the detected grouping symbol, label insides
                    match groupingSymbols:
                        case "(":

                            while tokenTempList[i].lower() != ")":
                                labelTempList[i] = "I"
                                i += 1

                        case "[":

                            while tokenTempList[i].lower() != "]":
                                labelTempList[i] = "I"
                                i += 1

                        case "{":

                            while tokenTempList[i].lower() != "}":
                                labelTempList[i] = "I"
                                i += 1

                    # Label the closing pair
                    labelTempList[i] = "I"
                    i += 1

                # Catching English date formats
                elif tokenTempList[i].lower() in monthsList and (i+1) < len(tokenTempList) and (re.search(r'\d', tokenTempList[i+1]) or tokenTempList[i+1] == "."):
                    
                    daglatMonths = monthsList[0:20]

                    # DAY-MONTH (Ex: 15 April, 15 Apr.)
                    if (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i-1])):
                        labelTempList[i-1] = "B-MWE"
                        labelTempList[i] = "I"
                        i += 1
                        
                        if i < len(tokenTempList) and tokenTempList[i-1].lower() in daglatMonths and tokenTempList[i] == ".":
                            labelTempList[i] = "I"
                            i += 1


                    # ABBREVIATED MONTH.-DAY (Ex: Apr. 15,)
                    elif (i+1) < len(tokenTempList) and tokenTempList[i+1] == "." and tokenTempList[i].lower() in daglatMonths:
                        if (i+2) < len(tokenTempList) and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i+2])):
                            if i > 1 and tokenTempList[i-2].lower() in daysOfTheWeek and labelTempList[i-2] == "B-MWE":
                                labelTempList[i] = "I"
                            else:
                                labelTempList[i] = "B-MWE"

                            labelTempList[i+1] = "I"
                            labelTempList[i+2] = "I"
                            i += 3

                            if i < len(tokenTempList) and tokenTempList[i] == "," and re.search(r'\b[0-9]{4}\b', tokenTempList[i+1]):
                                labelTempList[i] = "I"
                                i += 1

                        # Catching months without the prefix "ika-" + abbreviated month (Ex. sa 15 ng Apr.)
                        elif i > 1 and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i-2])):
                            if tokenTempList[i-1].lower() == "ng":
                                # 
                                labelTempList[i-2] = "B-MWE"
                                labelTempList[i-1] = "I"
                                labelTempList[i] = "I"
                                i += 1
                                
                                if i < len(tokenTempList) and tokenTempList[i] == "." and tokenTempList[i-1].lower() in daglatMonths:
                                    labelTempList[i] = "I"
                                    
                                    i += 1

                            else:
                                i += 1
                        else:
                            i += 1
                    
                    # MONTH-DAY (Ex. April 15, )
                    elif (i+1) < len(tokenTempList) and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i+1])):
                        if i > 1 and tokenTempList[i-2].lower() in daysOfTheWeek and labelTempList[i-2] == "B-MWE":
                            labelTempList[i] = "I"
                        else:
                            labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 2

                        if i < len(tokenTempList) and tokenTempList[i] == "," and re.search(r'\b[0-9]{4}\b', tokenTempList[i+1]):
                            labelTempList[i] = "I"
                            i += 1
                    
                    # MONTH-YEAR only (April 2025)
                    elif (i+1) < len(tokenTempList) and (re.search(r'\b[0-9]{4}\b', tokenTempList[i+1])):
                        if i > 1 and tokenTempList[i-2].lower() in daysOfTheWeek and labelTempList[i-2] == "B-MWE":
                            labelTempList[i] = "I"
                        else:
                            labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 2

                    # Not a valid month format
                    else:
                        i += 1

                    # For catching year, when present
                    if i < len(tokenTempList) and (re.search(r'\b[0-9]{4}\b', tokenTempList[i])):
                        labelTempList[i] = "I"
                        i += 1

                # English 12-hr clock system, no minutes (Ex: 3 PM)
                elif tokenTempList[i].lower() in ["am", "pm"] and (re.search(r'\d', tokenTempList[i-1])):
                    
                    if labelTempList[i-2] != "O":
                        labelTempList[i-1] = "I"
                    else:
                        labelTempList[i-1] = "B-MWE"

                    labelTempList[i] = "I"
                    i += 1

                # To catch contracted "hindi" and "huwag" written with apostrophe
                # However, we only increment once to check for entities that starts with "di" and "wag"
                elif tokenTempList[i].lower() in ["'", "’", "‘"] and tokenTempList[i+1].lower() in ["di", "wag"]:
                    
                    labelTempList[i] = "B-MWE"
                    labelTempList[i+1] = "I"
                    i += 1

                # Catching contractions and other applications of apostrophe
                elif tokenTempList[i].lower() in ["'", "’", "‘", "″"]:
                    
                    # Contracted year and height (Example: 2024 -> '24)
                    if i+1 < len(tokenTempList) and (re.search(r'\d', tokenTempList[i+1])):
                        # Height: 5'0
                        if i != 0 and (re.search(r'\d', tokenTempList[i-1])) and labelTempList[i-1] == "O":
                            
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        # Contracted year as part of other entity
                        elif labelTempList[i-1] in ["B-PER", "B-LOC", "B-ORG", "B-MWE", "I"]:
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        # Contracted year
                        else:                            
                            labelTempList[i] = "B-MWE"
                            labelTempList[i+1] = "I"
                            i += 2

                    # Catching Spanish numbers' spelling variation that uses "'y" (Ex. trenta'y dos)
                    elif i > 0 and tokenTempList[i-1] in ["treynta", "trenta", "kwarenta", "singkwenta", "sisenta", "sitenta", "otsenta", "nobenta"]:
                        if i + 1 < len(tokenTempList) and tokenTempList [i+1].lower() == "y":
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            labelTempList[i+2] = "I"
                            i += 3
                                    
                        else:
                            i += 1

                    # Catching words with contracted first sylabble (Ex: ito -> 'to, iyon -> 'yon)
                    elif i+1 < len(tokenTempList) and tokenTempList[i+1].lower() in firstLetterContraction:
                        # To catch: nito -> n'to, niyo -> n'yo, mga ito -> mga 'to, 
                        if i != 0 and tokenTempList[i-1].lower() in ["n", "mga"]:
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        # Words with contracted first sylabble
                        else:
                            labelTempList[i] = "B-MWE"
                            labelTempList[i+1] = "I"
                            i += 2

                    # Other contractions
                    else:
                        if i+1 < len(tokenTempList) and (re.search(r'\w', tokenTempList[i-1])) and (re.search(r'\w', tokenTempList[i+1])):
                            # Check if part of another entity
                            if labelTempList[i-1] not in ["B-PER", "B-LOC", "B-ORG", "B-MWE", "I"]:
                                labelTempList[i-1] = "B-MWE"
                            elif tokenTempList[i-1].lower() in contractedNot:
                                labelTempList[i-1] = "B-MWE"

                            labelTempList[i] = "I"
                            
                            # Catch contracted "at" and "not"
                            if tokenTempList[i+1].lower() == "t" and tokenTempList[i-1].lower() not in contractedNot:
                                labelTempList[i+1] = "I"

                                # Catch when the next word ends with -ng, connecting another word
                                if i+2 < len(tokenTempList) and (re.search(r'(ng)$', tokenTempList[i+2].lower())):
                                    labelTempList[i+2] = "I"
                                    labelTempList[i+3] = "I"
                                    i += 4
                                else:
                                    labelTempList[i+2] = "I"
                                    i += 3

                            # Contracted "not"
                            else:
                                labelTempList[i+1] = "I"
                                i += 2
                        else:
                            i += 1

                # Catching multi-word expressions connected by dash and slash
                elif i != 0 and i+1 < len(tokenTempList) and tokenTempList[i].lower() == "-" or tokenTempList[i].lower() == "/":
                    
                    if (re.search(r"\w", tokenTempList[i-1].lower()) or tokenTempList[i-1].lower() == ")") and re.search(r"\w", tokenTempList[i+1].lower()):
                        # For labelling entities connected by dash or slash
                        if isDashDetected == False and labelTempList[i-1] not in ["I", "B-PER", "B-ORG", "B-LOC"]:
                            if tokenTempList[i-1].lower() in ["tga", "taga"]:
                                labelTempList[i-1] = "B-LOC"
                            else:
                                labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"

                        # For labelling consecutive dashes or slashes in an expression
                        else:
                            labelTempList[i] = "I"
                            
                        if re.search(r'(ed)$', tokenTempList[i+1].lower()):
                            labelTempList[i+1] = "I" 
                            labelTempList[i+2] = "I"
                            i += 2
                        else:
                            labelTempList[i+1] = "I"
                            i += 1

                        # For catching consecutive uses of dashes, slashes, and certain date and time formats
                        if i+1 < len(tokenTempList) and tokenTempList[i+1] in ["-", "/", "ng", ":"]:
                            i += 1

                            if i != len(tokenTempList):
                                if tokenTempList[i].lower() == "-" or tokenTempList[i].lower() == "/":
                                    isDashDetected = True

                                # Catch date and time expressions using the prefix "ika-" and "a-""
                                elif tokenTempList[i] == "ng":
                                    

                                    # Catching month for date expressions and Tagalog time indicators for time expressions
                                    if tokenTempList[i+1].lower() in monthsList or tokenTempList[i+1] in tagalogTimeIndicators:
                                        labelTempList[i] = "I"
                                        labelTempList[i+1] = "I"

                                        # For catching the second word in "hating gabi" and "madaling araw"
                                        if i+2 < len(tokenTempList) and tokenTempList[i+2].lower() in ["gabi", "araw"]:
                                            labelTempList[i+2] = "I"
                                            i += 3
                                        else:
                                            i += 2
                                    else:
                                        i += 1

                                # Catching time expressions of English XX:XX - XX:XX AM/PM format
                                elif tokenTempList[i] == ":":
                                    
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2

                                    # For catching English time indicators, if present or not
                                    if tokenTempList[i].lower() in ["am", "pm"]:
                                        labelTempList[i] = "I"
                                        i += 1
                                    # For catching Tagalog time indicators, if present or not
                                    elif tokenTempList[i].lower() == "ng" and i+1 < len(tokenTempList) and tokenTempList[i+1] in tagalogTimeIndicators:
                                        labelTempList[i] = "I"
                                        labelTempList[i+1] = "I"
                                        i += 2

                                        if i < len(tokenTempList) and tokenTempList[i].lower() in ["gabi", "araw"]:
                                            labelTempList[i] = "I"
                                            i += 1  
                                else:
                                    isDashDetected = False
                            else:
                                isDashDetected = False
                        else:
                            isDashDetected = False

                    # Catching subtraction and division
                    elif (tokenTempList[i].lower() in ["-", "/"] and (re.search(r'\d|^[a-z]{1,2}$|\(', tokenTempList[i+1])) and (re.search(r'\d|^[a-z]{1,2}$|\)', tokenTempList[i-1]))):

                        if tokenTempList[i+1] == "(" and tokenTempList[i-1] == ")":
                            labelTempList[i] = "I"
                            i += 1
                        else:
                            if labelTempList[i-1] == "I":
                                labelTempList[i-1] = "I"
                            else:
                                labelTempList[i-1] = "B-MWE"

                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                    else:
                        i += 1

                # For catching the use of percentage
                elif tokenTempList[i].lower() in ["%", "porsiyento", "porsyento", "percent"] and tokenTempList[i-1].isdigit():
                    
                    if labelTempList[i-1] != "I":
                        labelTempList[i-1] = "B-MWE"
                    
                    labelTempList[i] = "I"
                    i += 1

                # For catching the use of degrees
                elif tokenTempList[i].lower() in ["°", "º"] and tokenTempList[i-1].isdigit():
                    
                    labelTempList[i-1] = "B-MWE"
                    labelTempList[i] = "I"
                    labelTempList[i+1] = "I"
                    i += 2

                # Catching basic math operations
                elif (tokenTempList[i].lower() in ["+", "x", "=", "^"] and (i+1) < len(tokenTempList) and
                     (re.search(r'\d|^[a-z]{1,2}$|\(', tokenTempList[i+1])) and (re.search(r'\d|^[a-z]{1,2}$|\)', tokenTempList[i-1]))):
                    

                    if labelTempList[i-1] == "I":
                        labelTempList[i-1] = "I"
                    else:
                        labelTempList[i-1] = "B-MWE"

                    labelTempList[i] = "I"
                    labelTempList[i+1] = "I"
                    i += 2
                    
                    # Catching symbols before number (Ex. -4, ln 4)
                    if (i < len(tokenTempList) and tokenTempList[i-1].lower() in ["+", "-", "±", "ln", "log", "sqrt", "√"] and (re.search(r'\d|^[a-z]{1,2}$|', tokenTempList[i]))):
                        labelTempList[i] = "I"
                        i += 1

                # Catching basic math operations, symbols before number (Ex. ±4, log 10)
                elif (tokenTempList[i].lower() in ["+", "-", "±", "ln", "log", "sqrt", "√"] and (i+1) < len(tokenTempList) 
                      and (re.search(r'\d|^[a-z]{1,2}$|\(', tokenTempList[i+1]))):
                    
                    
                    if i > 0 and labelTempList[i-1] == "I":
                        labelTempList[i] = "I"
                    else:
                        labelTempList[i] = "B-MWE"

                    labelTempList[i+1] = "I"

                    if tokenTempList[i+1] == "(":
                        i += 1
                    else:
                        i += 2

                # Catching basic math operations, symbols after number (Ex. 160 x 25%, 8″ x 5″)
                elif tokenTempList[i].lower() in ["+", "-", "x", "/"] and tokenTempList[i-1].lower() in ["″", "%"]:
                    
                    
                    if labelTempList[i-1] == "I":
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 2

                elif (i+1) <= len(tokenTempList):
                    # For catching nicknames enclosed in ""
                    quoteChecker = tokenTempList[i].lower().find('\"')

                    # For catching repeated words with added infix
                    infixInIndex = tokenTempList[i].lower().find("in")
                    infixUmIndex = tokenTempList[i].lower().find("um")
                    tokenWithoutInfix = ""

                    # 
                    # 

                    # Remove the infix and save the root word in the tokenWithoutInfix variable
                    if infixInIndex != -1 or infixUmIndex != -1:
                        if infixInIndex != -1:
                            prevString = tokenTempList[i][0:infixInIndex].lower()
                            nextString = tokenTempList[i][(infixInIndex + 2):].lower()
                            tokenWithoutInfix = prevString + nextString
                            
                        elif infixUmIndex != -1:
                            prevString = tokenTempList[i][0:infixUmIndex].lower()
                            nextString = tokenTempList[i][(infixUmIndex + 2):].lower()
                            tokenWithoutInfix = prevString + nextString
                            

                    # For checking for intensified words (connected by "-ng") and plain repeating words (Ex. gaya gaya)
                    # Check if current word starts with the next word
                    if (i+1) < len(tokenTempList) and tokenTempList[i].lower().startswith(tokenTempList[i+1].lower()) and re.search(r"\w", tokenTempList[i].lower()) and len (tokenTempList[i+1]) > 2:
                        

                        # To catch exaggerations connected by "-ng" (Ex: magandang maganda)
                        if (re.search(r'(ng)$', tokenTempList[i].lower()) and (tokenTempList[i][:(len(tokenTempList[i])-2)].lower() == tokenTempList[i+1].lower() or 
                            tokenTempList[i][:(len(tokenTempList[i])-1)].lower() == tokenTempList[i+1].lower())):
                            
                            labelTempList[i] = "B-MWE"
                            labelTempList[i+1] = "I"
                            i += 2
                        
                        # Plain repeating words
                        elif tokenTempList[i].lower() == tokenTempList[i+1].lower():
                            #  To avoid labelling subsequent "na". For instance in: "alam ko na na ganon talaga"
                            if tokenTempList[i].lower() != "na":
                                #  To catch phrases that make sense with "ang" or pa. 
                                #  Ex: ang ganda ganda, pa bago bago
                                if i > 0 and tokenTempList[i-1].lower() in ["ang", "pa",]:
                                    labelTempList[i-1] = "B-MWE"
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2
                                # Plain repeating words
                                else:
                                    if i > 0 and tokenTempList[i-1].lower() != "-":
                                        labelTempList[i] = "B-MWE"
                                    elif i == 0:
                                        labelTempList[i] = "B-MWE"
                                    else:
                                        labelTempList[i] = "I"

                                    labelTempList[i+1] = "I"
                                    i += 2

                            # No match = go to next word
                            else:
                                i += 1
                        # No match = go to next word
                        else:
                            i += 1

                    # Repeating words with partial reduplication (Ex. kani kanila)
                    # Check length of first word to avoid conflicting particles (Ex. "na naliligo" should not be labeled)
                    elif (i+1) < len(tokenTempList) and tokenTempList[i].lower() == tokenTempList[i+1][:len(tokenTempList[i])].lower() and len(tokenTempList[i].lower()) > 3:
                        

                        # 
                        labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 2

                    # Repeating words with added prefix. (Ex: magtuloy tuloy, mabago bago, kaproud proud, mamali mali, tatanga tanga)
                    # Check if current word ends with next word
                    elif ((i+1) < len(tokenTempList) and tokenTempList[i].lower().endswith(tokenTempList[i+1].lower()) and re.search(r"\w", tokenTempList[i].lower()) and len (tokenTempList[i+1]) > 2 and
                            (tokenTempList[i][0:2].lower() == tokenTempList[i+1][0:2].lower() or tokenTempList[i][:(len(tokenTempList[i]) - len(tokenTempList[i+1]))].lower() in combinedPrefixes or 
                            tokenTempList[i][:(len(tokenTempList[i]) - len(tokenTempList[i+1]))].lower() in (s + tokenTempList[i+1][0:2].lower() for s in combinedPrefixes) )):
                        
                        
                        # When the prefix is written with space following the repeated word and was detected as a preliminary marker (Ex: mag tutuloy tuloy)
                        # Plural repeating nouns are also labelled here. (Ex. mga nagloloko loko)
                        if i > 0 and labelTempList[i-1] == "B-MWE":
                            labelTempList[i] = "I"
                        else:
                            
                            labelTempList[i] = "B-MWE"

                        labelTempList[i+1] = "I"
                        i += 2
                    
                    # For checking for intensified words (connected by "na" and "at")
                    # For checking for continuity of action, based on "nang"
                    # For checking for the use of the preposition "to" in this format: <WORD> to <SAME WORD>
                    elif (i+1) < len(tokenTempList) and tokenTempList[i] in ["na", "nang", "to", "at"] and tokenTempList[i-1].lower() == tokenTempList[i+1].lower() and re.search(r'\w', tokenTempList[i-1]):
                        

                        labelTempList[i-1] = "B-MWE"
                        labelTempList[i] = "I"
                        labelTempList[i+1] = "I"
                        i += 2

                    # Repeating words with added infix. (Ex: tumalon talon, pumunta punta, tinali tali)
                    elif (i+1) < len(tokenTempList) and tokenWithoutInfix != "" and tokenWithoutInfix == tokenTempList[i+1].lower():
                        

                        labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 2

                    # Repeating words that ends with "ng" (Ex. marami raming)
                    elif (i > 0 and re.search(r'(ng)$', tokenTempList[i].lower()) and 
                        tokenTempList[i][:(len(tokenTempList[i])-2)].lower() == tokenTempList[i-1][len(tokenTempList[i-1])-len(tokenTempList[i][:(len(tokenTempList[i])-2)]):].lower() and
                        len(tokenTempList[i][:(len(tokenTempList[i])-2)]) > 2 and len(tokenTempList[i-1][len(tokenTempList[i-1])-len(tokenTempList[i][:(len(tokenTempList[i])-2)]):]) > 2):
                        
                        
                        # 
                        # 
                        
                        labelTempList[i-1] = "B-MWE"
                        labelTempList[i] = "I"
                        i += 1
                    
                    # Catching the use of Spanish "y" in connecting maternal's surname in one's full name
                    # Catching independent use of Spanish numbers from 30 - 99
                    elif (i+1) < len(tokenTempList) and tokenTempList[i].lower() == "y":
                        
                        
                        # The beginning word of Spanish numbers from 30 to 99
                        spanish30to99Beginning = ["treynta", "trenta", "kwarenta", "singkwenta", "sisenta", "sitenta", "otsenta", "nobenta"]

                        # Spanish "y" in connecting maternal surname
                        if i > 0 and labelTempList[i-1] in ["B-PER", "I"]:

                            # Traverse entity to check if it is within a Person entity or not
                            iHolder = i-1
                            if iHolder == 0 and labelTempList[iHolder] == "B-PER":
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2

                            # Not a valid use of Spanish "y"
                            elif iHolder == 0 and labelTempList[iHolder] != "B-PER":
                                i += 1

                            else:
                                # Traverse the entity
                                while labelTempList[iHolder] == "I":
                                    if iHolder > 0:
                                        iHolder -= 1
                                    else:
                                        break

                                # Label if within a Person entity
                                if labelTempList[iHolder] == "B-PER":
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2
                                else:
                                    i += 1

                        # Independent use of Spanish numbers
                        elif tokenTempList[i+1].lower() in ["uno", "dos", "tres", "kwatro", "singko", "sais", "syete", "otso", "nwebe"]:
                            # Standard Spanish spelling using "y" (Ex. trenta y dos)
                            if i > 0 and tokenTempList[i-1].lower() in spanish30to99Beginning:
                                labelTempList[i-1] = "B-MWE"
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2

                        else:
                            i += 1

                    # Catching Tagalog numbers from 11-19 (Ex. labing apat)
                    elif (i+1) < len(tokenTempList) and (re.search(r'^labing$|^beynte$|^bente$', tokenTempList[i].lower())):  
                        
                        
                        if i > 0 and tokenTempList[i-1].lower == "at" and labelTempList[i-1] == "I":
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        else:
                            labelTempList[i] = "B-MWE"
                            labelTempList[i+1] = "I"
                            i += 2

                    # English 12-hr clock system with minutes (Ex. 9:30 ng umaga, 9:30 AM)
                    elif (i+1) < len(tokenTempList) and tokenTempList[i].lower() == ":":
                        

                        if (re.search(r'\d', tokenTempList[i-1])) and (re.search(r'\d', tokenTempList[i+1])):
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2

                            if i < len(tokenTempList):
                                # English abbreviated time indicators
                                if tokenTempList[i].lower() in ["am", "pm"]:
                                    labelTempList[i] = "I"
                                    i += 1

                                # Catching Tagalog time indicators
                                elif tokenTempList[i].lower() == "ng" and i+1 < len(tokenTempList) and tokenTempList[i+1].lower() in tagalogTimeIndicators:
                                    labelTempList[i] = "I"
                                    labelTempList[i+1] = "I"
                                    i += 2

                                    if i < len(tokenTempList) and tokenTempList[i].lower() in ["gabi", "araw"]:
                                        labelTempList[i] = "I"
                                        i += 1

                                # For catching XX:XX - XX:XX formats
                                elif tokenTempList[i].lower() == "-":
                                    
                                    isDashDetected = True
                                    i = i
                        else:
                            i += 1

                    # Catching decimal numbers and daglat of specific location markers
                    elif (i+1) < len(tokenTempList) and tokenTempList[i] == ".":
                        
                        
                        # Decimal numbers
                        if i > 0 and re.search(r'^.?[0-9]+$', tokenTempList[i-1]) and tokenTempList[i+1].isdigit():
                            labelTempList[i-1] = "B-MWE"
                            labelTempList[i] = "I"
                            labelTempList[i+1] = "I"
                            i += 2
                        # Daglat of location markers
                        elif i > 0 and tokenTempList[i-1].lower() in ["brgy", "bgy", "blk", "prk", "subd", "cpd", "ave", "blvd", "hiway", "hwy"]:
                            if i > 1 and labelTempList[i-2] == "I":
                              labelTempList[i-1] = "I"  
                            else:
                                labelTempList[i-1] = "B-LOC"
                            labelTempList[i] = "I"
                            i += 1
                        else:
                            i += 1

                    # Attemp to catch specific location markers that are not yet in the NE-LOC dictionary
                    # Would be best to add these specific places in the dictionary once there are available resources
                    elif (i+1) < len(tokenTempList) and tokenTempList[i].lower() in ["sitio", "barrio", "purok"]:
                        

                        # Check if part of a larger NE-LOC entity or the start of an entity
                        if i > 0 and labelTempList[i-1] == "I" and tokenTempList[i-1].lower() in [",", "-"]:                            
                            backwardTraversal = i-1

                            while labelTempList[backwardTraversal] == "I":
                                if backwardTraversal == 0:
                                    break
                                else:
                                    backwardTraversal -= 1

                            if labelTempList[backwardTraversal] == "B-LOC":
                                labelTempList[i] = "I"
                            else:
                                labelTempList[i] = "B-LOC"
                            
                            labelTempList[i+1] = "I"
                            i += 2
                        
                        # Start of an entity
                        else:
                            labelTempList[i] = "B-LOC"
                            labelTempList[i+1] = "I"
                            i += 2

                        # Comma could indicate further locations
                        if i < len(tokenTempList) and tokenTempList[i].lower() == ",":
                            labelTempList[i] = "I"
                            i += 1
                            
                    # Attemp to catch specific location markers that are not yet in the NE-LOC dictionary
                    # Would be best to add these specific places in the dictionary once there are available resources
                    elif (i+1) < len(tokenTempList) and tokenTempList[i+1].lower() in ["street", "subdivision", "compound", "avenue", "boulevard", "highway"]:
                        
                        
                        # Check if part of a larger NE-LOC entity or the start of an entity
                        if i > 0 and labelTempList[i-1] == "I" and tokenTempList[i-1].lower() in [",", "-"]:
                            backwardTraversal = i-1

                            while labelTempList[backwardTraversal] == "I":
                                if backwardTraversal == 0:
                                    break
                                else:
                                    backwardTraversal -= 1

                            if labelTempList[backwardTraversal] == "B-LOC":
                                labelTempList[i] = "I"
                            else:
                                labelTempList[i] = "B-LOC"

                            labelTempList[i+1] = "I"
                            i += 2
                            
                        # Start of an entity
                        else:
                            labelTempList[i] = "B-LOC"
                            labelTempList[i+1] = "I"
                            i += 2

                        # Comma could indicate further locations
                        if i < len(tokenTempList) and tokenTempList[i].lower() == ",":
                            labelTempList[i] = "I"
                            i += 1

                    # Catching the following formats: <Month> <Day> to <Day>, <Month> <Year> to <Year>. (Ex. April 25 to 30, April 2024 hanggang 2025)
                    elif (i+1) < len(tokenTempList) and tokenTempList[i].lower() in ["to", "hanggang"] and tokenTempList[i+1].isdigit() and i > 0 and tokenTempList[i-1].isdigit():
                        

                        if i > 1 and tokenTempList[i-2].lower() in monthsList:
                            # Month Day to Day or Year to Year format
                            if ((re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i-1]) and re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', tokenTempList[i+1])) or 
                                (re.search(r'\b[0-9]{4}\b', tokenTempList[i-1]) and re.search(r'\b[0-9]{4}\b', tokenTempList[i+1]))):
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                                i += 2
                            else:
                                i += 1
                        else:
                            # Could be written without month (Ex. 14 to 31)
                            if labelTempList[i-1] == "I":
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"
                            # Could be independent use of this format (Ex. Sa 2024 hanggang 2025 ...)
                            else:
                                labelTempList[i-1] = "B-MWE"
                                labelTempList[i] = "I"
                                labelTempList[i+1] = "I"

                            i += 2

                    # To catch the format: <Day of the Week>, <Date> (Ex. Miyerkules, May 14)
                    # May 14 in this example, is catched by prior rules regarding dates
                    elif (i+2) < len(tokenTempList) and tokenTempList[i].lower() in daysOfTheWeek and tokenTempList[i+1].lower() == "," and tokenTempList[i+2].lower() in monthsList:
                        
                        
                        labelTempList[i] = "B-MWE"
                        labelTempList[i+1] = "I"
                        i += 2

                        
                    else:
                        # i += 1
                        # # 
                        
                        

                        # First word and letter of the suspected NE
                        word = tokenTempList[i].lower()
                        firstLetterOfWord = word[0]
                        
                        # Initialize flags and counter for detecting NEs
                        isNE = False
                        isLongerNE = False
                        shouldBeComplete = False
                        NEIndicator = 0
                        changeTheLabel = False
                        positionModifier = False
                        labelToChange = ""
                        indexToChange = 0

                        # Check if the detected word falls within the NEs or MWE categories
                        while NEIndicator < 4: 
                            # 

                            # Initialize the NEs or MWE dictionaries
                            match NEIndicator:
                                case 0:
                                    NECountDictionary = organizationNECountDict
                                    NEKeysList = organizationNEKeysList
                                    NEList = organizationNEList
                                case 1:
                                    NECountDictionary = locationNECountDict
                                    NEKeysList = locationNEKeysList
                                    NEList = locationNEList
                                case 2:
                                    NECountDictionary = personNECountDict
                                    NEKeysList = personNEKeysList
                                    NEList = personNEList
                                case 3:
                                    NECountDictionary = MWECountDict
                                    NEKeysList = MWEKeysList
                                    NEList = MWEList
                                    

                            # To reduce searching time, we only check on the indexes containing entities starting with the first letter of the current word
                            # The starting and ending indexes are stored in the countDict, which uses the starting letter of the word & its succeeding letter in the alphabet as keys
                            # We traverse the keyList to get these letters that serves as the dictionary keys, 
                            firstLetterStartIndex = NECountDictionary.get(firstLetterOfWord, "Not found")
                            
                            if firstLetterStartIndex != "Not found":
                            
                                nextLetterIndex = 0
                                succeddingLetter = ""

                                while nextLetterIndex < len(NEKeysList):
                                    if NEKeysList[nextLetterIndex] == firstLetterOfWord:
                                        succeddingLetter = NEKeysList[nextLetterIndex + 1]
                                        break
                                    else:
                                        nextLetterIndex += 1
                                        continue
                                        
                                succeddingLetterStartIndex = NECountDictionary.get(succeddingLetter, "Not found")

                                if succeddingLetterStartIndex != "Not Found":
                                    # iHolder holds the current position of the word being checked
                                    iHolder = i
                                    index = 0
                                    deductor = 0
                                    
                                    # Check if the word exist within entities in the dictionaries
                                    while firstLetterStartIndex <= succeddingLetterStartIndex:
                                        entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                        if word == entity[0]:

                                            
                                            shouldBeComplete = True

                                            # If preceeded by a beginningMarker
                                            if i > 0 and tokenTempList[i-1].lower() in beginningMarkers:
                                                
                                                labelTempList[i] = "I"  

                                            # If preceeded by certain symbols
                                            elif i > 0 and tokenTempList[i-1].lower() in ["'", "’", "‘", "-", "/"] and labelTempList[i-1] in ["I", "B-MWE"]:
                                                
                                                labelTempList[i] = "I"

                                            # If preceeded by a prefix
                                            elif prevPrefix != "" and i > 0 and tokenTempList[i].lower().startswith(tokenTempList[i-1][len(prefix):]):
                                                
                                                labelTempList[i] = "I"
                                                prevPrefix = ""
                                                
                                            # If preceeded by the location marker "barangay"
                                            elif NEIndicator == 1 and i > 0 and tokenTempList[i-1].lower() == "barangay":
                                                
                                                if i > 1 and labelTempList[i-2] in ["I", "B-LOC"]:
                                                    labelTempList[i-1] = "I"
                                                else:
                                                    labelTempList[i-1] = "B-LOC"
                                                labelTempList[i] = "I"
                                                isNE = True

                                            # If preceeded by the location marker "barangay" in its daglat form
                                            elif NEIndicator == 1 and i > 1 and tokenTempList[i-2].lower() in ["brgy", "bgy"]:
                                                
                                                labelTempList[i] = "I"
                                                isNE = True

                                            # If preceeded by modifying adjectives on a person's position
                                            elif NEIndicator == 2 and i > 0 and tokenTempList[i-1].lower() in ["dating", "bagong", "former"]:
                                                
                                                labelTempList[i-1] = "B-PER"
                                                labelTempList[i] = "I"
                                                isNE = True
                                                
                                            # Check if a NE-PER entity is within another entity
                                            elif i > 0 and NEIndicator == 2 and labelTempList[i-1] in ["B-PER", "B-ORG", "B-LOC", "I"]:
                                                
                                                
                                                
                                                # If preceeded by titles or honorifics 
                                                if tokenTempList[i-1] == "." or tokenTempList[i-1] in titleBeforeList or tokenTempList[i-1] in beginningMarkers:
                                                    labelTempList[i] = "I"    
                                                    
                                                
                                                # For detecting single name + single surname combination 
                                                elif labelTempList[i-1] == "B-PER":
                                                    labelTempList[i] = "I" 

                                                # If could be within a NE-ORG or NE-LOC entity
                                                elif labelTempList[i-1] in ["I", "B-ORG", "B-LOC"]:
                                                    
                                                    # Do backward traversal to identify current classification of entity
                                                    backwardTraversal = i-1
                                                    while labelTempList[backwardTraversal] == "I":
                                                        if backwardTraversal == 0:
                                                            break
                                                        else:
                                                            backwardTraversal -= 1

                                                    

                                                    # If inside another person entity or preceeded by the "mga" marker
                                                    if labelTempList[backwardTraversal] == "B-PER" or tokenTempList[backwardTraversal] == "mga":
                                                        labelTempList[i] = "I"  

                                                    # We update the label when it is a certain position of a person in a specific organization or location
                                                    # (Ex: DOH Undersecretary, Pasig City Mayor)
                                                    elif labelTempList[backwardTraversal] in ["B-ORG", "B-LOC"]:
                                                        if backwardTraversal > 0 and tokenTempList[backwardTraversal-1].lower() in ["dating", "former"]:
                                                            positionModifier = True
                                                            changeTheLabel = True
                                                            labelToChange = "B-PER"
                                                            indexToChange = backwardTraversal
                                                        else:
                                                            changeTheLabel = True
                                                            labelToChange = "B-PER"
                                                            indexToChange = backwardTraversal

                                                        labelTempList[i] = "I"  
                                                    
                                                    # Start of an independent person entity
                                                    else:
                                                        labelTempList[i] = "B-PER"
                                                # Start of an independent person entity
                                                else:
                                                    labelTempList[i] = "B-PER"

                                            # For catching Organization entities of the following formats:
                                            # Sangguniang Barangay/Bayan/Panlalawigan ng <Loc>
                                            # For catching Location entities of the following formats:
                                            # Lalawigan/Barangay ng <Loc> 
                                            elif NEIndicator == 1 and i > 0 and tokenTempList[i-1].lower() in ["ng", "of"] and labelTempList[i-1] == "I":
                                                

                                                # Do backward traversal to identify current classification of entity
                                                backwardTraversal = i-1
                                                while labelTempList[backwardTraversal] == "I":
                                                    if backwardTraversal == 0:
                                                        break
                                                    else:
                                                        backwardTraversal -= 1
                                                
                                                if labelTempList[backwardTraversal] in ["B-ORG", "B-LOC"]:
                                                    labelTempList[i] = "I"  
                                                    isNE = True
                                                elif labelTempList[backwardTraversal] == "B-PER":
                                                    labelTempList[i] = "I" 
                                                    changeTheLabel = True
                                                    labelToChange = "B-PER"
                                                    indexToChange = backwardTraversal
                                                else:
                                                    labelTempList[i] = "B-LOC"

                                            # For detecting valid address, separated by comma
                                            # Ex: (Barangay, City/Municipality, Province, Country)
                                            elif NEIndicator == 1 and i > 1 and tokenTempList[i-1].lower() == "," and labelTempList[i-2] in ["I", "B-LOC"]:
                                                

                                                # Do backward traversal to get the location
                                                backwardTraversal = i-2
                                                locationChecker = ""
                                                while tokenTempList[backwardTraversal].lower() not in ["ng", ",", "of"]:
                                                    if backwardTraversal == 0:
                                                        break
                                                    else:
                                                        backwardTraversal -= 1

                                                if backwardTraversal != 0:
                                                    backwardTraversal += 1

                                                # Store location in the locationChecker variable
                                                while backwardTraversal <= i:
                                                    if backwardTraversal == i or (backwardTraversal+1 < i and tokenTempList[backwardTraversal+1].lower() == ","):
                                                        locationChecker += tokenTempList[backwardTraversal].lower()
                                                        backwardTraversal += 1
                                                    else:
                                                        locationChecker += tokenTempList[backwardTraversal].lower() + " "
                                                        backwardTraversal += 1

                                                # Check if the location is a valid address based on the NE-LOC dictionary
                                                isValid = any(element.startswith(locationChecker) for element in NEList)

                                                # Label accordingly based if it is vaid or not
                                                if isValid == True:
                                                    labelTempList[i-1] = "I"
                                                    labelTempList[i] = "I"
                                                    isNE = True
                                                else:
                                                    labelTempList[i] = "B-LOC"

                                            # For the format: <Position> ng/of <Organization/Location> (Ex. Mayor ng Pasig City)
                                            elif (NEIndicator == 0 or NEIndicator == 1) and i > 0 and tokenTempList[i-1].lower() in ["ng", "of"] and labelTempList[i-1] == "I":
                                                

                                                # Do backward traversal to identify current classification of entity
                                                backwardTraversal = i-1
                                                while labelTempList[backwardTraversal] == "I":
                                                    if backwardTraversal == 0:
                                                        break
                                                    else:
                                                        backwardTraversal -= 1
                                                
                                                if labelTempList[backwardTraversal] in ["B-MWE", "B-PER"]:
                                                    labelTempList[i] = "I"  
                                                else:
                                                    if NEIndicator == 0:
                                                        labelTempList[i] = "B-ORG"
                                                    else:
                                                        labelTempList[i] = "B-LOC"


                                            # For updating the label in format: <LOC> <ORG> (Ex. China Coast Guard)
                                            # For consecutive locations that are matched separately
                                            elif (NEIndicator == 0 or NEIndicator == 1) and i > 0 and labelTempList[i-1] in ["I", "B-LOC", "B-ORG"]:
                                                
                                                backwardTraversal = i-1

                                                while labelTempList[backwardTraversal] == "I":
                                                    if backwardTraversal == 0:
                                                        break
                                                    else:
                                                        backwardTraversal -= 1
                                                
                                                if labelTempList[backwardTraversal] == "B-ORG":
                                                    labelTempList[i] = "I"  
                                                elif labelTempList[backwardTraversal] == "B-LOC":
                                                    if NEIndicator == 1:
                                                       labelTempList[i] = "I" 
                                                    else: 
                                                        labelTempList[i] = "I" 
                                                        changeTheLabel = True
                                                        labelToChange = "B-ORG"
                                                        indexToChange = backwardTraversal
                                                else:
                                                    if NEIndicator == 0:
                                                        labelTempList[i] = "B-ORG"
                                                    else:
                                                        labelTempList[i] = "B-LOC"

                                            else:
                                                
                                                match NEIndicator:
                                                    case 0:
                                                        labelTempList[i] = "B-ORG"                 
                                                    case 1:
                                                        labelTempList[i] = "B-LOC"          
                                                    case 2:
                                                        labelTempList[i] = "B-PER"          
                                                    case 3:
                                                        labelTempList[i] = "B-MWE"                                 

                                            # Check for NEs containing 2 or more words
                                            if (i + 1) != len(tokenTempList):
                                                # For detecting single word entities
                                                # For example: In Mr. Santos or single word location (Pilipinas)
                                                if len(entity) == 1:
                                                    # 
                                                    # 
                                                    current = NEList[firstLetterStartIndex]

                                                    if firstLetterStartIndex+1 < succeddingLetterStartIndex:
                                                        next = NEList[firstLetterStartIndex+1]
                                                        
                                                        # Check for longer entities that starts with the initially detected single word entity
                                                        # If longer entities exist, check for possible matches
                                                        if (i+1) <= len(tokenTempList) and next.startswith(current):

                                                            # When isLongerNE flag = TRUE, there are longer entities in the dictionary that starts with the initially matched entity.
                                                            # (Ex. Pampanga is already matched, but there are other entities like Pampanga South Park, etc.)
                                                            # This flag indicates that we had checked for possible longer entity match
                                                            # If at the end of matching, deductor != 0, there is no longer entity match
                                                            # We would update the incorrectly labelled tokens using the deductor

                                                            isLongerNE = True
                                                            deductor = 0
                                                            iHolder = i + 1
                                                            firstLetterStartIndex += 1
                                                            if firstLetterStartIndex < succeddingLetterStartIndex:
                                                                entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                            else:
                                                                break
                                                        else:
                                                            isNE = True
                                                            i += 1
                                                            break
                                                    else:
                                                        isNE = True
                                                        i += 1
                                                        break

                                                # Update i to check for the next word
                                                i += 1
                                                index += 1
                                                
                                                while index < len(entity) and i != len(tokenTempList):
                                                    
                                                    # For catching multi-word entities
                                                    if word == entity[0]:
                                                        # 
                                                        # 

                                                        # If match, update the label and increment the indexes
                                                        if tokenTempList[i].lower() == entity[index]:
                                                            labelTempList[i] = "I"
                                                            i += 1
                                                            index += 1
                                                            

                                                            if isLongerNE == True:
                                                                deductor += 1

                                                            # Qualify as NE when matches completely with the entity in the dictionary
                                                            if index == len(entity):

                                                                current = NEList[firstLetterStartIndex]
                                                                if firstLetterStartIndex+1 <= succeddingLetterStartIndex:
                                                                    next = NEList[firstLetterStartIndex+1]

                                                                    # Check for longer entities that starts with the initially detected single word entity
                                                                    # If longer entities exist, check for possible matches
                                                                    if (i+1) <= len(tokenTempList) and next.startswith(current):
                                                                        
                                                                        isLongerNE = True
                                                                        deductor = 0
                                                                        iHolder = i
                                                                        firstLetterStartIndex += 1
                                                                        if firstLetterStartIndex < succeddingLetterStartIndex:
                                                                            entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                                        else:
                                                                            break

                                                                    # Longer entity match found, reset deductor and update iHolder
                                                                    elif isLongerNE == True:
                                                                        deductor = 0
                                                                        iHolder = i 
                                                                    else:
                                                                        
                                                                        isNE = True
                                                                        break
                                                                else:
                                                                    isNE = True
                                                                    break

                                                        # For names of persons that are not complete
                                                        # Such as first name with surnames only 
                                                        elif NEIndicator == 2 and tokenTempList[i].lower() == entity[-1] and entity[-1] != ".":
                                                            labelTempList[i] = "I"
                                                            isNE = True
                                                            i += 1
                                                            break


                                                        # Increment firstLetterStartIndex to check for next entity in dictionary
                                                        else:
                                                            firstLetterStartIndex += 1
                                                            if firstLetterStartIndex < succeddingLetterStartIndex:
                                                                entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                            else:
                                                                break
                                                    
                                                    # For cases of single word entities
                                                    else:
                                                        # Update i, accordingly
                                                        if isNE == True and index == 1:
                                                            i = iHolder + 1
                                                            break
                                                        else:
                                                            break

                                                
                                                break

                                            # For catching entities positioned at the end of a sentence
                                            elif (i + 1) == len(tokenTempList) and (len(entity) == 1 or isNE == True):
                                                isNE = True
                                                i += 1
                                                break

                                            else:
                                                break

                                        # Increment firstLetterStartIndex to check for next entity in dictionary
                                        else:
                                            firstLetterStartIndex += 1

                                    # isLongerNE flag == True when PANG-KAT had already matched with an entity, but longer entity 
                                    # that starts with these initially matched entity exists, so we also check for these longer entities
                                    if isLongerNE == True:
                                        # If deductor != 0, no longer entity match
                                        # Update the incorrectly labelled tokens using the deductor 
                                        while deductor >= 0:
                                            if (i - deductor) == len(tokenTempList):
                                                deductor -= 1
                                            else:
                                                labelTempList[i-deductor] = "O"
                                                deductor -= 1

                                        # Update i with the value of iHolder
                                        i = iHolder
                                        

                                        # Check for nicknames enclosed in ""
                                        if i < len(tokenTempList):
                                            quoteChecker = -1
                                            
                                            if tokenTempList[i].find('\"') != -1 or tokenTempList[i].lower() == '“':
                                                quoteChecker = 1

                                            
                                            
                                            

                                        # Check for possible label update
                                        if positionModifier == True and changeTheLabel == True:
                                            labelTempList[indexToChange-1] = labelToChange
                                            labelTempList[indexToChange] = "I"

                                            
                                            
                                            break
                                        elif changeTheLabel == True:
                                            labelTempList[indexToChange] = labelToChange
                                            break

                                        # Nickname detected, label accordingly
                                        elif quoteChecker != -1 and beginningQuotesDetected == False:
                                            labelTempList[i] = "I"
                                            i += 1
                                            
                                            isWithinQuotes = True

                                            # Label the nickname until the closing quotation mark is found
                                            while isWithinQuotes == True:
                                                if tokenTempList[i].lower().find('\"') != -1 or tokenTempList[i].lower() == '”':
                                                    isWithinQuotes = False
                                                else:
                                                    labelTempList[i] = "I"
                                                    i += 1

                                            # Label the closing quotation mark
                                            labelTempList[i] = "I"
                                            i += 1
                                        else:
                                            break

                                    # When checking for entities is finished
                                    # Break the loop if qualified as entity
                                    elif isNE == True:
                                        
                                        # Check for possible label update
                                        if positionModifier == True and changeTheLabel == True:
                                            
                                            labelTempList[indexToChange-1] = labelToChange
                                            labelTempList[indexToChange] = "I"

                                            
                                            
                                            break
                                        elif changeTheLabel == True:
                                            
                                            labelTempList[indexToChange] = labelToChange
                                            break

                                        # Incomplete matching for location entities
                                        elif NEIndicator == 1 and tokenTempList[i-1].lower() == "," and labelTempList[i-1] == "I":
                                            
                                            labelTempList[i-1] = "O"
                                            break

                                        else:
                                            break

                                    # If not an entity, reset i and the labels to check for other categories
                                    elif shouldBeComplete == True and isNE == False:
                                        
                                        
                                        
                                        while index >= 0:
                                            if (i - index) == len(tokenTempList):
                                                index -= 1
                                            else:
                                                labelTempList[i-index] = "O"
                                                index -= 1

                                        i = iHolder
                                        NEIndicator += 1
                                        changeTheLabel = False

                                    # Increment NEIndicator to check for other categories
                                    else:
                                        NEIndicator += 1

                                else:
                                    # Increment NEIndicator to check for other categories
                                    NEIndicator += 1   

                            else:
                                # Increment NEIndicator to check for other categories
                                NEIndicator += 1         

                        if NEIndicator > 3:
                            
                            # Some rules doesn't fully increment matches, to check if they are succeeded with multi-word entities or expressions
                            # For instance, to catch "mga walang hiya", we only increment once to be able to catch "walang hiya", which is in the MWE dictionary.
                            # If no dictionary match were found, we label the word preceeded by a beginning marker and related rules here.

                            if tokenTempList[i-1].lower() in beginningMarkers:
                                labelTempList[i] = "I"
                            elif i > 1 and tokenTempList[i-2].lower() == "'" and tokenTempList[i-1].lower() == "di":
                                labelTempList[i-1] = "I"
                            elif i > 0 and tokenTempList[i-1] in ["-", "/"]:
                                if re.search(r'\w', tokenTempList[i]) and i > 1 and re.search(r'\w', tokenTempList[i-2]):
                                    labelTempList[i] = "I"
                            elif i > 1 and re.search(r'(ng)$', tokenTempList[i-1].lower()) and tokenTempList[i-2].lower() == "mga":
                                labelTempList[i] = "I"

                            # For checking nicknames enclosed in ""
                            # Could only be a nickname if the detected quote, is the beginning quote
                            if tokenTempList[i].find('\"') != -1 or tokenTempList[i].lower() == '“':
                                if beginningQuotesDetected == False:
                                    beginningQuotesDetected = True
                                else:
                                    beginningQuotesDetected = False

                            i += 1       

                else:
                    # For tracking if the quotation detected is a beginning or closing quote.
                    if tokenTempList[i].find('\"') != -1 or tokenTempList[i].lower() == '“':
                        if beginningQuotesDetected == False:
                            beginningQuotesDetected = True
                        else:
                            beginningQuotesDetected = False

                    i += 1
                    # 

            self.tokenList.append(tokenTempList)
            self.labelList.append(labelTempList)

        self.groupLongerTokenUnits(self.tokenList, self.labelList, self.longerTokenList, self.longerLabelList)
        
        return self.tokenList, self.labelList, self.longerTokenList, self.longerLabelList