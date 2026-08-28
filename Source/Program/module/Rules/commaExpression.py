import re

# Catching uses of comma: 
# (1) connecting titles after name, (2) as a number delimeter and
# (3) to catch person entities of the format <Surname> , <Name>
def commaExpression(state):
    if state.tokenTempList[state.i].lower() == ',' and state.i + 1 < len(state.tokenTempList):

        # Catch titles added after a person's name (Ex, <Name> , PhD)
        if state.tokenTempList[state.i+1].lower() in state.titleAfterList and state.i > 0 and state.labelTempList[state.i-1] in ["I", "B-PER"]:
            # For the format: <Surname> , <Title>
            if state.labelTempList[state.i-1] == "B-PER":
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            else:
                iHolder = state.i - 1
                # Else, traverse the entity to check if it is a person entity
                # For format with <Name> <Surname> , <Title>
                if iHolder == 0 and state.labelTempList[iHolder] == "B-PER":
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2
                # Not a valid daglat of titles
                elif iHolder == 0 and state.labelTempList[iHolder] != "B-PER":
                    state.i += 1
                else:
                    # Traversing the entity
                    while state.labelTempList[iHolder] == "I":
                        if iHolder > 0:
                            iHolder -= 1
                        else:
                            break

                    # If inside a person entity, label the comma and title
                    if state.labelTempList[iHolder] == "B-PER":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2
                    else:
                        state.i += 1

        # For numbers delimited by comma
        elif (re.search(r'^(P?[0-9]{1,3})$', state.tokenTempList[state.i-1])) and (re.search(r'^([0-9]{1,3})$', state.tokenTempList[state.i+1])):
            if state.labelTempList[state.i-1] != "O":
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            else:
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2


        # Catch Person entities in <Surname> , <First Name> ... format
        else:

            # Check if the current word is in the list of Person Entities
            word = state.tokenTempList[state.i+1].lower()
            firstLetterOfWord = word[0]

            # To reduce searching time, we only check on the indexes containing entities starting with the first letter of the current word
            # The starting and ending indexes are stored in the personNECountDict
            firstLetterStartIndex = state.personNECountDict.get(firstLetterOfWord, "Not found")
            if firstLetterStartIndex != "Not found":

                nextLetterIndex = 0
                succeddingLetter = ""

                while nextLetterIndex < len(state.personNEKeysList):
                    if state.personNEKeysList[nextLetterIndex] == firstLetterOfWord:
                        succeddingLetter = state.personNEKeysList[nextLetterIndex + 1]
                        break
                    else:
                        nextLetterIndex += 1
                        continue

                succeddingLetterStartIndex = state.personNECountDict.get(succeddingLetter, "Not found")

                if succeddingLetterStartIndex != "Not Found":

                    # Check if the current word exists among the entites in the selected indexes of personNEList
                    while firstLetterStartIndex <= succeddingLetterStartIndex:
                        entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", state.personNEList[firstLetterStartIndex])
                        # If both first and last name matches, label them
                        if word == entity[0] and entity[-1] == state.tokenTempList[state.i-1].lower():

                            state.labelTempList[state.i-1] = "B-PER"
                            state.labelTempList[state.i] = "I"
                            state.labelTempList[state.i+1] = "I"

                            surname = state.tokenTempList[state.i-1].lower()
                            state.i += 2

                            # Check for possible succeeding names for the entity
                            if len(entity) >= 2 and state.i != len(state.tokenTempList):
                                index = 1
                                while index < len(entity) and state.i != len(state.tokenTempList):
                                    # Check for possible entities with the same first and last name, but different succeeding names
                                    if word == entity[0] and entity[-1] == surname:
                                        if state.tokenTempList[state.i].lower() == entity[index]:
                                            state.labelTempList[state.i] = "I"
                                            state.i += 1
                                            index += 1
                                        # If succeeding names doesn't match with current entity, check for next entity
                                        # Entities are sorted alphabetically to reduce searching time
                                        else:
                                            firstLetterStartIndex += 1
                                            if firstLetterStartIndex < succeddingLetterStartIndex:
                                                entity = re.findall(r"[\$\w]+|[.,!?;'%()-–—″‘’“”&¿#…°º√\"]", state.personNEList[firstLetterStartIndex])
                                            else:
                                                break
                                    else:
                                        state.i += 1
                                        break

                                # If no succeeding names found, decrement i to recheck the word for other possible rule match
                                state.i -= 1
                                break

                            else:
                                break
                        else:
                            firstLetterStartIndex += 1

                    # If current word != entity, move to next word. Always update i for any rule mismatch
                    state.i += 1
                else:
                    state.i += 1
            else:
                state.i += 1
        return True
    return False