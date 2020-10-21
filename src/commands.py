#!/usr/bin/python3.8

import command_funcs as cf

# See end of file for useful variables related to commands.

text_commands = [
    {
        "aliases": ["caps", "uppercase", "upper"],
        "args": [],
        "callback": cf.uppercase,
        "category": "basic",
        "description": "Uppercases text.",
        "example": {
            "input": "Hello, world! | upper",
            "output": "HELLO, WORLD!",
        },
    },
    {
        "aliases": ["lowercase", "lower"],
        "args": [],
        "callback": cf.lowercase,
        "category": "basic",
        "description": "Lowercases text.",
        "example": {
            "input": "Hello, WORLD! | lower",
            "output": "hello, world!",
        },
    },
    {
        "aliases": ["swapcase", "swap case", "swap"],
        "args": [],
        "callback": cf.swapcase,
        "category": "basic",
        "description": "Swaps the case of the text. Also see `mock`.",
        "example": {
            "input": "Hello, WORLD! | swapcase",
            "output": "hELLO, world!",
        },
    },
    {
        "aliases": ["clap", "clapback"],
        "args": ["emoji"],
        "callback": cf.clap,
        "category": "misc",
        "description": "Uppercases text and separates words with clapping emojis.",
        "example": {
            "input": "you are valid and so is this communication style | clap",
            "output": "YOU 👏 ARE 👏 VALID 👏 AND 👏 SO 👏 IS 👏 THIS 👏 COMMUNICATION 👏 STYLE",
        },
    },
    {
        "aliases": ["mock", "spongebob"],
        "args": [],
        "callback": cf.mock,
        "category": "misc",
        "description": "Randomly upper- and lowercases letters in text.",
        "examples": {
            "input": "This is a good thing. | mock",
            "output": "ThiS iS a GooD tHinG.",
        },
    },
    {
        "aliases": ["zalgo", "spooky"],
        "args": [],
        "callback": cf.zalgo,
        "category": "misc",
        "description": "Adds random combining characters to make text look crazy.",
        "examples": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["scramble"],
        "args": [],
        "callback": cf.anagram,
        "category": "misc",
        "description": "Scrambles all characters in their respective words.",
        "examples": {"input": "todo", "output": "todo",},
    },
    {
        "aliases": ["redact", "censor", "expunge"],
        "args": [],
        "callback": cf.redact,
        "category": "substitution",
        "description": "Replaces letters and numbers with a black block character.",
        "examples": {
            "input": "It's essential that you know [...]! | redact",
            "output": "████ █████████ ████ ███ ████ [...]!",
        },
    },
    {
        "aliases": ["vaporwave", "vapour", "vapor", "vapourwave", "fullwidth", "full"],
        "args": [],
        "callback": cf.vapourwave,
        "category": "substitution",
        "description": "Changes letters to their full-width equivalents.",
        "examples": {"input": "nice AESTHETICC | full", "output": "ｎｉｃｅ ＡＥＳＴＨＥＴＩＣＣ",},
    },
    {
        "aliases": ["leet", "haxxor", "hacker", "1337"],
        "args": [],
        "callback": cf.leet,
        "category": "substitution",
        "description": "Changes letters to their leet equivalents.",
        "examples": {
            "input": "Mess with the best, die like the rest. | leet",
            "output": "M3$$ WI7H 7H3 83$7, DI3 1IK3 7H3 R3$7.",
        },
    },
    {
        "aliases": ["blackletter", "gothic", "fraktur", "old"],
        "args": ["bold"],
        "callback": cf.light_blackletter,
        "category": "substitution",
        "description": "Changes letters to their old-timey equivalents.",
        "examples": {
            "input": "This is soooo legible | blackletter",
            "output": "𝔗𝔥𝔦𝔰 𝔦𝔰 𝔰𝔬𝔬𝔬𝔬 𝔩𝔢𝔤𝔦𝔟𝔩𝔢",
        },
    },
    {
        "aliases": ["hash"],
        "args": ["type"],
        "callback": cf.md5,
        "category": "cyber",
        "description": "Creates an MD5 hash from text.",
        "examples": {
            "input": "12345goodPa$$word | md5",
            "output": "b735c2f4ffa92fd7ed887bc423a7b3fd",
        },
    },
    {
        "aliases": ["hex", "hexidecimal"],
        "args": [],
        "callback": cf.hexidecimal,
        "category": "cyber",
        "description": "Gets the hex of the text.",
        "examples": {"input": "", "output": "",},
    },
    {
        "aliases": ["binary", "bin"],
        "args": [],
        "callback": cf.binary,
        "category": "cyber",
        "description": "Gets the binary of the text.",
        "examples": {"input": "", "output": "",},
    },
    {
        "aliases": ["bold", "embolden"],
        "args": [],
        "callback": cf.bold,
        "category": "markdown",
        "description": "Embolden text through Discord's markdown.",
        "examples": {"input": "Hello", "output": "**Hello**",},
    },
    {
        "aliases": ["italic", "italics", "italicize", "italicise"],
        "args": [],
        "callback": cf.italic,
        "category": "markdown",
        "description": "Italicize text through Discord's markdown.",
        "examples": {"input": "Hello", "output": "*Hello*",},
    },
    {
        "aliases": ["underline"],
        "args": [],
        "callback": cf.underline,
        "category": "markdown",
        "description": "Underline text through Discord's markdown.",
        "examples": {"input": "Hello", "output": "__Hello__",},
    },
    {
        "aliases": ["spoiler", "spoil", "spoilers", "spoilerz"],
        "args": [],
        "callback": cf.spoiler,
        "category": "markdown",
        "description": "Puts spoiler tags around the text.",
        "examples": {"input": "Clark Kent is Superman", "output": "||Clark Kent is Superman||",},
    },
    {
        "aliases": ["code"],
        "args": [],
        "callback": cf.code,
        "category": "markdown",
        "description": "Puts text in inline code tags.",
        "examples": {"input": "I64 i = 0", "output": "`I64 i = 0`",},
    },
    {
        "aliases": ["codeblock", "blockcode"],
        "args": ["language"],
        "callback": cf.codeblock,
        "category": "markdown",
        "description": "Puts text in code block.",
        "examples": {"input": "I64 i = 0;", "output": "```\nI64 i = 0\n```",},
    },
    {
        "aliases": ["blockquote", "quote", "quotation"],
        "args": [],
        "callback": cf.blockquote,
        "category": "markdown",
        "description": "Puts text in a blockquote.",
        "examples": {"input": "Hello", "output": "> Hello",},
    },
]


# Map of aliases and respective command functions.
#alias_command_map = {alias: tc["callback"] for tc in text_commands for alias in tc['aliases']}
alias_command_map = {alias: tc for tc in text_commands for alias in tc['aliases']}

# Aliases.
all_aliases = [alias for tc in text_commands for alias in tc['aliases']]
primary_aliases = [tc["aliases"][0] for tc in text_commands]

categories = [command["category"] for command in text_commands]

# Useful regex patterns (not compiled).
aliases_pattern = fr"\b({'|'.join(all_aliases)})\b"  # Matches "zalgo", "caps", etc.
aliases_pattern_with_pipe = fr"\|\s*{aliases_pattern}"  # Matches "|zalgo", "| caps", etc.
