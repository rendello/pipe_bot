#!/usr/bin/python3.8

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Sequence, Optional, Union

import re
from colorama import Fore, Back, Style

import commands

# [ Generate a regex with all command names ]
command_aliases = [alias for tc in commands.text_commands for alias in tc['aliases']]  # type: ignore
command_aliases_pattern = fr"\b({'|'.join(command_aliases)})\b"

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
    arguments: List[str]


@dataclass
class Group:
    """ An AST node.
    Text and groups are stored in order. Groups will be processed in the
    generation stage and combined with the text. The commands will be run in
    order* on the entire unified text (*command order will be re-arranged
    somewhat, see "buoyancy" comment in commands.py).
    """
    content: List[Union[str,Group]]
    commands: List[Command]

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

    def parse_text(self) -> str:
        text = ""
        while self.peek(["WHITESPACE", "COMMA", "TEXT"]):
            text += self.consume("ANY").value
        print(text)
        return text

    def parse_arguments(self) -> List[str]:
        arguments = []

        while True:
            arguments.append(self.consume("TEXT").value)
            self.consume_if_exists("WHITESPACE")
            if self.peek("COMMA"):
                self.consume("COMMA")
                self.consume_if_exists("WHITESPACE")
            else:
                break
        return arguments

    def parse_commands(self):
        commands: List[Command] = []

        while True:
            command = Command(alias="", arguments=[])
            self.consume("PIPE")
            self.consume_if_exists("WHITESPACE")
            command.alias = self.consume("COMMAND").value
            self.consume_if_exists("WHITESPACE")
            if self.peek("TEXT"):
                command.arguments = self.parse_arguments()
            commands.append(command)

            self.consume_if_exists("WHITESPACE")
            if not self.peek("PIPE"):
                break

        return commands

    def parse(self) -> Group:
        content: List[Union[Command,str]] = []
        commands: List[Command] = []
        #while not self.peek("BRACE_CLOSED") and (self.index < len(self.tokens) - 1):
        while (self.index < len(self.tokens) - 1):

            self.consume_if_exists("WHITESPACE")

            if self.peek("TEXT"):
                content.append(self.parse_text())
            elif self.peek("PIPE"):
                commands = self.parse_commands()
                self.consume_if_exists("BRACE_CLOSED")
                break;
            elif self.peek("BRACE_OPEN"):
                self.consume("BRACE_OPEN")
                content.append(self.parse())

        return Group(content, commands)



#tokens = tokenize("Hell\o cruel world, {I am \ {Gaven | zalgo orange} | redact bold, bolder} and I see you | zalgo bold | caps")
#tokens = tokenize("Hello, I'm {Gaven | zalgo caps} | french")
tokens = tokenize("I'm {named {the great | mock} Gaven | zalgo bold | lower} yo")
t_print(tokens, True)

parser = Parser(tokens)
print(parser.parse())
