import re

# Catching basic math operations, symbols before number (Ex. ±4, log 10)
def mathPrefixSymbol(state):
    if state.tokenTempList[state.i].lower() in ['+', '-', '±', 'ln', 'log', 'sqrt', '√'] and state.i + 1 < len(state.tokenTempList) and re.search('\\d|^[a-z]{1,2}$|\\(', state.tokenTempList[state.i + 1]):


        if state.i > 0 and state.labelTempList[state.i-1] == "I":
            state.labelTempList[state.i] = "I"
        else:
            state.labelTempList[state.i] = "B-MWE"

        state.labelTempList[state.i+1] = "I"

        if state.tokenTempList[state.i+1] == "(":
            state.i += 1
        else:
            state.i += 2
        return True
    return False