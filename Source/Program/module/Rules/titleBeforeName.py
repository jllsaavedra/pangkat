# For catching daglat of Tagalog titles and honorifics placed before a person’s name
def titleBeforeName(state):
    if state.tokenTempList[state.i].lower() in state.titleBeforeList and state.i + 2 < len(state.tokenTempList) and (state.tokenTempList[state.i + 1] == '.'):

        # Multiple titles/honorifics in daglat form
        if state.i > 1 and state.tokenTempList[state.i-1].lower() == "." and state.tokenTempList[state.i-2].lower() in state.titleBeforeList:
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 2
        elif state.i > 0 and state.tokenTempList[state.i-1].lower() in ["dating", "former"]:
            state.labelTempList[state.i-1] = "B-PER"
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 2
        else:
            # Multiple titles/honorifics, preceeding honorific is not in Daglat
            backwardTraversal = state.i-1

            while state.labelTempList[backwardTraversal] == "I":
                if backwardTraversal == 0:
                    break
                else:
                    backwardTraversal -= 1

            if state.labelTempList[backwardTraversal] == "B-PER":
                state.labelTempList[state.i] = "I"
            elif state.labelTempList[backwardTraversal] == "B-ORG":
                state.labelTempList[backwardTraversal] = "B-PER"
                state.labelTempList[state.i] = "I"  
            elif state.labelTempList[backwardTraversal] == "B-LOC":
                state.labelTempList[backwardTraversal] = "B-PER"
                state.labelTempList[state.i] = "I" 
            # Starting titles/honorifics
            else:
                state.labelTempList[state.i] = "B-PER"

            state.labelTempList[state.i+1] = "I"
            state.labelTempList[state.i+2] = "I"
            state.i += 2
        return True
    return False