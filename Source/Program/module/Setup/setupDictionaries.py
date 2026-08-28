# Function to set-up the dictionaries for the named entities (NE) and multi-word expressions (MWE)
# Although it is called dictionaries, they are implemented as arrays for easier traversal of the entities
# Morever, Python dictionary can't have duplicated keys that conflicts with the data of the NE and MWE dictionaries 
# Parameters passed include NEs (for the raw list of entities), NEList (where the pre-process entities are to be stored),
# NECountDict and NEKeysList are additional data for traversing the NEList
# NECountDict is a Python Dict, holding the starting index of entities in the NEList for each letter of the alphabet.
# NEKeysList holds the order of keys in NECountDict, crucial when no entity starting of a certain letter exists in the NEList
def setupDictionaries(NEs, NEList, NECountDict, NEKeysList):

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
