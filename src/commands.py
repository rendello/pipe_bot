#!/usr/bin/python3.8

from typing import List
import command_funcs as cf

### TEXT COMMANDS #########################################################
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
        "example": "Hello, world! | upper"
    },
    {
        "aliases": ["lowercase", "lower"],
        "callback": cf.lowercase,
        "category": "basic",
        "description": "Lowercase",
        "example": "Hello, WORLD! | lower"
    },
    {
        "aliases": ["swapcase", "swap case", "swap"],
        "callback": cf.swapcase,
        "category": "basic",
        "description": "Swapped case per letter",
        "example": "Hello, WORLD! | swapcase"
    },
    {
        "aliases": ["clap", "clapback"],
        "callback": cf.clap,
        "category": "misc",
        "description": "Emojis between words (default 👏)",
        "example": "you are valid and so is this communication style | clap"
    },
    {
        "aliases": ["mock", "spongebob"],
        "callback": cf.mock,
        "category": "misc",
        "description": "Random upper/lowercase",
        "example": "This is a good thing. | mock"
    },
    {
        "aliases": ["zalgo", "spooky"],
        "callback": cf.zalgo,
        "category": "misc",
        "description": "Spooky zalgo text",
        "example": "He comes | zalgo"
    },
    {
        "aliases": ["scramble"],
        "callback": cf.anagram,
        "category": "misc",
        "description": "Scrambled characters",
        "example": "Uhhhh this is fine"
    },
    {
        "aliases": ["redact", "censor", "expunge"],
        "callback": cf.redact,
        "category": "substitution",
        "description": "Letters substituted for character (default █).",
        "example": "It's essential that you know {this important thing|redact}!"
    },
    {
        "aliases": ["vaporwave", "vapour", "vapor", "vapourwave", "fullwidth", "full"],
        "callback": cf.vapourwave,
        "category": "substitution",
        "description": "CJK full width letters",
        "example": "nice AESTHETICC | vapourwave"
    },
    {
        "aliases": ["leet", "haxxor", "hacker", "1337"],
        "callback": cf.leet,
        "category": "substitution",
        "description": "Elite hacker text",
        "example": "Mess with the best, die like the rest. | leet"
    },
    {
        "aliases": ["blackletter", "gothic", "fraktur", "old"],
        "callback": cf.light_blackletter,
        "category": "substitution",
        "description": "Old timey blackletter",
        "example": "This is soooo legible | blackletter"
    },
    {
        "aliases": ["serif", "cowboy", "western"],
        "callback": cf.serif,
        "category": "substitution",
        "description": "Unicode serif font",
        "example": "Howdy there, pardner. | serif"
    },
    {
        "aliases": ["upside-down", "upsidedown", "upside_down", "australia", "flip", "flipped"],
        "callback": cf.upside_down,
        "category": "substitution",
        "description": "Unicode upside-down font",
        "example": "I love living in Australia | upside-down"
    },
    {
        "aliases": ["md5", "hash"],
        "callback": cf.md5,
        "category": "cyber",
        "description": "MD5 hash",
        "example": "hunter2 | md5"
    },
    {
        "aliases": ["sha256"],
        "callback": cf.sha256,
        "category": "cyber",
        "description": "SHA256 hash",
        "example": "hunter2 | sha256"
    },
    {
        "aliases": ["hex", "hexidecimal"],
        "callback": cf.hexidecimal,
        "category": "cyber",
        "description": "Hexidecimal representation",
        "example": "Hello world | hex"
    },
    {
        "aliases": ["from_hex", "from_hexidecimal", "fhex"],
        "callback": cf.from_hexidecimal,
        "category": "cyber",
        "description": "Text from hexidecimal",
        "example": ""
    },
    {
        "aliases": ["binary", "bin"],
        "callback": cf.binary,
        "category": "cyber",
        "description": "Binary representation",
        "example": "Hello world | bin"
    },
    {
        "aliases": ["base64","b64","base_64"],
        "callback": cf.to_base64,
        "category": "cyber",
        "description": "Base64 encoded",
        "example": "Hello world | base64"
    },
    {
        "aliases": ["from_base64","from_b64", "fb64"],
        "callback": cf.from_base64,
        "category": "cyber",
        "description": "Text from base 64",
        "example": ""
    },
    {
        "aliases": ["bold", "embolden"],
        "callback": cf.bold,
        "category": "markdown",
        "description": "Bold",
        "example": "This is {bold|bold}"
    },
    {
        "aliases": ["italic", "italics", "italicize", "italicise"],
        "callback": cf.italic,
        "category": "markdown",
        "description": "Italics",
        "example": "Wow, look at me | italics"
    },
    {
        "aliases": ["underline"],
        "callback": cf.underline,
        "category": "markdown",
        "description": "Underline",
        "example": "This has a line underneath it | underline"
    },
    {
        "aliases": ["spoiler", "spoil", "spoilers", "spoilerz"],
        "callback": cf.spoiler,
        "category": "markdown",
        "description": "Spoiler tag",
        "example": "Clark Kent is Superman | spoiler"
    },
    {
        "aliases": ["code"],
        "callback": cf.code,
        "category": "markdown",
        "description": "Inline code tag",
        "example": "I64 i = 0 | code"
    },
    {
        "aliases": ["codeblock", "blockcode"],
        "callback": cf.codeblock,
        "category": "markdown",
        "description": "Code block",
        "example": "I64 i = 0; | codeblock",
    },
    {
        "aliases": ["blockquote", "quote", "quotation"],
        "callback": cf.blockquote,
        "category": "markdown",
        "description": "Block quote",
        "example": "Hello | blockquote"
    },
    {
        "aliases": ["uwu", "owo"],
        "callback": cf.uwu,
        "category": "misc",
        "description": "Cursed UwU text",
        "example": "Hello world | uwu"
    },
]

### USEFUL COMMAND GROUPINGS ##############################################
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
