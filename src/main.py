#!/usr/bin/python3.8

import re

import discord

import commands
from text_transform import process_text
from config import key


async def safely_replace_substr(text, substr, new_substr):
    """ Replace substr with a safely escaped new_substr. """
    dangerous_chars = r"\{}|,"

    for c in dangerous_chars:
        new_substr = new_substr.replace(c, "\\" + c)

    return text.replace(substr, new_substr, 1)


async def grab_text(ctx, identifier, expected_id_type:str):
    """ Grabs the identifier to be used for certain functions:

        Identifier is ___ Returns ___
        1. a message ID   ->  the referenced message
        2. an @'ed user   ->  their last channel message
        3. empty          ->  the last channel message
    """
    assert expected_id_type in ["message", "user"]

    text = "Not found"
    if re.match("(\A\d{18}\Z)", identifier):
        # Text is a message or user ID

        if expected_id_type == "message":
            async for message in ctx.channel.history(limit=100):
                if identifier == str(message.id):
                    text = message.content
                    break
        elif expected_id_type == "user":
            async for message in ctx.channel.history(limit=100):
                if identifier == str(message.author.id):
                    text = message.content
                    break
    elif identifier.strip() == "":
        # Grab message directly before user's, regardless of jumps in channel history.
        history = await ctx.channel.history(limit=10).flatten()
        for i, message in enumerate(history):
            if ctx.id == message.id:
                text = history[i+1].content
                break
    else:
        raise Exception

    return text


##### Compiled regexes.
# "|zalgo", "| mock"; Not "| randomtext"
command_pattern = re.compile(commands.aliases_pattern_with_pipe)

# Matches the $LAST macro if it's not preceded directly by a backslash or some
# text. It also matches the user id, whether it be directly or in an @.
# See `test.py` for succeeding and failing examples.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The user ID. May be empty.
macro_last_pattern = re.compile(r"(?:[^\\\w]|^)(\$LAST(?:\s+<@!)?(?:\s*(\d{18})(?:>)?)?)")

# Matches the $MESSAGE macro in much in the same way as $LAST. Looks for
# message IDs instead of user IDs. If there's a message link and not an ID, it
# grabs the ID from the end of the link. Unlike $LAST, it won't match if there's
# no ID / link, as $MESSAGE on its own is semantically meaningless.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The message ID. Won't match if it doesn't exist.
macro_message_pattern = re.compile(r"(?:[^\\\w]|^)(\$MESSAGE\s+(?:https://discord.com/channels/\d{18}/\d{18}/)?(\d{18}))")


##### Bot callbacks.
client = discord.Client()


@client.event
async def on_ready():
    pass


@client.event
async def on_message(ctx):
    text = ctx.content

    ##### Ignore messages from self
    if ctx.author.id == client.user.id:
        return

    ##### Help message
    elif (
        ctx.clean_content.lower().strip() in ["@pipebot", "@pipe|bot"] # Helpful if nick changed.
        or client.user in ctx.mentions
    ):
        pass

    elif (re.search(command_pattern, text) is not None
        or any(macro in text for macro in ["$LAST", "$MESSAGE"])):
        # (At least one pipe+command or macro has been found.)

        ##### Replace $LAST and $MESSAGE macros
        # Macros are replaced with the given message's text, if possible. The
        # text itself will have special characters escaped. See start of file
        # for detailed explanation of the regexes.
        #
        # $LAST:  Last message in channel, or last message by a certain user
        # in the channel if a user ID or @ is given. Implicit if the message
        # starts with « | ».
        #
        # $MESSAGE: Message ID or link in same channel.

        if text.startswith("|"):
            text = "$LAST" + text

        for last_macro in macro_last_pattern.findall(text):
            last_text = await grab_text(ctx, last_macro[1], "user")
            text = await safely_replace_substr(text, last_macro[0], last_text)

        for message_macro in macro_message_pattern.findall(text):
            message_text = await grab_text(ctx, message_macro[1], "message")
            text = await safely_replace_substr(text, message_macro[0], message_text)

        ##### Process pipe commands
        await ctx.channel.send(await process_text(text))


if __name__ == "__main__":
    client.run(key)
