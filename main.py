#!/usr/bin/python3.8

from copy import copy

from parse import toAST, Group
from commands import text_commands

bot_commands = {}
for tc in text_commands:
    for alias in tc["aliases"]:
        bot_commands[alias] = tc["command"]



def generate(group: Group) -> str:

    while True:
    
        # The `content` of a Group is a mixed list of strings and Groups. If a
        # Group's only content is a single string, it's the deepest node on that
        # branch and can be processed.
        for i, c in enumerate(group.content):
            if isinstance(c, Group):
                new_group = copy(group)
                new_group.content[i] = generate(c)

                # (Combine all strings if no Groups are left)
                if all(isinstance(item, str) for item in new_group.content):
                    new_group.content = [str().join(new_group.content)]

                new_group

            elif len(group.content) == 1:  # (is lone str)
                text = c
                for command in group.commands:
                    text = bot_commands[command.alias](text)
                return text

        group = new_group


AST = toAST("Hello world! I am {Katie | zalgo | caps | mock}, destroyer of worlds! | mock | clap")
print(AST)
print("\n\n")
print(generate(AST))
