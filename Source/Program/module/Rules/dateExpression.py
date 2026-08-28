import re

# Catching English date formats
def dateExpression(state):
    if state.tokenTempList[state.i].lower() in state.monthsList and state.i + 1 < len(state.tokenTempList) and (re.search('\\d', state.tokenTempList[state.i + 1]) or state.tokenTempList[state.i + 1] == '.'):

        daglatMonths = state.monthsList[0:20]

        # DAY-MONTH (Ex: 15 April, 15 Apr.)
        if (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i-1])):
            state.labelTempList[state.i-1] = "B-MWE"
            state.labelTempList[state.i] = "I"
            state.i += 1

            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i-1].lower() in daglatMonths and state.tokenTempList[state.i] == ".":
                state.labelTempList[state.i] = "I"
                state.i += 1


        # ABBREVIATED MONTH.-DAY (Ex: Apr. 15,)
        elif (state.i+1) < len(state.tokenTempList) and state.tokenTempList[state.i+1] == "." and state.tokenTempList[state.i].lower() in daglatMonths:
            if (state.i+2) < len(state.tokenTempList) and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i+2])):
                if state.i > 1 and state.tokenTempList[state.i-2].lower() in state.daysOfTheWeek and state.labelTempList[state.i-2] == "B-MWE":
                    state.labelTempList[state.i] = "I"
                else:
                    state.labelTempList[state.i] = "B-MWE"

                state.labelTempList[state.i+1] = "I"
                state.labelTempList[state.i+2] = "I"
                state.i += 3

                if state.i < len(state.tokenTempList) and state.tokenTempList[state.i] == "," and re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i+1]):
                    state.labelTempList[state.i] = "I"
                    state.i += 1

            # Catching months without the prefix "ika-" + abbreviated month (Ex. sa 15 ng Apr.)
            elif state.i > 1 and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i-2])):
                if state.tokenTempList[state.i-1].lower() == "ng":
                    # 
                    state.labelTempList[state.i-2] = "B-MWE"
                    state.labelTempList[state.i-1] = "I"
                    state.labelTempList[state.i] = "I"
                    state.i += 1

                    if state.i < len(state.tokenTempList) and state.tokenTempList[state.i] == "." and state.tokenTempList[state.i-1].lower() in daglatMonths:
                        state.labelTempList[state.i] = "I"

                        state.i += 1

                else:
                    state.i += 1
            else:
                state.i += 1

        # MONTH-DAY (Ex. April 15, )
        elif (state.i+1) < len(state.tokenTempList) and (re.search(r'\b[0-2][0-9]\b|\b3[0-1]\b|\b[0-9]\b', state.tokenTempList[state.i+1])):
            if state.i > 1 and state.tokenTempList[state.i-2].lower() in state.daysOfTheWeek and state.labelTempList[state.i-2] == "B-MWE":
                state.labelTempList[state.i] = "I"
            else:
                state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i] == "," and re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i+1]):
                state.labelTempList[state.i] = "I"
                state.i += 1

        # MONTH-YEAR only (April 2025)
        elif (state.i+1) < len(state.tokenTempList) and (re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i+1])):
            if state.i > 1 and state.tokenTempList[state.i-2].lower() in state.daysOfTheWeek and state.labelTempList[state.i-2] == "B-MWE":
                state.labelTempList[state.i] = "I"
            else:
                state.labelTempList[state.i] = "B-MWE"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # Not a valid month format
        else:
            state.i += 1

        # For catching year, when present
        if state.i < len(state.tokenTempList) and (re.search(r'\b[0-9]{4}\b', state.tokenTempList[state.i])):
            state.labelTempList[state.i] = "I"
            state.i += 1
        return True
    return False