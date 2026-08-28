# Catching basic math operations, symbols after number (Ex. 160 x 25%, 8″ x 5″)
def mathPostfixSymbol(state):
    if state.tokenTempList[state.i].lower() in ['+', '-', 'x', '/'] and state.tokenTempList[state.i - 1].lower() in ['″', '%']:


        if state.labelTempList[state.i-1] == "I":
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 2
        return True
    return False
