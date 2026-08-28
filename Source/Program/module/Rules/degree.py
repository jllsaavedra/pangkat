# For catching the use of degree
def degree(state):
    if state.tokenTempList[state.i].lower() in ['°', 'º'] and state.tokenTempList[state.i - 1].isdigit():

        state.labelTempList[state.i-1] = "B-MWE"
        state.labelTempList[state.i] = "I"
        state.labelTempList[state.i+1] = "I"
        state.i += 2
        return True
    return False