import re

# Catching contractions and other applications of apostrophe
def apostrophe(state):
    if state.tokenTempList[state.i].lower() in ["'", '’', '‘', '″']:

        # Contracted year and height (Example: 2024 -> '24)
        if state.i+1 < len(state.tokenTempList) and (re.search(r'\d', state.tokenTempList[state.i+1])):
            # Height: 5'0
            if state.i != 0 and (re.search(r'\d', state.tokenTempList[state.i-1])) and state.labelTempList[state.i-1] == "O":

                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            # Contracted year as part of other entity
            elif state.labelTempList[state.i-1] in ["B-PER", "B-LOC", "B-ORG", "B-MWE", "I"]:
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            # Contracted year
            else:                            
                state.labelTempList[state.i] = "B-MWE"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

        # Catching Spanish numbers' spelling variation that uses "'y" (Ex. trenta'y dos)
        elif state.i > 0 and state.tokenTempList[state.i-1] in ["treynta", "trenta", "kwarenta", "singkwenta", "sisenta", "sitenta", "otsenta", "nobenta"]:
            if state.i + 1 < len(state.tokenTempList) and state.tokenTempList [state.i+1].lower() == "y":
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.labelTempList[state.i+2] = "I"
                state.i += 3

            else:
                state.i += 1

        # Catching words with contracted first sylabble (Ex: ito -> 'to, iyon -> 'yon)
        elif state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in state.firstLetterContraction:
            # To catch: nito -> n'to, niyo -> n'yo, mga ito -> mga 'to, 
            if state.i != 0 and state.tokenTempList[state.i-1].lower() in ["n", "mga"]:
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2
            # Words with contracted first sylabble
            else:
                state.labelTempList[state.i] = "B-MWE"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

        # Other contractions
        else:
            if state.i+1 < len(state.tokenTempList) and (re.search(r'\w', state.tokenTempList[state.i-1])) and (re.search(r'\w', state.tokenTempList[state.i+1])):
                # Check if part of another entity
                if state.labelTempList[state.i-1] not in ["B-PER", "B-LOC", "B-ORG", "B-MWE", "I"]:
                    state.labelTempList[state.i-1] = "B-MWE"
                elif state.tokenTempList[state.i-1].lower() in state.contractedNot:
                    state.labelTempList[state.i-1] = "B-MWE"

                state.labelTempList[state.i] = "I"

                # Catch contracted "at" and "not"
                if state.tokenTempList[state.i+1].lower() == "t" and state.tokenTempList[state.i-1].lower() not in state.contractedNot:
                    state.labelTempList[state.i+1] = "I"

                    # Catch when the next word ends with -ng, connecting another word
                    if state.i+2 < len(state.tokenTempList) and (re.search(r'(ng)$', state.tokenTempList[state.i+2].lower())):
                        state.labelTempList[state.i+2] = "I"
                        state.labelTempList[state.i+3] = "I"
                        state.i += 4
                    else:
                        state.labelTempList[state.i+2] = "I"
                        state.i += 3

                # Contracted "not"
                else:
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2
            else:
                state.i += 1
        return True
    return False