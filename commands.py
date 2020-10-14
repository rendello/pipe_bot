#!/usr/bin/python3.8

import command_funcs as cf

# Many commands produce text that can't be capitalized by the regular functions,
# especially Unicode characters that look like regular Latin but are not.
# As such, commands are given a "buoyancy". Commands that change a text's case
# will silently sink down below commands that can not be capitalized on their own.
#
# ie. "upper → blackletter → mock" will silently become "upper →  mock → blackletter"
#
# -1 : Changes capitalization.
#  0 : Does not interact badly with capitalization.
#  1 : Interacts badly with capitalization.

text_commands = [
    {
        "aliases": ["caps", "uppercase", "upper"],
        "args": [],
        "command": cf.uppercase,
        "category": "basic",
        "help": "Uppercases text.",
        "example": {
            "input": "Hello, world! | upper",
            "output": "HELLO, WORLD!",
        },
    },
    {
        "aliases": ["lowercase", "lower"],
        "args": [],
        "command": cf.lowercase,
        "category": "basic",
        "help": "Lowercases text.",
        "example": {
            "input": "Hello, WORLD! | lower",
            "output": "hello, world!",
        },
    },
    {
        "aliases": ["swapcase", "swap case", "swap"],
        "args": [],
        "command": cf.swapcase,
        "category": "basic",
        "help": "Swaps the case of the text. Also see `mock`.",
        "example": {
            "input": "Hello, WORLD! | swapcase",
            "output": "hELLO, world!",
        },
    },
    {
        "aliases": ["clap", "clapback"],
        "args": ["emoji"],
        "command": cf.clap,
        "category": "misc",
        "help": "Uppercases text and separates words with clapping emojis.",
        "example": {
            "input": "you are valid and so is this communication style | clap",
            "output": "YOU 👏 ARE 👏 VALID 👏 AND 👏 SO 👏 IS 👏 THIS 👏 COMMUNICATION 👏 STYLE",
        },
    },
    {
        "aliases": ["mock", "spongebob"],
        "args": [],
        "command": cf.mock,
        "category": "misc",
        "help": "Randomly upper- and lowercases letters in text.",
        "examples": {
            "input": "This is a good thing. | mock",
            "output": "ThiS iS a GooD tHinG.",
        },
    },
    {
        "aliases": ["zalgo", "spooky"],
        "args": [],
        "command": cf.zalgo,
        "category": "misc",
        "help": "Adds random combining characters to make text look crazy.",
        "examples": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["anagram"],
        "args": [],
        "command": cf.anagram,
        "category": "misc",
        "help": "Scrambles all characters in their respective words.",
        "examples": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["redact", "censor", "expunge"],
        "args": [],
        "command": cf.redact,
        "category": "substitution",
        "help": "Replaces letters and numbers with a black block character.",
        "examples": {
            "input": "It's essential that you know [...]! | redact",
            "output": "████ █████████ ████ ███ ████ [...]!",
        },
    },
    {
        "aliases": ["vaporwave", "vapour", "vapor", "vapourwave", "fullwidth", "full"],
        "args": [],
        "command": cf.vapourwave,
        "category": "substitution",
        "help": "Changes letters to their full-width equivalents.",
        "examples": {"input": "nice AESTHETICC | full", "output": "ｎｉｃｅ ＡＥＳＴＨＥＴＩＣＣ",},
    },
    {
        "aliases": ["leet", "haxxor", "hacker", "1337"],
        "args": [],
        "command": cf.leet,
        "category": "substitution",
        "help": "Changes letters to their leet equivalents.",
        "examples": {
            "input": "Mess with the best, die like the rest. | leet",
            "output": "M3$$ WI7H 7H3 83$7, DI3 1IK3 7H3 R3$7.",
        },
    },
    {
        "aliases": ["blackletter", "gothic", "fraktur", "old"],
        "args": ["bold"],
        "command": cf.light_blackletter,
        "category": "substitution",
        "help": "Changes letters to their old-timey equivalents.",
        "examples": {
            "input": "This is soooo legible | blackletter",
            "output": "𝔗𝔥𝔦𝔰 𝔦𝔰 𝔰𝔬𝔬𝔬𝔬 𝔩𝔢𝔤𝔦𝔟𝔩𝔢",
        },
    },
    {
        "aliases": ["hash"],
        "args": ["type"],
        "command": cf.md5,
        "category": "cyber",
        "help": "Creates an MD5 hash from text.",
        "examples": {
            "input": "12345goodPa$$word | md5",
            "output": "b735c2f4ffa92fd7ed887bc423a7b3fd",
        },
    },
    {
        "aliases": ["hex", "hexidecimal"],
        "args": [],
        "command": cf.hexidecimal,
        "category": "cyber",
        "help": "Gets the hex of the text.",
        "examples": {"input": "", "output": "",},
    },
    {
        "aliases": ["bin", "binary"],
        "args": [],
        "command": cf.binary,
        "category": "cyber",
        "help": "Gets the binary of the text.",
        "examples": {"input": "", "output": "",},
    },
]
