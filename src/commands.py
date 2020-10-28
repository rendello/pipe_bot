#!/usr/bin/python3.8

from typing import List
import command_funcs as cf

# Due to their inherent structure, commands can't be easily organized in any
# given way. The existence of multiple aliases per command makes things messy.
# As such, they are stored in this flat dictionary for ease of creation, and
# a number of convenient mappings are provided at the end of this file.

# aliases: A list of aliases to used to call the function. The first alias is
#     the primary one, and will be automatically used in all documentation.
# callback: The callback function. See `command_funcs.py`.
# category: self-explanatory.
# description: A short description. Describes the processed text, not the
#    action taken, ie. "Scrambled characters", not "Scrambles characters".
# example: A full example of the command on some text. Can include args.

text_commands = [
    {
        "aliases": ["caps", "uppercase", "upper"],
        "callback": cf.uppercase,
        "category": "basic",
        "description": "Uppercase",
        "example": {
            "input": "Hello, world! | upper",
            "output": "HELLO, WORLD!",
        },
    },
    {
        "aliases": ["lowercase", "lower"],
        "callback": cf.lowercase,
        "category": "basic",
        "description": "Lowercase",
        "example": {
            "input": "Hello, WORLD! | lower",
            "output": "hello, world!",
        },
    },
    {
        "aliases": ["swapcase", "swap case", "swap"],
        "callback": cf.swapcase,
        "category": "basic",
        "description": "Swapped case per letter",
        "example": {
            "input": "Hello, WORLD! | swapcase",
            "output": "hELLO, world!",
        },
    },
    {
        "aliases": ["clap", "clapback"],
        "callback": cf.clap,
        "category": "misc",
        "description": "Emojis between words (default 👏)",
        "example": {
            "input": "you are valid and so is this communication style | clap",
            "output": "YOU 👏 ARE 👏 VALID 👏 AND 👏 SO 👏 IS 👏 THIS 👏 COMMUNICATION 👏 STYLE",
        },
    },
    {
        "aliases": ["mock", "spongebob"],
        "callback": cf.mock,
        "category": "misc",
        "description": "Random upper/lowercase",
        "example": {
            "input": "This is a good thing. | mock",
            "output": "ThiS iS a GooD tHinG.",
        },
    },
    {
        "aliases": ["zalgo", "spooky"],
        "callback": cf.zalgo,
        "category": "misc",
        "description": "Spooky zalgo text",
        "example": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["scramble"],
        "callback": cf.anagram,
        "category": "misc",
        "description": "Scrambled characters",
        "example": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["redact", "censor", "expunge"],
        "callback": cf.redact,
        "category": "substitution",
        "description": "Letters substituted for character (default █).",
        "example": {
            "input": "It's essential that you know [...]! | redact",
            "output": "████ █████████ ████ ███ ████ [...]!",
        },
    },
    {
        "aliases": ["vaporwave", "vapour", "vapor", "vapourwave", "fullwidth", "full"],
        "callback": cf.vapourwave,
        "category": "substitution",
        "description": "CJK full width letters",
        "example": {"input": "nice AESTHETICC | full", "output": "ｎｉｃｅ ＡＥＳＴＨＥＴＩＣＣ",},
    },
    {
        "aliases": ["leet", "haxxor", "hacker", "1337"],
        "callback": cf.leet,
        "category": "substitution",
        "description": "Elite hacker text",
        "example": {
            "input": "Mess with the best, die like the rest. | leet",
            "output": "M3$$ WI7H 7H3 83$7, DI3 1IK3 7H3 R3$7.",
        },
    },
    {
        "aliases": ["blackletter", "gothic", "fraktur", "old"],
        "callback": cf.light_blackletter,
        "category": "substitution",
        "description": "Old timey blackletter",
        "example": {
            "input": "This is soooo legible | blackletter",
            "output": "𝔗𝔥𝔦𝔰 𝔦𝔰 𝔰𝔬𝔬𝔬𝔬 𝔩𝔢𝔤𝔦𝔟𝔩𝔢",
        },
    },
    {
        "aliases": ["serif", "cowboy", "western"],
        "callback": cf.serif,
        "category": "substitution",
        "description": "Unicode serif font",
        "example": {
            "input": "Howdy there, pardner. | serif",
            "output": "𝐇𝐨𝐰𝐝𝐲 𝐭𝐡𝐞𝐫𝐞, 𝐩𝐚𝐫𝐝𝐧𝐞𝐫.",
        },
    },
    {
        "aliases": ["upsidedown", "upside-down", "upside_down", "australia", "flip", "flipped"],
        "callback": cf.upside_down,
        "category": "substitution",
        "description": "Unicode upside-down font",
        "example": {
            "input": "I love living in Australia | upside-down",
            "output": "I loʌǝ lᴉʌᴉuƃ ᴉu ∀nsʇɹɐlᴉɐ",
        },
    },
    {
        "aliases": ["md5", "hash"],
        "callback": cf.md5,
        "category": "cyber",
        "description": "MD5 hash",
        "example": {
            "input": "12345goodPa$$word | md5",
            "output": "b735c2f4ffa92fd7ed887bc423a7b3fd",
        },
    },
    {
        "aliases": ["sha256"],
        "callback": cf.sha256,
        "category": "cyber",
        "description": "SHA256 hash",
        "example": {
            "input": "12345goodPa$$word | sha256",
            "output": "4b89ce08630dc13be855658e9152d47dd1762800f7825d010018e02d3a67c6ae",
        },
    },
    {
        "aliases": ["hex", "hexidecimal"],
        "callback": cf.hexidecimal,
        "category": "cyber",
        "description": "Hexidecimal representation",
        "example": {"input": "", "output": "",},
    },
    {
        "aliases": ["from_hex", "from_hexidecimal", "fhex"],
        "callback": cf.from_hexidecimal,
        "category": "cyber",
        "description": "Text from hexidecimal",
        "example": {"input": "", "output": "",},
    },
    {
        "aliases": ["binary", "bin"],
        "callback": cf.binary,
        "category": "cyber",
        "description": "Binary representation",
        "example": {"input": "", "output": "",},
    },
    {
        "aliases": ["base64","b64","base_64"],
        "callback": cf.to_base64,
        "category": "cyber",
        "description": "Base64 encoded",
        "example": {"input": "", "output": "",},
    },
    {
        "aliases": ["from_base64","from_b64", "fb64"],
        "callback": cf.from_base64,
        "category": "cyber",
        "description": "Text from base 64",
        "example": {"input": "", "output": "",},
    },
    {
        "aliases": ["bold", "embolden"],
        "callback": cf.bold,
        "category": "markdown",
        "description": "Bold",
        "example": {"input": "Hello", "output": "**Hello**",},
    },
    {
        "aliases": ["italic", "italics", "italicize", "italicise"],
        "callback": cf.italic,
        "category": "markdown",
        "description": "Italics",
        "example": {"input": "Hello", "output": "*Hello*",},
    },
    {
        "aliases": ["underline"],
        "callback": cf.underline,
        "category": "markdown",
        "description": "Underline",
        "example": {"input": "Hello", "output": "__Hello__",},
    },
    {
        "aliases": ["spoiler", "spoil", "spoilers", "spoilerz"],
        "callback": cf.spoiler,
        "category": "markdown",
        "description": "Spoiler tag",
        "example": {"input": "Clark Kent is Superman", "output": "||Clark Kent is Superman||",},
    },
    {
        "aliases": ["code"],
        "callback": cf.code,
        "category": "markdown",
        "description": "Inline code tag",
        "example": {"input": "I64 i = 0", "output": "`I64 i = 0`",},
    },
    {
        "aliases": ["codeblock", "blockcode"],
        "callback": cf.codeblock,
        "category": "markdown",
        "description": "Code block",
        "example": {"input": "I64 i = 0;", "output": "```\nI64 i = 0\n```",},
    },
    {
        "aliases": ["blockquote", "quote", "quotation"],
        "callback": cf.blockquote,
        "category": "markdown",
        "description": "Block quote",
        "example": {"input": "Hello", "output": "> Hello",},
    },
    {
        "aliases": ["uwu", "owo"],
        "callback": cf.uwu,
        "category": "misc",
        "description": "Cursed UwU text",
        "example": {"input": "Hello", "output": "> Hewwo",},
    },
]


# Map of aliases to their respective command dicts.
alias_map = {alias: tc for tc in text_commands for alias in tc['aliases']}

# Unique categories in alphabetical order.
categories: List[str] = sorted(set([command["category"] for command in text_commands]))

# Aliases.
all_aliases: List[str] = [alias for tc in text_commands for alias in tc['aliases']]
primary_aliases: List[str] = [tc["aliases"][0] for tc in text_commands]

# Primary aliases, in alphabetical order, per category.
primary_aliases_per_category = {}
for c in categories:

    cat_aliases = []
    for a in primary_aliases:
        if alias_map[a]["category"] == c:
            cat_aliases.append(a)

    primary_aliases_per_category[c] = sorted(cat_aliases, key=str.lower)

# Useful regex patterns (not compiled).
aliases_pattern = fr"\b({'|'.join(all_aliases)})\b"  # Matches "zalgo", "caps", etc.
aliases_pattern_with_pipe = fr"\|\s*{aliases_pattern}"  # Matches "|zalgo", "| caps", etc.
