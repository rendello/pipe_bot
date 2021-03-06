# SPDX-License-Identifier: BSD-2-Clause

import re
import pathlib
import asyncio
import platform

import discord
import toml
import appdirs
if platform.system() == "OpenBSD":
    import openbsd

import commands
from text_transform import process_text


async def safely_replace_substr(text, substr, new_substr):
    """ Replace substr with a safely escaped new_substr. """
    dangerous_chars = r"\{}|,"

    for c in dangerous_chars:
        new_substr = new_substr.replace(c, "\\" + c)

    return text.replace(substr, new_substr, 1)


async def grab_message(ctx, identifier, expected_id_type: str):
    """ Grab a certain message, based on the parameters. """
    assert expected_id_type in ["message", "user"]

    result_message = None

    if re.match(r"(\A\d{18}\Z)", identifier):
        # Text is a message or user ID

        if expected_id_type == "message":
            async for message in ctx.channel.history(limit=500):
                if identifier == str(message.id):
                    result_message = message
                    break
        elif expected_id_type == "user":
            # If the person calling is looking for their own last message,
            # ignore the very last message they sent, which will be the calling
            # message itself. There is potential for a race condition, but it's
            # low-stakes.
            calling_message_found = False
            async for message in ctx.channel.history(limit=100):
                if identifier == str(message.author.id):
                    if identifier == str(ctx.author.id) and calling_message_found == False:
                        calling_message_found = True
                        continue
                    else:
                        result_message = message
                        break
    elif identifier.strip() == "":
        # Grab message directly before user's, regardless of jumps in channel history.
        history = await ctx.channel.history(limit=10).flatten()
        for i, message in enumerate(history):
            if ctx.id == message.id:
                result_message = history[i + 1]
                break
    else:
        raise Exception

    return result_message


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


async def clean_up_mentions(msg, text):
    """ Replace mentions with a non-pingning text equivelent. """

    for user in msg.mentions:
        text = text.replace(f"<@{user.id}>", f"@\u200b{user.display_name}")
        text = text.replace(
            f"<@!{user.id}>", f"@\u200b{user.display_name}"
        )  # Has nick set

    for role in msg.role_mentions:
        text = text.replace(f"<@&{role.id}>", f"@\u200b{role.name}")

    text = text.replace(f"@everyone", f"@\u200beveryone")
    text = text.replace(f"@here", f"@\u200bhere")

    return text


### USER HELP DATA ########################################################
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

##### Create help decription embeds for each command.
# Note: To generate each command's example output we have to run the command
# callback. Since the callbacks are asyncronous, they must be run with
# `async.run()`. `discord.Client()` expects to get the default inactive loop
# and starts using that, but `asyncio.run()` completely deletes the default
# loop, and the discord code fails. Hence why we save and reset the event loop
# here.
old_loop = asyncio.get_event_loop()
for alias in commands.all_aliases:
    command = commands.alias_map[alias]
    example = asyncio.run(process_text(command['example']))

    command_description = (
        f"{command['description']}\n\n"
        + f"**Aliases:**\n {', '.join([a for a in command['aliases']])}\n\n"
        + f"**Example:**\n{command['example']}\n{example}"
    )

    help_embeds[alias] = discord.Embed(
        title=f"**Command: `{alias}`**",
        description=command_description,
        color=0xFCF169,
    )
asyncio.set_event_loop(old_loop)

### COMPILED REGEXES ######################################################
# "|zalgo", "| mock"; Not "| randomtext"
command_pattern = re.compile(commands.aliases_pattern_with_pipe)

# Matches the $LAST macro if it's not preceded directly by a backslash or some
# text. It also matches the user id, whether it be directly or in an @.
# See `test.py` for succeeding and failing examples.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The user ID. May be empty.
macro_LAST_pattern = re.compile(
    r"(?:[^\\\w]|^)(\$LAST(?:\s+<@(?:!)?)?(?:\s*(\d{18})(?:>)?)?)",
    re.IGNORECASE
)

