# SPDX-License-Identifier: BSD-2-Clause

from typing import List
import random
import math
import hashlib
import re
import base64

# Data #########################################################################
morse_map = [
    ("E̅E̅E̅E̅E̅E̅E̅E̅", "........"),
    ("I̅N̅T̅", "..-.-"),
    ("S̅O̅S̅", "...---..."),
    ("A̅A̅", ".-.-"),
    ("A̅R̅", ".-.-."),
    ("A̅S̅", ".-..."),
    ("B̅K̅", "-...-.-"),
    ("C̅L̅", "-·-··-··"),
    ("S̅N̅", "...-."),
    ("B̅T̅", "-...-"),
    ("C̅T̅", "-.-.-"),
    ("D̅O̅", "-··---"),
    ("K̅N̅", "-·--·"),
    ("S̅K̅", "···-·-"),
    ("A", ".-"),
    ("B", "-..."),
    ("C", "-.-."),
    ("D", "-.."),
    ("E", "."),
    ("F", "..-."),
    ("G", "--."),
    ("H", "...."),
    ("I", ".."),
    ("J", ".---"),
    ("K", "-.-"),
    ("L", ".-.."),
    ("M", "--"),
    ("N", "-."),
    ("O", "---"),
    ("P", ".--."),
    ("Q", "--.-"),
    ("R", ".-."),
    ("S", "..."),
    ("T", "-"),
    ("U", "..-"),
    ("V", "...-"),
    ("W", ".--"),
    ("X", "-..-"),
    ("Y", "-.--"),
    ("Z", "--.."),
    ("0", "-----"),
    ("1", ".----"),
    ("2", "..---"),
    ("3", "...--"),
    ("4", "....-"),
    ("5", "....."),
    ("6", "-...."),
    ("7", "--..."),
    ("8", "---.."),
    ("9", "----."),
    (".", ".-.-.-"),
    (",", "--..--"),
    ("?", "..--.."),
    ("'", ".----."),
    ("!", "-.-.--"),
    ("/", "-..-."),
    ("(", "-.--."),
    (")", "-.--.-"),
    ("&", ".-..."),
    (":", "---..."),
    (";", "-.-.-."),
    ("=", "-...-"),
    ("+", ".-.-."),
    ("-", "-....-"),
    ("_", "..--.-"),
    ('"', ".-..-."),
    ("$", "...-..-"),
    ("@", ".--.-."),
    ("¿", "..-.-"),
    ("¡", "--...-"),
    (" ", "/"),
]

### MISC. UTILITY FUNCTIONS ###############################################
async def char_translate(text, chars, mapped_chars):
    translations = dict(zip(chars, mapped_chars))

    new_text = ""
    for char in text:
        try:
            new_text += translations[char]
        except KeyError:
            new_text += char

    return new_text


async def get_hash(hash_type, text):
    h = hashlib.new(hash_type)
    h.update(text.encode())
    return h.hexdigest()


async def get_seperator(args: List[str]) -> str:
    if args == [] or args[0].lower() == "space":
        seperator = " "
    elif args[0].lower() == "none":
        seperator = ""
    else:
        seperator = args[0]
    return seperator


### CALLBACKS #############################################################
# Every command callback should:
#   - Be asyncronous
#   - Accept two arguments:
#     - Text to transform
#     - List of argument strings (even if it doesn't use them)
#   - Return transformed text

async def uppercase(text, args):
    return text.upper()


async def lowercase(text, args):
    return text.lower()


async def swapcase(text, args):
    return text.swapcase()


