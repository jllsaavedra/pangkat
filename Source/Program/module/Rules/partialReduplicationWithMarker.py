import re

# Rule for catching beginning markers + partial reduplication of combined word, no-hyphen (Ex. nagma marites)
def partialReduplicationWithMarker(state):
    if state.prefix != '' and re.search('\\w', state.tokenTempList[state.i]) and (state.i + 1 < len(state.tokenTempList)) and state.tokenTempList[state.i + 1].lower().startswith(state.tokenTempList[state.i][len(state.prefix):]) and (len(state.tokenTempList[state.i][len(state.prefix):]) > 1):

        # Check if start of within an entity (Ex. mga nagma marites)
        if state.i !=0 and state.labelTempList[state.i-1] == "B-MWE":
            state.labelTempList[state.i] = "I"
        else:    
            state.labelTempList[state.i] = "B-MWE"

        state.labelTempList[state.i+1] = "I"
        # prevPrefix is used for checking for named entities preceeded by a prefix
        state.prevPrefix = state.prefix
        state.i += 1
        return True
    return False