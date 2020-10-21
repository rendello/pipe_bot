#!/usr/bin/python3.8

import random
import math
import hashlib
import re


def uppercase(text, args):
    return text.upper()


def lowercase(text, args):
    return text.lower()


def swapcase(text, args):
    return text.swapcase()


def char_translate(text, chars, mapped_chars):
    translations = dict(zip(chars, mapped_chars))

    new_text = ""
    for char in text:
        try:
            new_text += translations[char]
        except KeyError:
            new_text += char

    return new_text


def light_blackletter(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    blackletter = "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"

    return char_translate(text, standard, blackletter)


def heavy_blackletter(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    blackletter = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"

    return char_translate(text, standard, blackletter)


def vapourwave(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    full = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"

    return char_translate(text, standard, full)


def leet(text, args):
    standard = "aeoltbgzs"
    leet = "43017862$"

    new_text = char_translate(text.lower(), standard, leet)

    return new_text.upper()


def redact(text, args):
    new_text = ""

    if args != []:
        redact_char = args[0]
    else:
        redact_char = "█"

    for char in text:
        if char.isalnum() or char == "'":
            new_text += redact_char
        else:
            new_text += char

    return new_text


def bold(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    bold = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"

    return char_translate(text, standard, bold)


def clap(text, args):
    """ Puts clap emojis between words. """

    if args != []:
        clap_str = args[0]
    else:
        clap_str = "👏"

    # empty split() splits on *any* whitespace
    words = text.split()
    clappy_text = f" {clap_str} ".join(words)

    return clappy_text


def mock(text, args):
    """ Alternates between upper and lower case randomly. Sequences of 3+ do
    not occur. """

    new_text = ""

    for char in text:
        new_text += random.choice((char.upper(), char.lower()))
        last_chars = "".join([c for c in new_text[-3:] if c.isalpha()])
        if last_chars.isupper() or last_chars.islower():
            new_text = new_text[:-1] + new_text[-1].swapcase()

    return new_text


def anagram(text, args):
    words = text.split()
    new_text = ""

    for word in words:
        new_word = [None] * len(word)
        indexes = list(range(len(word)))

        for char in word:
            index = random.choice(indexes)
            new_word[index] = char
            indexes.remove(index)

        new_text += f"{''.join(new_word)} "

    return new_text


def zalgo(text, args):
    def apply_diacritic(char):
        if char.isspace():
            return char

        # Chars in "Combining Diacritical Marks" Unicode block.
        combining_chars = [chr(n) for n in range(768, 878)]
        combining_char = random.choice(combining_chars)
        return char + combining_char

    frequency = 150 / len(text)
    sum_of_frequencies = 0
    new_text = ""

    for index, char in enumerate(text):
        if frequency >= 1:
            for i in range(0, math.floor(frequency)):
                char = apply_diacritic(char)
        else:
            sum_of_frequencies += frequency

        if sum_of_frequencies >= 1:
            for i in range(0, math.floor(sum_of_frequencies)):
                char = apply_diacritic(char)
            sum_of_frequencies = 0

        new_text += char

    return new_text


def get_hash(hash_type, text):
    h = hashlib.new(hash_type)
    h.update(text.encode())
    return h.hexdigest()


def md5(text, args):
    return get_hash("md5", text)


def sha256(text, args):
    return get_hash("sha256", text)


def hexidecimal(text, args):
    return text.encode("utf-8").hex()


# broken: left zeros not preserved
def binary(text, args):
    h = hexidecimal(text, [])
    return bin(int(h, 16))[2:].zfill(8)


##### Discord markdown

def bold(text, args):
    return f"**{text}**"


def italic(text, args):
    return f"*{text}*"


def underline(text, args):
    return f"__{text}__"


def spoiler(text, args):
    return f"||{text}||"


def code(text, args):
    return f"`{text}`"


def codeblock(text, args):
    if args != []:
        language = args[0]
    else:
        language = str()

    return f"```{language}\n{text}\n```"


def blockquote(text, args):
    return f"> {text}\n"
