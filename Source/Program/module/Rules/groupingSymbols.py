import re

# Catching grouping symbols
def groupingSymbols(state):
    if state.tokenTempList[state.i].lower() in ['(', '[', '{']:

        state.groupingSymbols = state.tokenTempList[state.i]

        # Checking if the content refers to an abbreviation of an entity (Ex. (DOH), (OFW))
        if state.i > 0 and state.labelTempList[state.i-1] in ["B-PER", "B-ORG", "I"]:

            # Traverse entity to check if it is within a Person entity, Organization entity or not
            iHolder = state.i-1
            if iHolder == 0 and state.labelTempList[iHolder] in ["B-PER", "B-ORG", "B-LOC", "B-MWE"]:

                state.labelTempList[state.i] = "I"
                state.i += 1

            # Not an abbreviation
            elif iHolder == 0 and state.labelTempList[iHolder] not in ["B-PER", "B-ORG", "B-LOC", "B-MWE"]:

                state.labelTempList[state.i] = "B-MWE"
                state.i += 1

            else:
                # Traverse the entity
                while state.labelTempList[iHolder] == "I":
                    if iHolder > 0:
                        iHolder -= 1
                    else:
                        break

                # Label if within a Person/Organization entity
                if state.labelTempList[iHolder] in ["B-ORG", "B-LOC", "B-PER"]:
                    state.labelTempList[state.i] = "I"
                    state.i += 1
                # Within a mathematical equation
                elif state.labelTempList[iHolder] == "B-MWE" and state.i+1 < len(state.tokenTempList) and (re.search(r'\d|[a-z]{1,2}', state.tokenTempList[state.i+1])):
                    state.labelTempList[state.i] = "I"
                    state.i += 1
                # Preceeded by a beginning marker
                elif state.labelTempList[iHolder] == "B-MWE" and state.tokenTempList[iHolder].lower() in state.beginningMarkers:
                    state.labelTempList[state.i] = "I"
                    state.i += 1
                else:
                    state.labelTempList[state.i] = "B-MWE"
                    state.i += 1

        # Mathematical equation markers
        elif state.tokenTempList[state.i-1].lower() in ["+", "-", "±", "ln", "log", "sqrt"]:
            state.labelTempList[state.i] = "I"
            state.i += 1

        # Independent use of grouping symbols
        else:
            state.labelTempList[state.i] = "B-MWE"
            state.i += 1

        # Find the closing pair of the detected grouping symbol, label insides
        match state.groupingSymbols:
            case "(":

                while state.tokenTempList[state.i].lower() != ")":
                    state.labelTempList[state.i] = "I"
                    state.i += 1

            case "[":

                while state.tokenTempList[state.i].lower() != "]":
                    state.labelTempList[state.i] = "I"
                    state.i += 1

            case "{":

                while state.tokenTempList[state.i].lower() != "}":
                    state.labelTempList[state.i] = "I"
                    state.i += 1

        # Label the closing pair
        state.labelTempList[state.i] = "I"
        state.i += 1
        return True
    return False