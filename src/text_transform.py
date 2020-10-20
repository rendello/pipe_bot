#!/usr/bin/python3.8

from __future__ import annotations
# ^ Allows classes to contain themselves

from dataclasses import dataclass
from typing import List, Tuple, Sequence, Optional, Union
from copy import copy
import re

from colorama import Fore, Back, Style

import commands

# ====== GLOBAL STUFF ======

# A list of tokens is created with patterns to match on. All command aliases
# are combined into a big regex to match on.
_ = [
    ("TEXT", r'\\(\n|.)'), # Escaped char.
    ("PIPE", "(\|)"),
    ("COMMA", "(,)"),
    ("BRACE_OPEN", "({)"),
    ("BRACE_CLOSED", "(})"),
    ("NEWLINE", r"(\n)"),
    ("WHITESPACE", r"(\s+)"),
    ("COMMAND", commands.aliases_pattern),
    ("TEXT", r"(\S)"),
]
TOKENS = [(t[0],re.compile(t[1], re.IGNORECASE)) for t in _]


# ====== EXCEPTIONS ======
class PipeBotError(Exception):
    pass


# ====== TOKENIZER ======
@dataclass
class Token:
    type_: str
    value: str
    line: int = 0
    column: int = 0
    char_index: int = 0


def token_verify(tokens: List[Token]):
    brace_value = 0

    for token in tokens:
        if token.type_ == "BRACE_OPEN":
            brace_value += 1
        elif token.type_ == "BRACE_CLOSED":
            brace_value -= 1

        if brace_value < 0:
            raise PipeBotError("Unbalanced curly braces.")

    if brace_value != 0:
        raise PipeBotError("Unbalanced curly braces.")


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

    token_verify(tokens)
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


# ====== PARSER ======

@dataclass
class Command:
    alias: str
    arguments: List[str]


@dataclass
class Group:
    """ An AST node.
    Text and groups are stored in order. Groups will be processed in the
    generation stage and combined with the text. The commands will be run in
    order on the entire unified text.
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
            for token in self.tokens:
                if token.line == t.line:
                    color: str = Back.RED + Fore.YELLOW if token == t else ""
                    print(f"{color}{token.value}{Style.RESET_ALL}", end="")
            raise PipeBotError(f"\n{t.line}, {t.column}: Expected {expected_type}, got {t.type_}")

    def consume_if_exists(self, expected_type: str) -> Optional[Token]:
        if self.peek(expected_type):
            return self.consume(expected_type)
        return None

    def parse_text(self) -> str:
        text = ""
        while self.peek("ANY") and not self.peek(["BRACE_OPEN", "BRACE_CLOSED", "PIPE"]):
            text += self.consume("ANY").value
        return text

    def parse_arguments(self) -> List[str]:
        arguments = []

        while True:
            arguments.append(self.consume("TEXT").value)
            self.consume_if_exists("WHITESPACE")
            if self.peek("COMMA"):
                self.consume("COMMA")
                self.consume_if_exists("WHITESPACE")
            elif self.peek("BRACE_CLOSED"):
                break
            else:
                raise PipeBotError("Bad argument.")
        return arguments

    def parse_commands(self):
        commands: List[Command] = []

        while True:
            command = Command(alias="", arguments=[])
            self.consume("PIPE")
            if not self.peek("ANY"):  # end of tokens
                raise PipeBotError("Pipe character at the end of tokens.")

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

        if self.tokens == []:
            return Group([""], [])

        while (self.index < len(self.tokens)):
            if self.peek("PIPE"):
                commands = self.parse_commands()
            elif self.peek("BRACE_OPEN"):
                self.consume("BRACE_OPEN")
                content.append(self.parse())
            elif self.peek("BRACE_CLOSED"):
                self.consume("BRACE_CLOSED")
                break
            elif self.peek("ANY"):
                content.append(self.parse_text())


        return Group(content, commands)


def toAST(text) -> str:
    tokens = tokenize(text)
    return Parser(tokens).parse()


# ====== GENERATOR ======

def generate(group: Group) -> str:
    """ Recursively generates text from the AST. """

    while True:
        # The `content` of a Group is a mixed list of strings and Groups. If a
        # Group's only content is a single string, it's the deepest node on that
        # branch and can be processed.

        if group.content == []:
            return str()

        new_group = copy(group)
        for i, c in enumerate(group.content):
            if isinstance(c, Group):
                new_group.content[i] = generate(c)

                # (Combine all strings if no Groups are left)
                if all(isinstance(item, str) for item in new_group.content):
                    new_group.content = [str().join(new_group.content)]

            elif len(group.content) == 1:  # (is lone str)
                text = c
                for command in group.commands:
                    text = commands.alias_command_map[command.alias.lower()](text, command.arguments)
                return text

        group = new_group


def process_text(text: str) -> str:
    try:
        AST = toAST(text)
        res = generate(AST)
        return res
    except PipeBotError as e:
        return f"`ERROR: {e}`"
