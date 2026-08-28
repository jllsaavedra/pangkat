import re

# For catching basic math operations
def basicMathOperation(state):
    if state.tokenTempList[state.i].lower() in ['+', 'x', '=', '^'] and state.i + 1 < len(state.tokenTempList) and re.search('\\d|^[a-z]{1,2}$|\\(', state.tokenTempList[state.i + 1]) and re.search('\\d|^[a-z]{1,2}$|\\)', state.tokenTempList[state.i - 1]):


        if state.labelTempList[state.i-1] == "I":
            state.labelTempList[state.i-1] = "I"
        else:
            state.labelTempList[state.i-1] = "B-MWE"

        state.labelTempList[state.i] = "I"
        state.labelTempList[state.i+1] = "I"
        state.i += 2

        # Catching symbols before number (Ex. -4, ln 4)
        if (state.i < len(state.tokenTempList) and state.tokenTempList[state.i-1].lower() in ["+", "-", "±", "ln", "log", "sqrt", "√"] and (re.search(r'\d|^[a-z]{1,2}$|', state.tokenTempList[state.i]))):
            state.labelTempList[state.i] = "I"
            state.i += 1
        return True
    return False