import re

# Catching multi-word expressions connected by dash or slash
def dashOrSlash(state):
    if state.i != 0 and state.i + 1 < len(state.tokenTempList) and (state.tokenTempList[state.i].lower() == '-') or state.tokenTempList[state.i].lower() == '/':

        if (re.search(r"\w", state.tokenTempList[state.i-1].lower()) or state.tokenTempList[state.i-1].lower() == ")") and re.search(r"\w", state.tokenTempList[state.i+1].lower()):
            # For labelling entities connected by dash or slash
            if state.isDashDetected == False and state.labelTempList[state.i-1] not in ["I", "B-PER", "B-ORG", "B-LOC"]:
                if state.tokenTempList[state.i-1].lower() in ["tga", "taga"]:
                    state.labelTempList[state.i-1] = "B-LOC"
                else:
                    state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"

            # For labelling consecutive dashes or slashes in an expression
            else:
                state.labelTempList[state.i] = "I"

            if re.search(r'(ed)$', state.tokenTempList[state.i+1].lower()):
                state.labelTempList[state.i+1] = "I" 
                state.labelTempList[state.i+2] = "I"
                state.i += 2
            else:
                state.labelTempList[state.i+1] = "I"
                state.i += 1

            # For catching consecutive uses of dashes, slashes, and certain date and time formats
            if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1] in ["-", "/", "ng", ":"]:
                state.i += 1

                if state.i != len(state.tokenTempList):
                    if state.tokenTempList[state.i].lower() == "-" or state.tokenTempList[state.i].lower() == "/":
                        state.isDashDetected = True

                    # Catch date and time expressions using the prefix "ika-" and "a-""
                    elif state.tokenTempList[state.i] == "ng":


                        # Catching month for date expressions and Tagalog time indicators for time expressions
                        if state.tokenTempList[state.i+1].lower() in state.monthsList or state.tokenTempList[state.i+1] in state.tagalogTimeIndicators:
                            state.labelTempList[state.i] = "I"
                            state.labelTempList[state.i+1] = "I"

                            # For catching the second word in "hating gabi" and "madaling araw"
                            if state.i+2 < len(state.tokenTempList) and state.tokenTempList[state.i+2].lower() in ["gabi", "araw"]:
                                state.labelTempList[state.i+2] = "I"
                                state.i += 3
                            else:
                                state.i += 2
                        else:
                            state.i += 1

                    # Catching time expressions of English XX:XX - XX:XX AM/PM format
                    elif state.tokenTempList[state.i] == ":":

                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2

                        # For catching English time indicators, if present or not
                        if state.tokenTempList[state.i].lower() in ["am", "pm"]:
                            state.labelTempList[state.i] = "I"
                            state.i += 1
                        # For catching Tagalog time indicators, if present or not
                        elif state.tokenTempList[state.i].lower() == "ng" and state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1] in state.tagalogTimeIndicators:
                            state.labelTempList[state.i] = "I"
                            state.labelTempList[state.i+1] = "I"
                            state.i += 2

                            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["gabi", "araw"]:
                                state.labelTempList[state.i] = "I"
                                state.i += 1  
                    else:
                        state.isDashDetected = False
                else:
                    state.isDashDetected = False
            else:
                state.isDashDetected = False

        # Catching subtraction and division
        elif (state.tokenTempList[state.i].lower() in ["-", "/"] and (re.search(r'\d|^[a-z]{1,2}$|\(', state.tokenTempList[state.i+1])) and (re.search(r'\d|^[a-z]{1,2}$|\)', state.tokenTempList[state.i-1]))):

            if state.tokenTempList[state.i+1] == "(" and state.tokenTempList[state.i-1] == ")":
                state.labelTempList[state.i] = "I"
                state.i += 1
            else:
                if state.labelTempList[state.i-1] == "I":
                    state.labelTempList[state.i-1] = "I"
                else:
                    state.labelTempList[state.i-1] = "B-MWE"

                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
        else:
            state.i += 1
        return True
    return False
