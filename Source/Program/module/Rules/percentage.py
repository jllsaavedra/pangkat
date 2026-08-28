# For catching the use of percentage
def percentage(state):
    if state.tokenTempList[state.i].lower() in ['%', 'porsiyento', 'porsyento', 'percent'] and state.tokenTempList[state.i - 1].isdigit():

        if state.labelTempList[state.i-1] != "I":
            state.labelTempList[state.i-1] = "B-MWE"

        state.labelTempList[state.i] = "I"
        state.i += 1
        return True
    return False