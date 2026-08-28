import re

# Rule for catching spelled-out large numbers in English
def englishLargeNumber(state):
    if re.search('^hundred$|^thousand$|^million$|^billion$|^trillion$', state.tokenTempList[state.i].lower()):

        singleWordNumbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                                "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "thirty",
                                "fourty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        singleDigitNumbers = singleWordNumbers[0:9]
        powerOfTens = singleWordNumbers[19:]

        # Check for numeric form + spelled out numerical classifiers (Ex. P900 million)
        if state.i > 0 and (re.search(r'^.?[0-9]+$', state.tokenTempList[state.i-1])):
            # Check if within an entity or the start of an entity
            if state.i > 1 and state.tokenTempList[state.i-2].lower() in [",", "."] and state.labelTempList[state.i-2] == "I":
                state.labelTempList[state.i-1] = "I"
            else:
                state.labelTempList[state.i-1] = "B-MWE"

            state.labelTempList[state.i] = "I"                        
            state.i += 1

        # Spelled out numbers in English
        else:
            # Comma is used to separate values (Ex. six hundred fifty-four thousand, three hundred twenty-one.)
            if state.i > 1 and state.tokenTempList[state.i-2].lower() == "," and state.labelTempList[state.i-2] == "I":
                state.labelTempList[state.i-1] = "I"
                state.labelTempList[state.i] = "I"
                state.i += 1
            # Numbers connected with hyphen are catched by the hyphen rules (Ex. fifty-four thousand)
            elif state.i > 1 and state.tokenTempList[state.i-2].lower() == "-" and state.labelTempList[state.i-1] == "I" and state.tokenTempList[state.i-1].lower() in singleWordNumbers:
                state.labelTempList[state.i] = "I"
                state.i += 1
            # Start of an entity
            else:
                state.labelTempList[state.i-1] = "B-MWE"
                state.labelTempList[state.i] = "I"
                state.i += 1

            # Catch comma used to separate values
            if state.tokenTempList[state.i].lower() == "," and state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in singleWordNumbers:
                state.labelTempList[state.i] = "I"

            # Catch numbers that are not connected with hyphen (Ex. twenty two)
            if state.tokenTempList[state.i].lower() in powerOfTens:
                if state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in singleDigitNumbers:
                    state.labelTempList[state.i] = "I"
                    state.labelTempList[state.i+1] = "I"
                    state.i += 2
                else:
                    state.labelTempList[state.i] = "I"
                    state.i += 1
            # Catch single word numbers (Ex. Sixteen)
            elif state.tokenTempList[state.i].lower() in singleWordNumbers:
                state.labelTempList[state.i] = "I"
                state.i += 1
            # Catch hundred + <another numerical classifier" (Ex: 900,000 -> nine hundred thousand)
            elif state.i > 0 and state.tokenTempList[state.i-1].lower() == "hundred" and state.tokenTempList[state.i].lower() in ["thousand", "million", "billion", "trillion"]:
                state.labelTempList[state.i] = "I"
                state.i += 1

                # Catch comma used to separate values
                if state.tokenTempList[state.i].lower() == "," and state.i+1 < len(state.tokenTempList) and state.tokenTempList[state.i+1].lower() in singleWordNumbers:
                    state.labelTempList[state.i] = "I"
        return True
    return False