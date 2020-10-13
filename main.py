#!/usr/bin/python3.7

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Sequence, Optional, Union

from colorama import Fore, Back, Style

import re

_ = [
    ("TEXT", r'\\(\n|.)'), # Escaped char.
    ("DOUBLE_PIPE", "(\|\|)"),
    ("PIPE", "(\|)"),
    ("BRACE_OPEN", "({)"),
    ("BRACE_CLOSED", "(})"),
    ("NEWLINE", r"(\n)"),
    ("WHITESPACE", r"(\s+)"),
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
            tokens.append(token)

            char_index = token.char_index
            if token.type_ == "NEWLINE":
                line += 1
                line_start = char_index
            column = char_index - line_start + 1

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

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0  # The only shared mutable state

    def peek(self, expected_type, pos=0) -> bool:
        if self.index + pos > len(self.tokens) - 1:  # (out of range.)
            return False
        elif expected_type == "ANY":
            return True
        else:
            assert any(expected_type in t for t in TOKENS), "expected_type doesn't exist."
            return self.tokens[self.index + pos].type_ == expected_type

    def consume(self, expected_type: str) -> Optional[Token]:
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

    def parse_text(self):
        text = ""
        while True:
            text += self.consume("ANY").value
            if not self.peek("WHITESPACE") and not self.peek("TEXT"):
                break
        return text.strip()

    def parse(self):
        while self.index < len(self.tokens) - 1:
            if self.peek("TEXT"):
                print(self.parse_text())

            if self.peek("ANY"):
                token = self.consume("ANY")



tokens = tokenize("{is || a} test! \| tr\eat | me like disease")

t_print(tokens)

parser = Parser(tokens)
parser.parse()
