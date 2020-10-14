#!/usr/bin/python3.8

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Sequence, Optional, Union

import re
from colorama import Fore, Back, Style

import commands

# [ Generate a regex with all command names ]
command_aliases = [alias for tc in commands.text_commands for alias in tc['aliases']]  # type: ignore
command_aliases_pattern = fr"({'|'.join(command_aliases)})\b"

_ = [
    ("TEXT", r'\\(\n|.)'), # Escaped char.
    ("PIPE", "(\|)"),
    ("COMMA", "(,)"),
    ("BRACE_OPEN", "({)"),
    ("BRACE_CLOSED", "(})"),
    ("NEWLINE", r"(\n)"),
    ("WHITESPACE", r"(\s+)"),
    ("COMMAND", command_aliases_pattern),
    ("TEXT", r"(\S)"),
]
TOKENS = [(t[0],re.compile(t[1])) for t in _]


@dataclass
class Token:
    type_: str
    value: str
    line: int = 0
    column: int = 0
    char_index: int = 0


def tokenize(text) -> List[Token]:
    """ Tokenizes text. """

    def tokenize_single(text, line, column, char_index) -> Optional[Token]:
        """ Tokenizes a single token and returns. """

        for type_, pattern in TOKENS:
            match = pattern.match(text, pos=char_index)

            if match is not None:
                value = match.group(1)
                char_index = match.end()
                return Token(type_, value, line, column, char_index)

        return None

    tokens: List[Token] = []
    char_index = 0
    last_char = len(text) - 1

    line = 1
    column = 1
    line_start = 1  # Used to calculate column

    while char_index <= last_char:
        token = tokenize_single(text, line, column, char_index)

        if token is not None:

            # Unify characters into text. Doing it here using a single regex
            # pass to grab escaped characters.
            if token.type_ == "TEXT" and len(tokens) > 0 and tokens[-1].type_ == "TEXT":
                token.value = tokens[-1].value + token.value
                tokens.pop()

            tokens.append(token)
            char_index = token.char_index
            if token.type_ == "NEWLINE":
                line += 1
                line_start = char_index
            column = char_index - line_start + 1

    for token in tokens:
        print(token)
    return tokens


def t_print(tokens: Sequence[Token], show_key=False) -> None:
    """ Prints arbritrary tokens with unique colors. """

    foreground = (Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN,
        Fore.MAGENTA, Fore.WHITE)
    style = Style.BRIGHT, Style.NORMAL, Style.DIM

    color_map = {}

    for i, (token_type, _) in enumerate(TOKENS):
        # (Jumps through foreground colors, then loops back and uses second
        # style, et cetera. Enable show_key for visualization.)
        color_map[token_type] = (
            foreground[i % len(foreground)]
            + style[int(i / len(foreground)) % len(style)]
        )
        if show_key:
            print(color_map[token_type] + token_type + Style.RESET_ALL)

    for token in tokens:
        if token.type_ == "WHITESPACE":
            color = Back.GREEN
        else:
            color = color_map[token.type_]
        print(color + token.value + Style.RESET_ALL, end="")
    print()


class ParseError(Exception):
    pass


@dataclass
class Command:
    alias: str
    arguments: str


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0  # The only shared mutable state

    def peek(self, expected_types, offset=0) -> bool:
        """ Looks at tokens without consuming them. `expected_types` can be a single
        token name (string) or a collection of acceptable token names. """
        results: List[bool] = []
        if type(expected_types) not in [list, tuple]:
            expected_types = [expected_types]

        for expected_type in expected_types:
            if self.index + offset > len(self.tokens) - 1:  # (out of range.)
                results.append(False)
            elif expected_type == "ANY":
                results.append(True)
            else:
                assert any(expected_type in t for t in TOKENS), "expected_type doesn't exist."
                results.append(self.tokens[self.index + offset].type_ == expected_type)

        return (True in results)

    def consume(self, expected_type: str) -> Token:
        if self.peek(expected_type):
            # (Update index before returning, but use original for return)
            self.index += 1
            return self.tokens[self.index - 1]
        else:
            t = self.tokens[self.index]
            print(f"\n{t.line}, {t.column}: Expected {expected_type}, got {t.type_}")
            for token in self.tokens:
                if token.line == t.line:
                    color: str = Back.RED + Fore.YELLOW if token == t else ""
                    print(f"{color}{token.value}{Style.RESET_ALL}", end="")
            raise ParseError

    def consume_if_exists(self, expected_type: str) -> Optional[Token]:
        if self.peek(expected_type):
            return self.consume(expected_type)
        return None

    def parse_text(self):
        text = ""
        while True:
            text += self.consume("ANY").value
            if not self.peek(["WHITESPACE", "COMMA", "TEXT"]):
                break
        return text

    def parse_arguments(self):
        args = []
        while True:
            arg_text = ""
            while self.peek("TEXT"):
                arg_text += self.consume("TEXT").value
            args.append(arg_text)

            if not self.peek("COMMA"):
                break
        return args

    def parse_commands(self):
        commands: List[Command] = []

        self.consume("PIPE")
        self.consume_if_exists("WHITESPACE")
        self.consume("COMMAND")
        self.consume_if_exists("WHITESPACE")
        if self.peek("TEXT")

    def parse(self):
        text = ""
        while True:
            if self.peek("BRACE_CLOSED") or (self.index > len(self.tokens) - 1):
                return text
            if self.peek("TEXT"):
                text += self.parse_text()
            elif self.peek("BRACE_OPEN"):
                self.consume("BRACE_OPEN")
                text += self.parse()

            if self.peek("ANY"):
                self.consume("ANY")



tokens = tokenize("Hell\o cruel{ world, {I am Gaven | redact} and I see you | zalgo | caps")

t_print(tokens)

parser = Parser(tokens)
print(parser.parse())
