import secrets
from functools import lru_cache
from typing import List
import hashlib
import urllib.request
import os


def roll_dice(amount: int) -> List[int]:
    """Rolls amount six sided dice"""
    result: List[int] = []
    for _ in range(amount):
        result.append(secrets.randbelow(6) + 1)
    return result


@lru_cache(1)
def get_wordlist():
    """Create word list"""
    WORDFILE = "./diceware.wordlist.asc"
    WORDFILEURL = "http://world.std.com/~reinhold/diceware.wordlist.asc"
    WORDFILEHASH = "3cd6164a99e95381f8620aec782a933545bcd5833fa331d267a6829f6665256e"

    data: str = ""
    if not os.path.isfile(WORDFILE):
        urllib.request.urlretrieve(WORDFILEURL, filename=WORDFILE)

    with open(WORDFILE, "r", encoding="utf-8") as myfile:
        data = myfile.read()

    data_list = data.split("\n")
    data_list = data_list[2:]
    data_list = data_list[:-12]

    #ideally would check pgp signature here
    assert hashlib.sha256(data.encode("utf-8")).hexdigest() == WORDFILEHASH
    assert data_list[0][:5] == "11111"
    assert data_list[-1][:5] == "66666"

    return data_list


def get_word():
    """Create word"""
    data: List[str] = get_wordlist()

    dice_str = "".join(map(str, roll_dice(5)))

    for s in data:
        if dice_str == s[:5]:
            return s[6:-1]

    print(dice_str)
    raise Exception(dice_str + " not found in file")


def get_password(word_amount: int = 4):
    """Create password"""
    result = ""
    for _ in range(word_amount):
        word = get_word().capitalize()
        result += word
    return result + str(secrets.randbelow(100))


print(get_password())
