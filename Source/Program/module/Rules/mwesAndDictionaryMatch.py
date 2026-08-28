import re

# For catching multi words expressions and dictionary lookup
def mwesAndDictionaryMatch(state):
    if state.i + 1 <= len(state.tokenTempList):
        # For catching nicknames enclosed in ""
        quoteChecker = state.tokenTempList[state.i].lower().find('\"')

        # For catching repeated words with added infix
        infixInIndex = state.tokenTempList[state.i].lower().find("in")
        infixUmIndex = state.tokenTempList[state.i].lower().find("um")
        tokenWithoutInfix = ""

        # Remove the infix and save the root word in the tokenWithoutInfix variable
        if infixInIndex != -1 or infixUmIndex != -1:
            if infixInIndex != -1:
                prevString = state.tokenTempList[state.i][0:infixInIndex].lower()
                nextString = state.tokenTempList[state.i][(infixInIndex + 2):].lower()
                tokenWithoutInfix = prevString + nextString

            elif infixUmIndex != -1:
                prevString = state.tokenTempList[state.i][0:infixUmIndex].lower()
                nextString = state.tokenTempList[state.i][(infixUmIndex + 2):].lower()
                tokenWithoutInfix = prevString + nextString

        # For checking for intensified words (connected by "-ng") and plain repeating words (Ex. gaya gaya)
        # Check if current word starts with the next word
        if (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower().startswith(state.tokenTempList[state.i+1].lower()) and re.search(r"\w", state.tokenTempList[state.i].lower()) and len (state.tokenTempList[state.i+1]) > 2:

            # To catch exaggerations connected by "-ng" (Ex: magandang maganda)
            if (re.search(r'(ng)$', state.tokenTempList[state.i].lower()) and (state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-2)].lower() == state.tokenTempList[state.i+1].lower() or 
                state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-1)].lower() == state.tokenTempList[state.i+1].lower())):

                state.labelTempList[state.i] = "B-MWE"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Plain repeating words
            elif state.tokenTempList[state.i].lower() == state.tokenTempList[state.i+1].lower():
                #  To avoid labelling subsequent "na". For instance in: "alam ko na na ganon talaga"
                if state.tokenTempList[state.i].lower() != "na":
                    #  To catch phrases that make sense with "ang" or pa. 
                    #  Ex: ang ganda ganda, pa bago bago
                    if state.i > 0 and state.tokenTempList[state.i-1].lower() in ["ang", "pa",]:
                        state.labelTempList[state.i-1] = "B-MWE"
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2
                    # Plain repeating words
                    else:
                        if state.i > 0 and state.tokenTempList[state.i-1].lower() != "-":
                            state.labelTempList[state.i] = "B-MWE"
                        elif state.i == 0:
                            state.labelTempList[state.i] = "B-MWE"
                        else:
                            state.labelTempList[state.i] = "I"

                        state.labelTempList[state.i+1] = "I"
                        state.i += 2

                # No match = go to next word
                else:
                    state.i += 1
            # No match = go to next word
            else:
                state.i += 1

        # Repeating words with partial reduplication (Ex. kani kanila)
        # Check length of first word to avoid conflicting particles (Ex. "na naliligo" should not be labeled)
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == state.tokenTempList[state.i+1][:len(state.tokenTempList[state.i])].lower() and len(state.tokenTempList[state.i].lower()) > 3:

            state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # Repeating words with added prefix. (Ex: magtuloy tuloy, mabago bago, kaproud proud, mamali mali, tatanga tanga)
        # Check if current word ends with next word
        elif ((state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower().endswith(state.tokenTempList[state.i+1].lower()) and re.search(r"\w", state.tokenTempList[state.i].lower()) and len (state.tokenTempList[state.i+1]) > 2 and
                (state.tokenTempList[state.i][0:2].lower() == state.tokenTempList[state.i+1][0:2].lower() or state.tokenTempList[state.i][:(len(state.tokenTempList[state.i]) - len(state.tokenTempList[state.i+1]))].lower() in state.combinedPrefixes or 
                state.tokenTempList[state.i][:(len(state.tokenTempList[state.i]) - len(state.tokenTempList[state.i+1]))].lower() in (s + state.tokenTempList[state.i+1][0:2].lower() for s in state.combinedPrefixes) )):


            # When the prefix is written with space following the repeated word and was detected as a preliminary marker (Ex: mag tutuloy tuloy)
            # Plural repeating nouns are also labelled here. (Ex. mga nagloloko loko)
            if state.i > 0 and state.labelTempList[state.i-1] == "B-MWE":
                state.labelTempList[state.i] = "I"
            else:
                state.labelTempList[state.i] = "B-MWE"

            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # For checking for intensified words (connected by "na" and "at")
        # For checking for continuity of action, based on "nang"
        # For checking for the use of the preposition "to" in this format: <WORD> to <SAME WORD>
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i] in ["na", "nang", "to", "at"] and state.tokenTempList[state.i-1].lower() == state.tokenTempList[state.i+1].lower() and re.search(r'\w', state.tokenTempList[state.i-1]):

            state.labelTempList[state.i-1] = "B-MWE"
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # Repeating words with added infix. (Ex: tumalon talon, pumunta punta, tinali tali)
        elif (state.i+1) < len(state.tokenTempList) and tokenWithoutInfix != "" and tokenWithoutInfix == state.tokenTempList[state.i+1].lower():

            state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # Repeating words that ends with "ng" (Ex. marami raming)
        elif (state.i > 0 and re.search(r'(ng)$', state.tokenTempList[state.i].lower()) and 
            state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-2)].lower() == state.tokenTempList[state.i-1][len(state.tokenTempList[state.i-1])-len(state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-2)]):].lower() and
            len(state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-2)]) > 2 and len(state.tokenTempList[state.i-1][len(state.tokenTempList[state.i-1])-len(state.tokenTempList[state.i][:(len(state.tokenTempList[state.i])-2)]):]) > 2):

            state.labelTempList[state.i-1] = "B-MWE"
            state.labelTempList[state.i] = "I"
            state.i += 1

        # Catching the use of Spanish "y" in connecting maternal's surname in one's full name
        # Catching independent use of Spanish numbers from 30 - 99
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "y":

            # The beginning word of Spanish numbers from 30 to 99
            spanish30to99Beginning = ["treynta", "trenta", "kwarenta", "singkwenta", "sisenta", "sitenta", "otsenta", "nobenta"]

            # Spanish "y" in connecting maternal surname
            if state.i > 0 and state.labelTempList[state.i-1] in ["B-PER", "I"]:

                # Traverse entity to check if it is within a Person entity or not
                iHolder = state.i-1
                if iHolder == 0 and state.labelTempList[iHolder] == "B-PER":
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2

                # Not a valid use of Spanish "y"
                elif iHolder == 0 and state.labelTempList[iHolder] != "B-PER":
                    state.i += 1

                else:
                    # Traverse the entity
                    while state.labelTempList[iHolder] == "I":
                        if iHolder > 0:
                            iHolder -= 1
                        else:
                            break

                    # Label if within a Person entity
                    if state.labelTempList[iHolder] == "B-PER":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2
                    else:
                        state.i += 1

            # Independent use of Spanish numbers
            elif state.tokenTempList[state.i+1].lower() in ["uno", "dos", "tres", "kwatro", "singko", "sais", "syete", "otso", "nwebe"]:
                # Standard Spanish spelling using "y" (Ex. trenta y dos)
                if state.i > 0 and state.tokenTempList[state.i-1].lower() in spanish30to99Beginning:
                    state.labelTempList[state.i-1] = "B-MWE"
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2

            else:
                state.i += 1

        # Catching Tagalog numbers from 11-19 (Ex. labing apat)
        elif (state.i+1) < len(state.tokenTempList) and (re.search(r'^labing$|^beynte$|^bente$', state.tokenTempList[state.i].lower())):  

            if state.i > 0 and state.tokenTempList[state.i-1].lower == "at" and state.labelTempList[state.i-1] == "I":
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            else:
                state.labelTempList[state.i] = "B-MWE"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

        # English 12-hr clock system with minutes (Ex. 9:30 ng umaga, 9:30 AM)
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ":":

            if (re.search(r'\d', state.tokenTempList[state.i-1])) and (re.search(r'\d', state.tokenTempList[state.i+1])):
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

                if state.i < len(state.tokenTempList):
                    # English abbreviated time indicators
                    if state.tokenTempList[state.i].lower() in ["am", "pm"]:
                        state.labelTempList[state.i] = "I"
                        state.i += 1

                    # Catching Tagalog time indicators
                    elif state.tokenTempList[state.i].lower() == "ng" and state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in state.tagalogTimeIndicators:
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2

                        if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["gabi", "araw"]:
                            state.labelTempList[state.i] = "I"
                            state.i += 1

                    # For catching XX:XX - XX:XX formats
                    elif state.tokenTempList[state.i].lower() == "-":

                        state.isDashDetected = True
                        state.i = state.i
            else:
                state.i += 1

        # Catching decimal numbers and daglat of specific location markers
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i] == ".":

            # Decimal numbers
            if state.i > 0 and re.search(r'^.?[0-9]+$', state.tokenTempList[state.i-1]) and state.tokenTempList[state.i+1].isdigit():
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Daglat of location markers
            elif state.i > 0 and state.tokenTempList[state.i-1].lower() in ["brgy", "bgy", "blk", "prk", "subd", "cpd", "ave", "blvd", "hiway", "hwy"]:
                if state.i > 1 and state.labelTempList[state.i-2] == "I":
                    state.labelTempList[state.i-1] = "I"  
                else:
                    state.labelTempList[state.i-1] = "B-LOC"
                state.labelTempList[state.i] = "I"
                state.i += 1

            else:
                state.i += 1

        # Attemp to catch specific location markers that are not yet in the NE-LOC dictionary
        # Would be best to add these specific places in the dictionary once there are available resources
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["sitio", "barrio", "purok"]:

            # Check if part of a larger NE-LOC entity or the start of an entity
            if state.i > 0 and state.labelTempList[state.i-1] == "I" and state.tokenTempList[state.i-1].lower() in [",", "-"]:                            
                backwardTraversal = state.i-1

                while state.labelTempList[backwardTraversal] == "I":
                    if backwardTraversal == 0:
                        break
                    else:
                        backwardTraversal -= 1

                if state.labelTempList[backwardTraversal] == "B-LOC":
                    state.labelTempList[state.i] = "I"
                else:
                    state.labelTempList[state.i] = "B-LOC"

                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Start of an entity
            else:
                state.labelTempList[state.i] = "B-LOC"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Comma could indicate further locations
            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ",":
                state.labelTempList[state.i] = "I"
                state.i += 1

        # Attemp to catch specific location markers that are not yet in the NE-LOC dictionary
        # Would be best to add these specific places in the dictionary once there are available resources
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in ["street", "subdivision", "compound", "avenue", "boulevard", "highway"]:

            # Check if part of a larger NE-LOC entity or the start of an entity
            if state.i > 0 and state.labelTempList[state.i-1] == "I" and state.tokenTempList[state.i-1].lower() in [",", "-"]:
                backwardTraversal = state.i-1

                while state.labelTempList[backwardTraversal] == "I":
                    if backwardTraversal == 0:
                        break
                    else:
                        backwardTraversal -= 1

                if state.labelTempList[backwardTraversal] == "B-LOC":
                    state.labelTempList[state.i] = "I"
                else:
                    state.labelTempList[state.i] = "B-LOC"

                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Start of an entity
            else:
                state.labelTempList[state.i] = "B-LOC"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # Comma could indicate further locations
            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ",":
                state.labelTempList[state.i] = "I"
                state.i += 1

        # Catching the following formats: <Month> <Day> to <Day>, <Month> <Year> to <Year>. (Ex. April 25 to 30, April 2024 hanggang 2025)
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["to", "hanggang"] and state.tokenTempList[state.i+1].isdigit() and state.i > 0 and state.tokenTempList[state.i-1].isdigit():

            if state.i > 1 and state.tokenTempList[state.i-2].lower() in state.monthsList:
                # Month Day to Day or Year to Year format
                if ((re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i-1]) and re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i+1])) or 
                    (re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i-1]) and re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i+1]))):
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2
                else:
                    state.i += 1
            else:
                # Could be written without month (Ex. 14 to 31)
                if state.labelTempList[state.i-1] == "I":
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                # Could be independent use of this format (Ex. Sa 2024 hanggang 2025 ...)
                else:
                    state.labelTempList[state.i-1] = "B-MWE"
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"

                state.i += 2

        # To catch the format: <Day of the Week>, <Date> (Ex. Miyerkules, May 14)
        # May 14 in this example, is catched by prior rules regarding dates
        elif (state.i+2) < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in state.daysOfTheWeek and state.tokenTempList[state.i+1].lower() == "," and state.tokenTempList[state.i+2].lower() in state.monthsList:

            state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        else:

            # First word and letter of the suspected NE
            word = state.tokenTempList[state.i].lower()
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

                # Initialize the NEs or MWE dictionaries
                match NEIndicator:
                    case 0:
                        NECountDictionary = state.organizationNECountDict
                        NEKeysList = state.organizationNEKeysList
                        NEList = state.organizationNEList
                    case 1:
                        NECountDictionary = state.locationNECountDict
                        NEKeysList = state.locationNEKeysList
                        NEList = state.locationNEList
                    case 2:
                        NECountDictionary = state.personNECountDict
                        NEKeysList = state.personNEKeysList
                        NEList = state.personNEList
                    case 3:
                        NECountDictionary = state.MWECountDict
                        NEKeysList = state.MWEKeysList
                        NEList = state.MWEList

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
                        iHolder = state.i
                        index = 0
                        deductor = 0

                        # Check if the word exist within entities in the dictionaries
                        while firstLetterStartIndex <= succeddingLetterStartIndex:
                            entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                            if word == entity[0]:

                                shouldBeComplete = True

                                # If preceeded by a beginningMarker
                                if state.i > 0 and state.tokenTempList[state.i-1].lower() in state.beginningMarkers:

                                    state.labelTempList[state.i] = "I"  

                                # If preceeded by certain symbols
                                elif state.i > 0 and state.tokenTempList[state.i-1].lower() in ["'", "’", "‘", "-", "/"] and state.labelTempList[state.i-1] in ["I", "B-MWE"]:

                                    state.labelTempList[state.i] = "I"

                                # If preceeded by a prefix
                                elif state.prevPrefix != "" and state.i > 0 and state.tokenTempList[state.i].lower().startswith(state.tokenTempList[state.i-1][len(state.prefix):]):

                                    state.labelTempList[state.i] = "I"
                                    state.prevPrefix = ""

                                # If preceeded by the location marker "barangay"
                                elif NEIndicator == 1 and state.i > 0 and state.tokenTempList[state.i-1].lower() == "barangay":

                                    if state.i > 1 and state.labelTempList[state.i-2] in ["I", "B-LOC"]:
                                        state.labelTempList[state.i-1] = "I"
                                    else:
                                        state.labelTempList[state.i-1] = "B-LOC"
                                    state.labelTempList[state.i] = "I"
                                    isNE = True

                                # If preceeded by the location marker "barangay" in its daglat form
                                elif NEIndicator == 1 and state.i > 1 and state.tokenTempList[state.i-2].lower() in ["brgy", "bgy"]:

                                    state.labelTempList[state.i] = "I"
                                    isNE = True

                                # If preceeded by modifying adjectives on a person's position
                                elif NEIndicator == 2 and state.i > 0 and state.tokenTempList[state.i-1].lower() in ["dating", "bagong", "former"]:

                                    state.labelTempList[state.i-1] = "B-PER"
                                    state.labelTempList[state.i] = "I"
                                    isNE = True

                                # Check if a NE-PER entity is within another entity
                                elif state.i > 0 and NEIndicator == 2 and state.labelTempList[state.i-1] in ["B-PER", "B-ORG", "B-LOC", "I"]:

                                    # If preceeded by titles or honorifics 
                                    if state.tokenTempList[state.i-1] == "." or state.tokenTempList[state.i-1] in state.titleBeforeList or state.tokenTempList[state.i-1] in state.beginningMarkers:
                                        state.labelTempList[state.i] = "I"    

                                    # For detecting single name + single surname combination 
                                    elif state.labelTempList[state.i-1] == "B-PER":
                                        state.labelTempList[state.i] = "I" 

                                    # If could be within a NE-ORG or NE-LOC entity
                                    elif state.labelTempList[state.i-1] in ["I", "B-ORG", "B-LOC"]:

                                        # Do backward traversal to identify current classification of entity
                                        backwardTraversal = state.i-1
                                        while state.labelTempList[backwardTraversal] == "I":
                                            if backwardTraversal == 0:
                                                break
                                            else:
                                                backwardTraversal -= 1

                                        # If inside another person entity or preceeded by the "mga" marker
                                        if state.labelTempList[backwardTraversal] == "B-PER" or state.tokenTempList[backwardTraversal] == "mga":
                                            state.labelTempList[state.i] = "I"  

                                        # We update the label when it is a certain position of a person in a specific organization or location
                                        # (Ex: DOH Undersecretary, Pasig City Mayor)
                                        elif state.labelTempList[backwardTraversal] in ["B-ORG", "B-LOC"]:
                                            if backwardTraversal > 0 and state.tokenTempList[backwardTraversal-1].lower() in ["dating", "former"]:
                                                positionModifier = True
                                                changeTheLabel = True
                                                labelToChange = "B-PER"
                                                indexToChange = backwardTraversal
                                            else:
                                                changeTheLabel = True
                                                labelToChange = "B-PER"
                                                indexToChange = backwardTraversal

                                            state.labelTempList[state.i] = "I"  

                                        # Start of an independent person entity
                                        else:
                                            state.labelTempList[state.i] = "B-PER"
                                    # Start of an independent person entity
                                    else:
                                        state.labelTempList[state.i] = "B-PER"

                                # For catching Organization entities of the following formats:
                                # Sangguniang Barangay/Bayan/Panlalawigan ng <Loc>
                                # For catching Location entities of the following formats:
                                # Lalawigan/Barangay ng <Loc> 
                                elif NEIndicator == 1 and state.i > 0 and state.tokenTempList[state.i-1].lower() in ["ng", "of"] and state.labelTempList[state.i-1] == "I":

                                    # Do backward traversal to identify current classification of entity
                                    backwardTraversal = state.i-1
                                    while state.labelTempList[backwardTraversal] == "I":
                                        if backwardTraversal == 0:
                                            break
                                        else:
                                            backwardTraversal -= 1

                                    if state.labelTempList[backwardTraversal] in ["B-ORG", "B-LOC"]:
                                        state.labelTempList[state.i] = "I"  
                                        isNE = True
                                    elif state.labelTempList[backwardTraversal] == "B-PER":
                                        state.labelTempList[state.i] = "I" 
                                        changeTheLabel = True
                                        labelToChange = "B-PER"
                                        indexToChange = backwardTraversal
                                    else:
                                        state.labelTempList[state.i] = "B-LOC"

                                # For detecting valid address, separated by comma
                                # Ex: (Barangay, City/Municipality, Province, Country)
                                elif NEIndicator == 1 and state.i > 1 and state.tokenTempList[state.i-1].lower() == "," and state.labelTempList[state.i-2] in ["I", "B-LOC"]:

                                    # Do backward traversal to get the location
                                    backwardTraversal = state.i-2
                                    locationChecker = ""
                                    while state.tokenTempList[backwardTraversal].lower() not in ["ng", ",", "of"]:
                                        if backwardTraversal == 0:
                                            break
                                        else:
                                            backwardTraversal -= 1

                                    if backwardTraversal != 0:
                                        backwardTraversal += 1

                                    # Store location in the locationChecker variable
                                    while backwardTraversal <= state.i:
                                        if backwardTraversal == state.i or (backwardTraversal+1 < state.i and state.tokenTempList[backwardTraversal+1].lower() == ","):
                                            locationChecker += state.tokenTempList[backwardTraversal].lower()
                                            backwardTraversal += 1
                                        else:
                                            locationChecker += state.tokenTempList[backwardTraversal].lower() + " "
                                            backwardTraversal += 1

                                    # Check if the location is a valid address based on the NE-LOC dictionary
                                    isValid = any(element.startswith(locationChecker) for element in NEList)

                                    # Label accordingly based if it is vaid or not
                                    if isValid == True:
                                        state.labelTempList[state.i-1] = "I"
                                        state.labelTempList[state.i] = "I"
                                        isNE = True
                                    else:
                                        state.labelTempList[state.i] = "B-LOC"

                                # For the format: <Position> ng/of <Organization/Location> (Ex. Mayor ng Pasig City)
                                elif (NEIndicator == 0 or NEIndicator == 1) and state.i > 0 and state.tokenTempList[state.i-1].lower() in ["ng", "of"] and state.labelTempList[state.i-1] == "I":

                                    # Do backward traversal to identify current classification of entity
                                    backwardTraversal = state.i-1
                                    while state.labelTempList[backwardTraversal] == "I":
                                        if backwardTraversal == 0:
                                            break
                                        else:
                                            backwardTraversal -= 1

                                    if state.labelTempList[backwardTraversal] in ["B-MWE", "B-PER"]:
                                        state.labelTempList[state.i] = "I"  
                                    else:
                                        if NEIndicator == 0:
                                            state.labelTempList[state.i] = "B-ORG"
                                        else:
                                            state.labelTempList[state.i] = "B-LOC"

                                # For updating the label in format: <LOC> <ORG> (Ex. China Coast Guard)
                                # For consecutive locations that are matched separately
                                elif (NEIndicator == 0 or NEIndicator == 1) and state.i > 0 and state.labelTempList[state.i-1] in ["I", "B-LOC", "B-ORG"]:

                                    backwardTraversal = state.i-1

                                    while state.labelTempList[backwardTraversal] == "I":
                                        if backwardTraversal == 0:
                                            break
                                        else:
                                            backwardTraversal -= 1

                                    if state.labelTempList[backwardTraversal] == "B-ORG":
                                        state.labelTempList[state.i] = "I"  
                                    elif state.labelTempList[backwardTraversal] == "B-LOC":
                                        if NEIndicator == 1:
                                            state.labelTempList[state.i] = "I" 
                                        else: 
                                            state.labelTempList[state.i] = "I" 
                                            changeTheLabel = True
                                            labelToChange = "B-ORG"
                                            indexToChange = backwardTraversal
                                    else:
                                        if NEIndicator == 0:
                                            state.labelTempList[state.i] = "B-ORG"
                                        else:
                                            state.labelTempList[state.i] = "B-LOC"

                                else:

                                    match NEIndicator:
                                        case 0:
                                            state.labelTempList[state.i] = "B-ORG"                 
                                        case 1:
                                            state.labelTempList[state.i] = "B-LOC"          
                                        case 2:
                                            state.labelTempList[state.i] = "B-PER"          
                                        case 3:
                                            state.labelTempList[state.i] = "B-MWE"                                 

                                # Check for NEs containing 2 or more words
                                if (state.i + 1) != len(state.tokenTempList):
                                    # For detecting single word entities
                                    # For example: In Mr. Santos or single word location (Pilipinas)
                                    if len(entity) == 1:

                                        current = NEList[firstLetterStartIndex]

                                        if firstLetterStartIndex+1 < succeddingLetterStartIndex:
                                            next = NEList[firstLetterStartIndex+1]

                                            # Check for longer entities that starts with the initially detected single word entity
                                            # If longer entities exist, check for possible matches
                                            if (state.i+1) <= len(state.tokenTempList) and next.startswith(current):

                                                # When isLongerNE flag = TRUE, there are longer entities in the dictionary that starts with the initially matched entity.
                                                # (Ex. Pampanga is already matched, but there are other entities like Pampanga South Park, etc.)
                                                # This flag indicates that we had checked for possible longer entity match
                                                # If at the end of matching, deductor != 0, there is no longer entity match
                                                # We would update the incorrectly labelled tokens using the deductor

                                                isLongerNE = True
                                                deductor = 0
                                                iHolder = state.i + 1
                                                firstLetterStartIndex += 1
                                                if firstLetterStartIndex < succeddingLetterStartIndex:
                                                    entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                else:
                                                    break
                                            else:
                                                isNE = True
                                                state.i += 1
                                                break
                                        else:
                                            isNE = True
                                            state.i += 1
                                            break

                                    # Update i to check for the next word
                                    state.i += 1
                                    index += 1

                                    while index < len(entity) and state.i != len(state.tokenTempList):

                                        # For catching multi-word entities
                                        if word == entity[0]:

                                            # If match, update the label and increment the indexes
                                            if state.tokenTempList[state.i].lower() == entity[index]:
                                                state.labelTempList[state.i] = "I"
                                                state.i += 1
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
                                                        if (state.i+1) <= len(state.tokenTempList) and next.startswith(current):

                                                            isLongerNE = True
                                                            deductor = 0
                                                            iHolder = state.i
                                                            firstLetterStartIndex += 1
                                                            if firstLetterStartIndex < succeddingLetterStartIndex:
                                                                entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", NEList[firstLetterStartIndex])
                                                            else:
                                                                break

                                                        # Longer entity match found, reset deductor and update iHolder
                                                        elif isLongerNE == True:
                                                            deductor = 0
                                                            iHolder = state.i 
                                                        else:

                                                            isNE = True
                                                            break
                                                    else:
                                                        isNE = True
                                                        break

                                            # For names of persons that are not complete
                                            # Such as first name with surnames only 
                                            elif NEIndicator == 2 and state.tokenTempList[state.i].lower() == entity[-1] and entity[-1] != ".":
                                                state.labelTempList[state.i] = "I"
                                                isNE = True
                                                state.i += 1
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
                                                state.i = iHolder + 1
                                                break
                                            else:
                                                break

                                    break

                                # For catching entities positioned at the end of a sentence
                                elif (state.i + 1) == len(state.tokenTempList) and (len(entity) == 1 or isNE == True):
                                    isNE = True
                                    state.i += 1
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
                                if (state.i - deductor) == len(state.tokenTempList):
                                    deductor -= 1
                                else:
                                    state.labelTempList[state.i-deductor] = "O"
                                    deductor -= 1

                            # Update i with the value of iHolder
                            state.i = iHolder

                            # Check for nicknames enclosed in ""
                            if state.i < len(state.tokenTempList):
                                quoteChecker = -1

                                if state.tokenTempList[state.i].find('\"') != -1 or state.tokenTempList[state.i].lower() == '“':
                                    quoteChecker = 1

                            # Check for possible label update
                            if positionModifier == True and changeTheLabel == True:
                                state.labelTempList[indexToChange-1] = labelToChange
                                state.labelTempList[indexToChange] = "I"
                                break

                            elif changeTheLabel == True:
                                state.labelTempList[indexToChange] = labelToChange
                                break

                            # Nickname detected, label accordingly
                            elif quoteChecker != -1 and state.beginningQuotesDetected == False:
                                state.labelTempList[state.i] = "I"
                                state.i += 1

                                isWithinQuotes = True

                                # Label the nickname until the closing quotation mark is found
                                while isWithinQuotes == True:
                                    if state.tokenTempList[state.i].lower().find('\"') != -1 or state.tokenTempList[state.i].lower() == '”':
                                        isWithinQuotes = False
                                    else:
                                        state.labelTempList[state.i] = "I"
                                        state.i += 1

                                # Label the closing quotation mark
                                state.labelTempList[state.i] = "I"
                                state.i += 1
                            else:
                                break

                        # When checking for entities is finished
                        # Break the loop if qualified as entity
                        elif isNE == True:

                            # Check for possible label update
                            if positionModifier == True and changeTheLabel == True:

                                state.labelTempList[indexToChange-1] = labelToChange
                                state.labelTempList[indexToChange] = "I"
                                break

                            elif changeTheLabel == True:
                                state.labelTempList[indexToChange] = labelToChange
                                break

                            # Incomplete matching for location entities
                            elif NEIndicator == 1 and state.tokenTempList[state.i-1].lower() == "," and state.labelTempList[state.i-1] == "I":
                                state.labelTempList[state.i-1] = "O"
                                break

                            else:
                                break

                        # If not an entity, reset i and the labels to check for other categories
                        elif shouldBeComplete == True and isNE == False:

                            while index >= 0:
                                if (state.i - index) == len(state.tokenTempList):
                                    index -= 1
                                else:
                                    state.labelTempList[state.i-index] = "O"
                                    index -= 1

                            state.i = iHolder
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

                if state.tokenTempList[state.i-1].lower() in state.beginningMarkers:
                    state.labelTempList[state.i] = "I"
                elif state.i > 1 and state.tokenTempList[state.i-2].lower() == "'" and state.tokenTempList[state.i-1].lower() == "di":
                    state.labelTempList[state.i-1] = "I"
                elif state.i > 0 and state.tokenTempList[state.i-1] in ["-", "/"]:
                    if re.search(r'\w', state.tokenTempList[state.i]) and state.i > 1 and re.search(r'\w', state.tokenTempList[state.i-2]):
                        state.labelTempList[state.i] = "I"
                elif state.i > 1 and re.search(r'(ng)$', state.tokenTempList[state.i-1].lower()) and state.tokenTempList[state.i-2].lower() == "mga":
                    state.labelTempList[state.i] = "I"

                # For checking nicknames enclosed in ""
                # Could only be a nickname if the detected quote, is the beginning quote
                if state.tokenTempList[state.i].find('\"') != -1 or state.tokenTempList[state.i].lower() == '“':
                    if state.beginningQuotesDetected == False:
                        state.beginningQuotesDetected = True
                    else:
                        state.beginningQuotesDetected = False

                state.i += 1
        return True
    return False