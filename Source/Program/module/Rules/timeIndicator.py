import re

# English 12-hr clock system, no minutes (Ex: 3 PM)
def timeIndicator(state):
    if state.tokenTempList[state.i].lower() in ['am', 'pm'] and re.search('\\d', state.tokenTempList[state.i - 1]):

        if state.labelTempList[state.i-2] != "O":
            state.labelTempList[state.i-1] = "I"
        else:
            state.labelTempList[state.i-1] = "B-MWE"

        state.labelTempList[state.i] = "I"
        state.i += 1
        return True
    return False