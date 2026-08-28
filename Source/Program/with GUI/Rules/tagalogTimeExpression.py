# Rule to catch Tagalog time expressions in “ala/alas [Spanish-number] ng [Tagalog-time-indicator]” format
def tagalogTimeExpression(state):
    if state.i + 1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ['ala', 'alas']:

        # Spanish numbers from 1-12:
        spanishHours = ["una", "dos", "tres", "kwatro", "kuwatro", "singko", "sais", "syete", "siyete", "otso", "nwebe", "nuwebe", "dyes", "diyes", "onse", "dose"]
        spanish1to9 = spanishHours[0:9]

        # If utilizes the dash format (Ex: ala-, alas-)
        if state.tokenTempList[state.i+1].lower() == "-":
            if state.i > 0 and state.tokenTempList[state.i-1].lower() == "pasado":
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
            else:
                state.labelTempList[state.i] = "B-MWE"

            state.labelTempList[state.i+1] = "I"
            state.i += 1

        # Catching spanish numbers, to assure that it is a time expression (Ex. alas tres)
        if state.tokenTempList[state.i+1] in spanishHours or state.tokenTempList[state.i+1].isdigit(): 
            # Catch "pasado", meaning "past" in "pasado alas dos". Can also be written after the Spanish-number.
            if state.i > 0 and state.tokenTempList[state.i-1].lower() == "pasado":
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
            elif state.tokenTempList[state.i].lower() == "-":
                state.labelTempList[state.i] = "I"
            else:
                state.labelTempList[state.i] = "B-MWE"

            state.labelTempList[state.i+1] = "I"
            state.i += 2

            # Impunto is used for exact time. (Ex. alas tres impunto for 3:00)
            if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["pasado", "impunto"]:
                state.labelTempList[state.i] = "I"
                state.i += 1

            if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == ":":
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"
                state.i += 2

            # For catching specific time written in Spanish (Ex. alas tres y medya)
            if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "y":
                # Spanish numbers above 30 are written with "y" (Ex. treynta y kwatro)
                # Spelling variations may occur and be written with "'y" (Ex. treynta'y kwatro)
                if state.tokenTempList[state.i+1] in ["treynta", "trenta", "kwarenta", "singkwenta"]:
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2

                    # Catch spelling variation using "'y"
                    if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in ["'", "’"] and state.tokenTempList[state.i+1].lower() == "y":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i+1] = "I"
                        state.labelTempList[state.i+2] = "I"
                        state.i += 3
                    # Catch spelling following the Spanish format
                    elif state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "y":
                        state.labelTempList[state.i] = "I"
                        state.labelTempList[state.i] = "I"
                        state.i += 2

                # Spanish numbers from 20-29 does not use "y" (Ex. beynte dos, bente dos)
                elif state.tokenTempList[state.i+1].lower() in ["beynte", "bente"]:
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2

                    # Catch numbers from 21-29
                    if state.i < len(state.tokenTempList) and state.tokenTempList[state.i].lower() in spanish1to9:
                        state.labelTempList[state.i] = "I"
                        state.i += 1

                # Spanish numbers from 16-19 uses the prefix "dyesi-" or its modified "disi-" form in Tagalog (disi-otso)
                # Spelling variations exist and may also be spelled as one word (Ex. disisyete)
                elif state.tokenTempList[state.i+1].lower() in ["dyesi", "disi"] and state.i+2 < len(state.tokenTempList) and state.tokenTempList[state.i+2].lower() == "-":
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.labelTempList[state.i+2] = "I"
                    state.labelTempList[state.i+3] = "I"
                    state.i += 4

                # Spanish numbers from 1 to 19 written in single words, "medya" is also catched here
                else:
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2

            # Time indicators may or may not be connected with "na"
            if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "na" and state.tokenTempList[state.i+1].lower() == "ng":
                state.labelTempList[state.i] = "I"
                state.i += 1

            # Catching Tagalog time indicators, if present or not 
            if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "ng" and state.tokenTempList[state.i+1].lower() in state.tagalogTimeIndicators:
                state.labelTempList[state.i] = "I"
                state.labelTempList[state.i+1] = "I"

                # For catching the second word in "hating gabi" and "madaling araw"
                if state.i+2 < len(state.tokenTempList) and state.tokenTempList[state.i+2].lower() in ["gabi", "araw"]:
                    state.labelTempList[state.i+2] = "I"
                    state.i += 3
                else:
                    state.i += 2

            # Abbreviated tagalog time formats
            elif state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i].lower() == "n" and state.tokenTempList[state.i+1] == ".":
                if state.i+3 < len(state.tokenTempList) and state.tokenTempList[state.i+2].lower() in ["u", "h", "g"] and state.tokenTempList[state.i+3] == ".":
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.labelTempList[state.i+2] = "I"
                    state.labelTempList[state.i+3] = "I"
                    state.i += 4
                else:
                    state.i += 1
        else:
            state.i += 1
        return True
    return False