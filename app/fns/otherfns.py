
def textanalysis(txt):
    lines = txt.count("\r") + txt.count("\n") + 1
    res = {'lines': lines}

    txt2 = txt.replace("\r", "").replace("\n", "").replace(" ", "")
    res['characters (total)']  = len(txt2)

    txt3 = txt2.lower()
    for x in range(ord('a'), ord('z')+1):
        txt3 = txt3.replace(chr(x), "")
    res['letters']  = len(txt2) - len(txt3)

    txt4 = txt3
    for x in range(10):
        txt4 = txt4.replace(str(x), "")
    res['figures']  = len(txt3) - len(txt4)

    res['other characters'] = len(txt4)

    wtxt = txt.replace("\r", " ").replace("\n", " ")
    wdict = {}
    for w in wtxt.split(" "):
        wlen = len(w)
        if wlen == 0:
            continue
        elif wlen in wdict:
            wdict[wlen] += 1
        else:
            wdict[wlen] = 1

    res['words'] = sum(wdict.values())

    for x in sorted(wdict):
        if x>0:
            res[str(x) + ' letter words']= wdict[x]

    return res










