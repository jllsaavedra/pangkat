# To catch contracted "hindi" and "huwag" written with apostrophe
# However, we only increment once to check for entities that starts with "di" and "wag"
def contractedNot(state):
    if state.tokenTempList[state.i].lower() in ["'", '’', '‘'] and state.tokenTempList[state.i + 1].lower() in ['di', 'wag']:

        state.labelTempList[state.i] = "B-MWE"
        state.labelTempList[state.i+1] = "I"
        state.i += 1
        return True
    return False