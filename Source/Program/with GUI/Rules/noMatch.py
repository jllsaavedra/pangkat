# Fallback executed when none of the explicit rules matched.
def noMatch(state):
    # For tracking if the quotation detected is a beginning or closing quote.
    if state.tokenTempList[state.i].find('\"') != -1 or state.tokenTempList[state.i].lower() == '“':
        if state.beginningQuotesDetected == False:
            state.beginningQuotesDetected = True
        else:
            state.beginningQuotesDetected = False

    state.i += 1
    return True