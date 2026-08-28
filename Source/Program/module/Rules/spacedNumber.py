import re

# English large numbers, numerical format, separated by spaces (Ex. 9 876 543 210)
def spacedNumber (state):
    if re.search('^[0-9]{1,3}$', state.tokenTempList[state.i]) and state.i + 1 < len(state.tokenTempList) and re.search('^[0-9]{1,3}$', state.tokenTempList[state.i + 1]):

        # Check if start of entity or inside the entity
        if state.labelTempList[state.i] != "O":
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 1
        else:
            state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 1
        return True
    return False