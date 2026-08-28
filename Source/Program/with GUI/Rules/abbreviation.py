import re

# Daglat with dots per letter
def abbreviation(state):
    if state.i > 0 and state.tokenTempList[state.i] == '.' and re.search('\\b[a-zA-Z]\\b', state.tokenTempList[state.i - 1]):

        # For catching successive letter with dot. The time indicator a.m. and p.m. is also catched here.
        if state.i > 1 and state.labelTempList[state.i-2] == "I" and (state.tokenTempList[state.i-2] == "." or re.search(r'\d', state.tokenTempList[state.i-2])):
            state.labelTempList[state.i-1] = "I"
            state.labelTempList[state.i] = "I"
            state.i += 1
        # Not a daglat
        elif state.i > 1 and state.tokenTempList[state.i-2] in ["'", "’", "‘"] and state.tokenTempList[state.i-1].lower() == "t":
            state.i += 1

        else:
            # If after a person entity, should be preceeded with a comma
            if state.i > 2 and state.tokenTempList[state.i-2].lower() == "," and state.labelTempList[state.i-3] == "I":
                state.labelTempList[state.i-2] = "I"
                state.labelTempList[state.i-1] = "I"

            elif state.i > 1 and re.search(r'\d', state.tokenTempList[state.i-2]) and state.tokenTempList[state.i-1].lower() in ["p", "a", "n"] and state.labelTempList[state.i-2] == "O":
                state.labelTempList[state.i-2] = "B-MWE"
                state.labelTempList[state.i-1] = "I"
                state.labelTempList[state.i] = "I"

            # Else, an independent daglat
            else:

                backwardTraversal = state.i-2

                while state.labelTempList[backwardTraversal] == "I":
                    if backwardTraversal == 0:
                        break
                    else:
                        backwardTraversal -= 1

                # Valid nickname



                if state.labelTempList[backwardTraversal] == "B-PER":
                    state.labelTempList[state.i-1] = "I"
                else:
                    state.labelTempList[state.i-1] = "B-MWE"

            state.labelTempList[state.i] = "I"
            state.i += 1
        return True
    return False