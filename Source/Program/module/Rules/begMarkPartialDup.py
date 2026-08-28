# Catch beginning markers + partial reduplication of combined word, no-hyphen (Ex. nagma marites)
# Catches "nag", so we can split "ma" and check if it is a partial reduplication of "marites"

def begMarkPartialDupNoHyphen(tokenTempList, i, marker):
    if tokenTempList[i].lower().startswith(marker):
        return marker
    else:
        return ""