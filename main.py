import secrets
from functools import lru_cache
from typing import List
import hashlib
import urllib.request
import os


def rollDice(amount: int) -> List[int]:
    result: List[int] = []
    for i in range(amount):
        result.append(secrets.randbelow(6) + 1)
    return result


@lru_cache(1)
def getWordlist():
    WORDFILE = "./diceware.wordlist.asc"
    WORDFILEURL = "http://world.std.com/~reinhold/diceware.wordlist.asc"
    WORDFILEHASH = "3cd6164a99e95381f8620aec782a933545bcd5833fa331d267a6829f6665256e"

    data: str = ""
    if not os.path.isfile(WORDFILE):
        urllib.request.urlretrieve(WORDFILEURL, filename=WORDFILE)

    with open(WORDFILE, "r", encoding="utf-8") as myfile:
        data = myfile.read()

    dataList = data.split("\n")
    dataList = dataList[2:]
    dataList = dataList[:-12]

    #ideally would check pgp signature here
    assert(hashlib.sha256(data.encode("utf-8")).hexdigest() == WORDFILEHASH)
    assert(dataList[0][:5] == "11111")
    assert(dataList[-1][:5] == "66666")

    return dataList


def getWord():
    data: List[str] = getWordlist()

    diceStr = "".join(map(str, rollDice(5)))

    for s in data:
        if diceStr == s[:5]:
            return s[6:-1]

    print(diceStr)
    raise Exception(diceStr + " not found in file")


def getPassword(wordAmount: int = 4):
    result = ""
    for i in range(wordAmount):
        word = getWord().capitalize()
        result += word
    return result + str(secrets.randbelow(100))


print(getPassword())
