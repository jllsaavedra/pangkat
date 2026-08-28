import re

# Rule for catching beginning markers
def beginningMarker(state):
    if state.tokenTempList[state.i].lower() in state.beginningMarkers:

        # Check if within or the start of a MWE
        if state.i !=0 and state.labelTempList[state.i-1] == "B-MWE":
            state.labelTempList[state.i] = "I"
        else:    
            state.labelTempList[state.i] = "B-MWE"

        # Checker for beginning marker + "<WORD/S>" format
        quoteChecker = -1
        if state.tokenTempList[state.i+1].lower().find('\"') != -1 or state.tokenTempList[state.i+1].lower() == '“':
            quoteChecker = 1

        # Checker for beginning marker + <WORD>-ng + <WORD> (Ex: mga nagdaang taon)
        if (state.i + 1) < len(state.tokenTempList) and (re.search(r'(ng)$', state.tokenTempList[state.i+1].lower())) and (re.search(r'\w', state.tokenTempList[state.i+1])):
            if (re.search(r'(ng)$', state.tokenTempList[state.i+1].lower())) and state.tokenTempList[state.i].lower() == "mga" and (state.i + 2) < len(state.tokenTempList):
                state.labelTempList[state.i+1] = "I"
                state.labelTempList[state.i+2] = "I"
                state.i += 2
            elif (state.i + 2) < len(state.tokenTempList) and state.tokenTempList[state.i+2].lower() in ["taon"]:
                state.labelTempList[state.i+1] = "I"
                state.labelTempList[state.i+2] = "I"
                state.i += 3
            else:
                state.labelTempList[state.i+1] = "I"
                state.i += 1

        # Checker for beginning marker + partial reduplication of <WORD> + <WORD> (Ex. nag ma marites)
        elif (state.i + 2) < len(state.tokenTempList) and state.tokenTempList[state.i+2].startswith(state.tokenTempList[state.i+1]):
            state.labelTempList[state.i+1] = "I"
            state.labelTempList[state.i+2] = "I"
            state.i += 3
            
        # Checker for beginning marker + "<WORD/S>" format
        elif quoteChecker != -1:

            state.labelTempList[state.i+1] = "I"
            state.i += 2
            isWithinQuotes = True

            # Label word/s until the closing quotation mark is found
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
            state.labelTempList[state.i+1] = "I"
            # Increment with 1 only to check for entities preceeded by preliminary markers
            # Ex: mga walang hiya
            state.i += 1
        return True
    return False