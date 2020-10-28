#!/usr/bin/python3.8

import re
from pathlib import Path
import asyncio

import discord
import toml

import commands
from text_transform import process_text
import appdirs


async def safely_replace_substr(text, substr, new_substr):
    """ Replace substr with a safely escaped new_substr. """
    dangerous_chars = r"\{}|,"

    for c in dangerous_chars:
        new_substr = new_substr.replace(c, "\\" + c)

    return text.replace(substr, new_substr, 1)


async def grab_text(ctx, identifier, expected_id_type: str):
    """ Return the text of a previous message, based on parameters.

        Identifier is ___ Returns ___
        1. a message ID   ->  the referenced message
        2. an @'ed user   ->  their last channel message
        3. empty          ->  the last channel message
    """
    assert expected_id_type in ["message", "user"]

    text = "`INFO: Not found`"

    if re.match(r"(\A\d{18}\Z)", identifier):
        # Text is a message or user ID

        if expected_id_type == "message":
            async for message in ctx.channel.history(limit=1000):
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
                text = history[i + 1].content
                break
    else:
        raise Exception

    return text


async def change_status_task():
    """ Replaces the status at 15 second intervals.  """

    uncommon_statuses = [
        "Start a message with « | » to use the last message's text!",
        "Use $LAST to get the last channel message. It accepts usernames too!",
        "Use $MESSAGE with a message link or ID to use that message's text!",
    ]

    while True:
        for command_alias in commands.primary_aliases:
            statuses = [
                f'Try typing "| {command_alias}"!',
                "I do meme-y text transformations! @ me for help!",
                f'Try the "{command_alias}" command!',
            ]
            for status in statuses:
                await client.change_presence(activity=discord.Game(status))
                await asyncio.sleep(15)
                await client.change_presence(
                    activity=discord.Game("@pipe|bot for help")
                )
                await asyncio.sleep(10)

        for status in uncommon_statuses:
            await client.change_presence(activity=discord.Game(status))
            await asyncio.sleep(30)


##### User help data
basic_description = """
pipe|bot runs text through commands and posts the results. Run a command by \
appending it to your message with the pipe character, « | ».

"**Hello, world! | uppercase**" will give you "**HELLO, WORLD!**"
"**Hello, world! | mock**" will give you "**hElLo, woRLd!**"

You can chain together as many commands as you would like:

"**Hello, world! | caps | zalgo | italics**" gives "**H͓̒͘E̜͒͜L̷̥ͥL͔̠̖Ǫ̼ͧ,̪̺͢ W̸̪͠Ǫ͛̀R̞̻̣L̶͑̇D̷͓͛**"

You can run sub-groups between curly braces:

"**Hello, {world! | redact}**" gives "**Hello, █████!**"

`@pipe|bot ADVANCED` for advanced usage.
`@pipe|bot COMMANDS` for command breakdown.
`@pipe|bot <command>` for details on a specific command.
"""

advanced_description = """
pipe|bot can use the text of previous messages with $LAST and $MESSAGE.

$LAST is replaced with the text of the last message in the channel. It can also
take a @mention or an ID, and use that person's last channel message.

$MESSAGE is similar, but requires a message link or ID.

With both $LAST and $MESSAGE, the message text is escaped, so characters such
as pipes and curly braces won't interfere with the current operations.

As a convenience, a $LAST is implied if a message starts with « | ».
"""

unknown_description = """
Unknown argument. Valid commands:

`@pipe|bot` for basic help,
`@pipe|bot ADVANCED` for advanced usage.
`@pipe|bot COMMANDS` for a list of commands.
`@pipe|bot <command>` for details on a specific command.
"""

commands_description = """
`@pipe|bot <command>` for details on a specific command.
"""
for category, aliases in commands.primary_aliases_per_category.items():
    commands_description += f"\n**{category.upper()}**\n"
    for alias in aliases:
        commands_description += f"{alias}, "


help_embeds = {}

help_embeds["basics"] = discord.Embed(
    title="**Basic Usage of pipe|bot**", description=basic_description, color=0xFCF169
)
help_embeds["advanced"] = discord.Embed(
    title="**Advanced Usage of pipe|bot**",
    description=advanced_description,
    color=0xFCF169,
)
help_embeds["commands"] = discord.Embed(
    title="**pipe|bot Commands**", description=commands_description, color=0xFCF169
)
help_embeds["unknown"] = discord.Embed(
    title="**Unknown Argument**", description=unknown_description, color=0xFCF169
)

for alias in commands.all_aliases:
    command = commands.alias_map[alias]
    command_description = (
        f"{command['description']}\n\n**Example:**\n"
        + f"{command['example']['input']}\n>> {command['example']['output']}"
    )

    help_embeds[alias] = discord.Embed(
        title=f"**Command: `{alias}`**",
        description=command_description,
        color=0xFCF169,
    )


##### Compiled regexes.
# "|zalgo", "| mock"; Not "| randomtext"
command_pattern = re.compile(commands.aliases_pattern_with_pipe)

# Matches the $LAST macro if it's not preceded directly by a backslash or some
# text. It also matches the user id, whether it be directly or in an @.
# See `test.py` for succeeding and failing examples.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The user ID. May be empty.
macro_last_pattern = re.compile(
    r"(?:[^\\\w]|^)(\$LAST(?:\s+<@(?:!)?)?(?:\s*(\d{18})(?:>)?)?)"
)

# Matches the $MESSAGE macro in much in the same way as $LAST. Looks for
# message IDs instead of user IDs. If there's a message link and not an ID, it
# grabs the ID from the end of the link. Unlike $LAST, it won't match if there's
# no ID / link, as $MESSAGE on its own is semantically meaningless.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The message ID. Won't match if it doesn't exist.
macro_message_pattern = re.compile(
    r"(?:[^\\\w]|^)(\$MESSAGE\s+(?:https://discord.com/channels/\d{18}/\d{18}/)?(\d{18}))"
)


##### Bot callbacks.
client = discord.Client()


@client.event
async def on_ready():
    await client.loop.create_task(change_status_task())


@client.event
async def on_message(ctx):
    text = ctx.content

    ##### Ignore messages from self
    if ctx.author.id == client.user.id:
        return

    elif re.search(command_pattern, text) is not None or any(
        macro in text for macro in ["$LAST", "$MESSAGE"]
    ):
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

    ##### Help messages
    ltext = text.lower().strip()

    if ltext.startswith(f"<@!{client.user.id}>"):
        try:
            argument = ltext.split()[1].strip()
        except IndexError:
            await ctx.channel.send(embed=help_embeds["basics"])

        try:
            await ctx.channel.send(embed=help_embeds[argument])
        except KeyError:
            await ctx.channel.send(embed=help_embeds["unknown"])


if __name__ == "__main__":

    # (Platform agnostic config file path.)
    config_dir = Path(appdirs.user_config_dir("pipebot"))
    config_file = config_dir.joinpath("config.toml")

    try:
        with open(config_file, "r") as f:
            config = toml.load(f)
        client.run(config["key"])

    except FileNotFoundError:
        print(f'No config found at "{config_file}"')
        if "y" in input("Create one? [y/n]: ").lower():
            config = {}
            config["key"] = input("Discord bot key: ").strip()
            config["max_response_length"] = input(
                "Max response length (max 2000): "
            ).strip()

            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_file, "w+") as f:
                toml.dump(config, f)
        else:
            print("Quitting.")
