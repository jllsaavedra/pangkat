# Rule for time format without prefix and minutes (Ex. 9 ng umaga)
def numericTimeExpression(state):
    if state.tokenTempList[state.i].isdigit() and state.i + 2 < len(state.tokenTempList) and (state.tokenTempList[state.i + 1].lower() == 'ng') and (state.tokenTempList[state.i + 2].lower() in state.tagalogTimeIndicators):

        state.labelTempList[state.i] = "B-MWE"
        state.labelTempList[state.i+1] = "I"
        state.labelTempList[state.i+2] = "I"
        state.i += 3

        if state.i < len(state.tokenTempList) and state.tokenTempList[state.i] in ["araw", "gabi"]:
            state.labelTempList[state.i] = "I"
            state.i += 1
        return True
    return False