async def light_blackletter(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    blackletter = "𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷"

    return await char_translate(text, standard, blackletter)


async def heavy_blackletter(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    blackletter = "𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟"

    return await char_translate(text, standard, blackletter)


async def vapourwave(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    full = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"

    return await char_translate(text, standard, full)


async def double_struck(text, args):
    standard =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    blackboard = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"

    return await char_translate(text, standard, blackboard)


async def leet(text, args):
    standard = "aeoltbgzs"
    leet = "43017862$"

    new_text = await char_translate(text.lower(), standard, leet)

    return new_text.upper()


async def redact(text, args):
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


async def serif(text, args):
    standard = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    bold = "𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳"

    return await char_translate(text, standard, bold)


async def upside_down(text, args):
    standard = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ud = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄Z"

    return await char_translate(text, standard, ud)


async def clap(text, args):
    """ Puts clap emojis between words. """

    if args != []:
        clap_str = args[0]
    else:
        clap_str = "👏"

    words = text.split(" ")
    clappy_text = f" {clap_str} ".join(words)

    return clappy_text


async def mock(text, args):
    """ Alternates between upper and lower case randomly. Sequences of 3+ do
    not occur. """

    new_text = ""

    for char in text:
        new_text += random.choice((char.upper(), char.lower()))
        last_chars = "".join([c for c in new_text[-3:] if c.isalpha()])
        if last_chars.isupper() or last_chars.islower():
            new_text = new_text[:-1] + new_text[-1].swapcase()

    return new_text


async def anagram(text, args):
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


async def zalgo(text, args):
    async def apply_diacritic(char):
        if char.isspace():
            return char

        # Chars in "Combining Diacritical Marks" Unicode block.
        combining_chars = [chr(n) for n in range(768, 878)]
        combining_char = random.choice(combining_chars)
        return char + combining_char

    if len(text) != 0:
        frequency = 150 / len(text)
    else:
        frequency = 0

    sum_of_frequencies = 0
    new_text = ""

    for index, char in enumerate(text):
        if frequency >= 1:
            for i in range(0, math.floor(frequency)):
                char = await apply_diacritic(char)
        else:
            sum_of_frequencies += frequency

        if sum_of_frequencies >= 1:
            for i in range(0, math.floor(sum_of_frequencies)):
                char = await apply_diacritic(char)
            sum_of_frequencies = 0

        new_text += char

    return new_text


async def md5(text, args):
    return await get_hash("md5", text)


async def sha256(text, args):
    return await get_hash("sha256", text)


async def hexidecimal(text, args):
    seperator = await get_seperator(args)

    hexstr = text.encode("utf-8").hex()
    hexstr = seperator.join([hexstr[i:i+2] for i in range(0, len(hexstr), 2)])

    return hexstr


async def from_hexidecimal(text, args):
    text = "".join([char if char in "0123456789abcdef" else "" for char in text.lower()])
    decoded = bytes.fromhex(text).decode('utf-8')
    return decoded


async def binary(text, args):
    seperator = await get_seperator(args)

    return seperator.join(format(x, 'b') for x in bytearray(text, 'utf-8'))


async def to_base64(text, args):
    return base64.standard_b64encode(text.encode()).decode()


async def from_base64(text, args):
    return base64.b64decode(text).decode()


##### Discord markdown

async def bold(text, args):
    return f"**{text}**"


async def italic(text, args):
    return f"*{text}*"


async def underline(text, args):
    return f"__{text}__"


async def spoiler(text, args):
    return f"||{text}||"


async def code(text, args):
    return f"`{text}`"


async def codeblock(text, args):
    if args != []:
        language = args[0]
    else:
        language = str()

    return f"```{language}\n{text}\n```"


async def blockquote(text, args):
    return f"\n> {text}\n"


##### Misc
async def uwu(text, args):
    """ Warning: cursed. """
    replacements = [("r","w"), ("R", "W"), ("l", "w"), ("L", "W"), ("no", "nyo"), ("No", "Nyo"), ("NO", "NYO"), ("I", "i")]

    for r in replacements:
        text = text.replace(r[0], r[1])
    return text


async def faux_cyrillic(text, args):
    transliterations = [
        (["BI", "BL"], ["Ы"]),
        (["LO", "IO"], ["Ю"]),
        (["B"], ["Ь","В"]),
        (["G"], ["Б"]),
        (["R"], ["Я"]),
        (["T"], ["Г"]),
        (["A"], ["Д"]),
        (["X"], ["Ж", "Х"]),
        (["E"], ["З", "Э"]),
        (["N"], ["Й", "И", "Л", "П"]),
        (["K"], ["К"]),
        (["H"], ["Н"]),
        (["P"], ["Р"]),
        (["C"], ["С"]),
        (["Y"], ["У", "Ч"]),
        (["O", "Q"], ["Ф", "Φ"]),
        (["U"], ["Ц", "Џ"]),
        (["W"], ["Ш", "Щ"]),
        (["F"], ["Ғ"])
    ]
    text = text.upper()
    for t in transliterations:
        for latin_str in t[0]:
            for occurence in range(0, text.count(latin_str)):
                text = text.replace(latin_str, random.choice(t[1]), 1)
    return text


async def to_morse(text, args):
    text_index = 0
    morse_text = ""

    caps_text = text.upper()
    while text_index <= len(caps_text):
        for pattern, morse_pattern in morse_map:
            if caps_text.startswith(pattern, text_index):
                text_index += len(pattern) - 1
                morse_text += morse_pattern + " "
        else:
            text_index += 1
    return morse_text


async def from_morse(text, args):
    latin_text = ""
    sections = text.split()
    for section in sections:
        for latin_pattern, morse_pattern in morse_map:
            if section == morse_pattern:
                latin_text += latin_pattern
                break
        else:
            latin_text += "[?]"

    return latin_text