# Matches the $MESSAGE macro in much in the same way as $LAST. Looks for
# message IDs instead of user IDs. If there's a message link and not an ID, it
# grabs the ID from the end of the link. Unlike $LAST, it won't match if there's
# no ID / link, as $MESSAGE on its own is semantically meaningless.
#
# Group 0: Whole match, whitespace stripped. For text replacement.
# Group 1: The message ID. Won't match if it doesn't exist.
macro_MESSAGE_pattern = re.compile(
    r"(?:[^\\\w]|^)(\$MESSAGE\s+(?:https://discord\.com/channels/\d{18}/\d{18}/)?(\d{18}))",
    re.IGNORECASE
)

### BOT CALLBACKS #########################################################
client = discord.Client()


@client.event
async def on_ready():
    if platform.system() == "OpenBSD":
        openbsd.unveil("/etc/ssl/certs", "r")
        openbsd.unveil("/usr/local/lib/python3.8/", "r")
        openbsd.pledge("stdio inet dns prot_exec rpath")

    await client.loop.create_task(change_status_task())


@client.event
async def on_message(ctx):
    text = ctx.content.strip()

    ##### Ignore messages from self
    if ctx.author.id == client.user.id:
        return

    elif not (
        re.search(command_pattern, text) is None
        and re.search(macro_MESSAGE_pattern, text) is None
        and re.search(macro_LAST_pattern, text) is None
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

        LAST_macro_cache = {}
        MESSAGE_macro_cache = {}

        for LAST_macro in macro_LAST_pattern.findall(text):
            if LAST_macro[1] in LAST_macro_cache.keys():
                message_text = LAST_macro_cache[LAST_macro[1]]
            else:
                message = await grab_message(ctx, LAST_macro[1], "user")
                if message is None:
                    message_text = "`$LAST: Message not found.`"
                else:
                    message_text = await clean_up_mentions(message, message.content)
                    LAST_macro_cache[LAST_macro[1]] = message_text
            text = await safely_replace_substr(text, LAST_macro[0], message_text)

        for MESSAGE_macro in macro_MESSAGE_pattern.findall(text):
            if MESSAGE_macro[1] in MESSAGE_macro_cache.keys():
                message_text = MESSAGE_macro_cache[MESSAGE_macro[1]]
            else:
                message = await grab_message(ctx, MESSAGE_macro[1], "message")
                if message is None:
                    message_text = "`$MESSAGE: Message not found.`"
                else:
                    message_text = await clean_up_mentions(message, message.content)
                    MESSAGE_macro_cache[MESSAGE_macro[1]] = message_text
            text = await safely_replace_substr(text, MESSAGE_macro[0], message_text)

        ##### Process pipe commands
        processed_text = await process_text(text)
        clean_processed_text = await clean_up_mentions(ctx, processed_text)

        if clean_processed_text != "":
            max_response_length = min(2000, int(config["max_response_length"]))
            response_length = len(clean_processed_text)

            if response_length > max_response_length:
                await ctx.channel.send(f"`INFO: Response too long. {response_length}/{max_response_length}`")
            else:
                await ctx.channel.send(clean_processed_text)
        else:
            await ctx.channel.send(
                "`INFO: Cannot send an empty message. This usually occurs when using $LAST on an embed.`"
            )

    ##### Help messages
    elif text.lower().strip().startswith(f"<@!{client.user.id}>"):
        try:
            argument = text.lower().split()[1].strip()
            try:
                await ctx.channel.send(embed=help_embeds[argument])
            except KeyError:
                await ctx.channel.send(embed=help_embeds["unknown"])
        except IndexError:
            await ctx.channel.send(embed=help_embeds["basics"])


### BOT STARTUP ###########################################################
if __name__ == "__main__":

    # (Platform agnostic config file path.)
    config_dir = pathlib.Path(appdirs.user_config_dir("pipebot"))
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
            maxlen = input(
                "Max response length (max 2000): "
            ).strip()
            if isinstance(maxlen, int) and maxlen > 0 and maxlen < 2000:
                config["max_response_length"] = maxlen
            else:
                print("Defaulting to 2000")
                config["max_response_length"] = 2000
                

            config_dir.mkdir(parents=True, exist_ok=True)
            with open(config_file, "w+") as f:
                toml.dump(config, f)
        else:
            print("Quitting.")
