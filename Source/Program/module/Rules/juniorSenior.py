# For catching daglat of junior and senior added after a person's name (Ex. Saavedra Jr.)
def juniorSenior(state):
    if state.tokenTempList[state.i].lower() in ['jr', 'sr']:

        if state.i > 0 and state.labelTempList[state.i-1] in ["I", "B-PER"]:
            state.labelTempList[state.i] = "I"
            state.i += 1

            if state.i < len(state.tokenTempList):
                # The daglat Jr and Sr may be written with or without periods
                if state.tokenTempList[state.i].lower() == ".":
                    state.labelTempList[state.i] = "I"
                    state.i += 1

        # The daglar Jr and Sr may be preceeded with a comma after a person's name (Saavedra, Jr.)
        elif state.i > 1 and state.tokenTempList[state.i-1] == "," and state.labelTempList[state.i-2] in ["I", "B-PER"]:
            state.labelTempList[state.i-1] = "I"
            state.labelTempList[state.i] = "I"
            state.i += 1

            if state.i < len(state.tokenTempList):
                # The daglat Jr and Sr may be written with or without periods
                if state.tokenTempList[state.i].lower() == ".":
                    state.labelTempList[state.i] = "I"
                    state.i += 1

        else:
            state.i += 1
        return True
    return False