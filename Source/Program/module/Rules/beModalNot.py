# For catching negated english be and model verbs
def beModalNot(state):
    if state.tokenTempList[state.i].lower() in state.beModalVerbsList and state.tokenTempList[state.i + 1] == 'not':

        state.labelTempList[state.i] = "B-MWE"
        state.labelTempList[state.i+1] = "I"
        state.i += 2
        return True
    return False