![Cover image](images/cover.png)

`pipe|bot` is a Discord chatbot that allows you to chain multiple text commands
together with pipes (`|`). It also supports arbritrary subgrouping with
`{` and `}`.

## Installation
The standard bot can be added to your server with the following link:

I encourage any server owners to modify and self host the bot themselves, as
the bot was built to be easily extensible.

## Modification and development
This project is licensed under the Simplified BSD license. If modified and
publicly re-released, I ask that you change the name to avoid confusion.

A simple overview of the project files is as follows:
### main.py
The Discord bot itself. This is the file run to start the bot.

### text\_transform.py
The hand-written lexer, parser, and generator. The grand majority of the bot's
functionality is implemented here.

### commands.py
Data related to the bots commands, including aliases, descriptions, examples,
and the names of callbacks.

The end of the file has useful data structures and regex patterns related to
the commands.

### command\_funcs.py
The callback functions for each command.

### test.py
Hypothesis and Pytest tests, mostly focusing on the lexing / parsing /
generation stages.

