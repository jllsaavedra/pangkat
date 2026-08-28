import re

# Rule for catching months without the prefix "ika-" (Ex. sa 15 ng Abril)
def monthDateExpression(state):
    if state.tokenTempList[state.i].lower() in state.monthsList and state.i > 1 and re.search('\\b[0-2][0-9]\\b|\\b3[0-1]\\b|\\b[0-9]\\b', state.tokenTempList[state.i - 2]):

        if state.tokenTempList[state.i-1].lower() == "ng":

            state.labelTempList[state.i-2] = "B-MWE"
            state.labelTempList[state.i-1] = "I"
            state.labelTempList[state.i] = "I"
            state.i += 1
        else:
            state.i += 1
        return True
    return False