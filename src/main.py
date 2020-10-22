#!/usr/bin/python3.8

import re

import discord

import commands
from text_transform import process_text
from config import key


client = discord.Client()

##### Compiled regexes.
# "|zalgo", "| mock"; Not "| randomtext"
command_pattern = re.compile(commands.aliases_pattern_with_pipe)

# Matches the $LAST macro if it's not preceded directly by a backslash or some
# text. It also matches the user id, whether it be directly or in an @.
# See `test.py` for succeeding and failing examples.
#
# Group 1: Whole match, whitespace stripped. For text replacement.
# Group 2: The user ID. May be empty.
macro_last_pattern = re.compile(r"(?:[^\\\w]|^)(\$LAST(?:\s+<@!)?(?:\s*(\d{18})(?:>)?){0,1})")

# Matches the $MESSAGE macro in much in the same way as $LAST. Looks for
# message IDs instead of user IDs. If there's a message link and not an ID, it
# grabs the ID from the end of the link. Unlike $LAST, it won't match if there's
# no ID / link, as $MESSAGE on its own is semantically meaningless.
#
# Group 1: Whole match, whitespace stripped. For text replacement.
# Group 2: The message ID. Won't match if it doesn't exist.
macro_message_pattern = re.compile(r"(?:[^\\\w]|^)(\$MESSAGE\s+(?:https://discord.com/channels/\d{18}/\d{18}/)?(\d{18}))")


##### Bot callbacks.
@client.event
async def on_ready():
    pass


@client.event
async def on_message(ctx):

    ##### Ignore messages from self
    if ctx.author.id == client.user.id:
        return

    ##### Help message
    elif (
        ctx.clean_content.lower().strip() in ["@pipebot", "@pipe|bot"] # Helpful if nick changed.
        or client.user in ctx.mentions
    ):
        pass

    ##### Process pipe commands
    elif re.search(command_pattern, ctx.clean_content) is not None:
        # (At least one pipe+command has been found.)
        text = ctx.clean_content

        ##### Replace $LAST and $MESSAGE macros.
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
            print("WOW")

        #for message_macro in macro_message_pattern.findall(text):

        await ctx.channel.send(await process_text(text))


if __name__ == "__main__":
    client.run(key)
