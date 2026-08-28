import re

# Rule for catching spelled-out large numbers in Tagalog
def tagalogLargeNumber(state):
    if re.search('^daa(n)?(ng)?$|^libo(n)?(ng)?$|^raa(n)?(ng)?$|^milyo(n)?(ng)?$|^bilyo(n)?(ng)?$|^trilyo(n)?(ng)?$', state.tokenTempList[state.i].lower()):

        # Check if detected is a part or the start of a large number
        # (Ex. limang libo anim na daan at pitumpu't walo)
        if state.i > 0 and state.labelTempList[state.i-1] == "O":
            if (state.i-1) == 0:
                state.labelTempList[state.i-1] = "B-MWE"
            elif state.i > 1 and state.labelTempList[state.i-2] == "I" and state.tokenTempList[state.i-2].lower() == ",":
                state.labelTempList[state.i-1] = "I"
            else:
                state.labelTempList[state.i-1] = "B-MWE"

        # Part of a large number
        elif state.i > 1 and state.labelTempList[state.i-2] in ["B-MWE", "I"]:
            state.labelTempList[state.i-1] = "I"

        # For catching "daang/raang libo/milyon/bilyon"
        if state.tokenTempList[state.i].lower() in ["daang", "raang"]:
            state.labelTempList[state.i] = "I"
            state.i += 1

        # For catching daang/libong/milyong/bilyong
        if (re.search(r'(ng)$', state.tokenTempList[state.i].lower())):
            state.labelTempList[state.i] = "I"
            state.labelTempList[state.i+1] = "I"
            state.i += 2

        # The conjuection "na" is often used to indicate numerical classifiers
        elif state.tokenTempList[state.i-1].lower() == "na":
            # Ex: limang libo anim na daan
            # Label "anim na daan" based if it is preeceded by a much larger value or not
            if state.i - 2 == 0:
                state.labelTempList[state.i-2] = "B-MWE"
            elif state.i > 2 and state.labelTempList[state.i-3] == "O" :
                state.labelTempList[state.i-2] = "B-MWE"
            else:
                state.labelTempList[state.i-2] = "I"

            state.labelTempList[state.i-1] = "I"
            state.labelTempList[state.i] = "I"
            state.i += 1

            # Comma may be present to seperate quantities, for better readability
            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ",":
                state.labelTempList[state.i] = "I"
                state.i += 1
        else:
            # For catching daan or libo only
            state.labelTempList[state.i] = "I"
            state.i += 1

            # Comma may be present to seperate quantities, for better readability
            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ",":
                state.labelTempList[state.i] = "I"
                state.i += 1

        # Conjunction "at" or its conjuncted form "'t" are used for more specific values
        # (Ex. dalawang daan at sampu, walong daan at pitumpu’t anim na milyon)
        if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["at", "'", "’"]:
            while True:
                if state.i == len(state.tokenTempList):
                    break
                else:   
                    # For catching the conjunction "at"
                    if state.tokenTempList[state.i].lower() == "at":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.i += 2
                    # For catching the conjuncted form of at
                    elif state.tokenTempList[state.i].lower() in ["'", "’"] and state.tokenTempList[state.i+1].lower() == "t":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.labelTempList[state.i+2] = "I"
                        state.i += 3

                    else:
                        break
        return True
    return False