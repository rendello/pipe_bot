#!/usr/bin/python3.8

from copy import copy

from parse import toAST, Group
from commands import text_commands

bot_commands = {}
for tc in text_commands:
    for alias in tc["aliases"]:
        bot_commands[alias] = tc["command"]



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
                    text = bot_commands[command.alias](text)
                return text

        group = new_group


def process_text(text: str):
    AST = toAST(text)
    return generate(AST)


if __name__ == "__main__":
    print(process_text("Hello, {world! | zalgo | mock}, it's me {yeetus|redact}| vapor"))
    print(process_text("{hi | zalgo}hhhh hh | zalgo"))
    print(process_text("in {Soviet Russia|old}, car drives {you| zalgo | vaporwave} | clap ☭ | mock"))
    print(process_text("{Hello|zalgo}"))
    print(process_text("{Hello} jello|zalgo"))
    print(process_text("{jello|zalgo} h|mock"))
    print(process_text("{jello} h|mock|zalgo"))
    print(process_text(""))
    print(process_text("{}"))
