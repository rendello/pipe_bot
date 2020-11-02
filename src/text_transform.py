#!/usr/bin/python3.8

from __future__ import annotations
# ^ Allows classes to contain themselves

from dataclasses import dataclass
from typing import List, Tuple, Sequence, Optional, Union
from copy import copy
import re

import commands

##### GLOBAL STUFF

# A list of tokens is created with patterns to match on. All command aliases
# are combined into a big regex to match on.
_ = [
    ("TEXT", r'\\(\n|.)'), # Escaped char.
    ("PIPE", r"(\|)"),
    ("COMMA", "(,)"),
    ("BRACE_OPEN", "({)"),
    ("BRACE_CLOSED", "(})"),
    ("NEWLINE", r"(\n)"),
    ("WHITESPACE", r"(\s+)"),
    ("COMMAND", commands.aliases_pattern),
    ("TEXT", r"(\S)"),
]
TOKENS = [(t[0],re.compile(t[1], re.IGNORECASE)) for t in _]


##### EXCEPTION
class PipeBotError(Exception):
    """ Any Pipebot (lexing, parsing, generation) error will directly raise
    this with a custom message. """
    pass


##### TOKENIZER
@dataclass
class Token:
    type_: str
    value: str
    line: int = 0
    column: int = 0
    char_index: int = 0


async def token_verify(tokens: List[Token]):
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


async def tokenize(text) -> List[Token]:
    """ Tokenizes text. """

    async def tokenize_single(text, line, column, char_index) -> Optional[Token]:
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
        token = await tokenize_single(text, line, column, char_index)

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

    await token_verify(tokens)
    return tokens


##### PARSER

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
    """ Recursive decent parser.
    
    The class' only shared mutable state is the its index in the tokens list.
    
    The only method that should be called externally is `parse`. This method
    recurses into itself and returns an AST.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0  # The only shared mutable state

    async def peek(self, expected_types, offset=0) -> bool:
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

    async def consume(self, expected_type: str) -> Token:
        if await self.peek(expected_type):
            # (Update index before returning, but use original for return.)
            self.index += 1
            return self.tokens[self.index - 1]
        else:
            t = self.tokens[self.index]
            raise PipeBotError(f"\n{t.line}, {t.column}: Expected {expected_type}, got {t.type_}")

    async def consume_space(self) -> None:
        """ Consumes whitespace and newlines until none left. """

        while await self.peek(["WHITESPACE","NEWLINE"]):
            await self.consume(["WHITESPACE", "NEWLINE"])

    async def parse_text(self, break_chars=["BRACE_OPEN", "BRACE_CLOSED", "PIPE"]) -> str:
        text = ""
        while await self.peek("ANY") and not await self.peek(break_chars):
            text += (await self.consume("ANY")).value
        return text

    async def parse_arguments(self) -> List[str]:
        arguments = []

        while True:
            await self.consume_space()
            if await self.peek("ANY"):
                arguments.append(await self.parse_text(break_chars=["BRACE_OPEN", "BRACE_CLOSED", "PIPE", "COMMA"]))

                if await self.peek("COMMA"):
                    await self.consume("COMMA")
                    await self.consume_space()
                elif await self.peek(["BRACE_CLOSED", "PIPE"]):
                    break
                elif await self.peek("ANY"):
                    raise PipeBotError("Bad argument.")
            else:
                break  # (End of tokens.)
        return arguments

    async def parse_commands(self):
        commands: List[Command] = []

        while True:
            command = Command(alias="", arguments=[])
            await self.consume("PIPE")
            await self.consume_space()
            if not await self.peek("ANY"):  # end of tokens
                raise PipeBotError("Pipe character at the end of tokens.")

            await self.consume_space()

            command.alias = (await self.consume("COMMAND")).value

            await self.consume_space()
            if await self.peek(["TEXT", "COMMAND"]):
                command.arguments = await self.parse_arguments()
            elif await self.peek("COMMA"):
                raise PipeBotError("Unexpected comma after command.")
            commands.append(command)

            await self.consume_space()
            if not await self.peek("PIPE"):
                break

        return commands

    async def parse(self) -> Group:
        content: List[Union[Command,str]] = []
        commands: List[Command] = []

        if self.tokens == []:
            return Group([""], [])

        while (self.index < len(self.tokens)):
            if await self.peek("PIPE"):
                commands = await self.parse_commands()
            elif await self.peek("BRACE_OPEN"):
                await self.consume("BRACE_OPEN")
                content.append(await self.parse())
            elif await self.peek("BRACE_CLOSED"):
                await self.consume("BRACE_CLOSED")
                break
            elif await self.peek("ANY"):
                content.append(await self.parse_text())

        return Group(content, commands)


async def toAST(text) -> str:
    tokens = await tokenize(text)
    return await Parser(tokens).parse()


##### GENERATOR

async def generate(group: Group) -> str:
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
                new_group.content[i] = await generate(c)

                # (Combine all strings if no Groups are left)
                if all(isinstance(item, str) for item in new_group.content):
                    new_group.content = [str().join(new_group.content)]

            elif len(group.content) == 1:  # (is lone str)
                text = c.strip()
                for command in group.commands:
                    text = await commands.alias_map[command.alias.lower()]["callback"](text, command.arguments)
                return text

        group = new_group


async def process_text(text: str) -> str:
    try:
        AST = await toAST(text)
        res = await generate(AST)
        return res
    except PipeBotError as e:
        return f"`ERROR: {e}`"
