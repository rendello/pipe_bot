#!/usr/bin/python3.8

import re

import discord

import commands
from text_transform import process_text
from config import key


client = discord.Client()

command_pattern = re.compile(commands.aliases_pattern_with_pipe)


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
        ctx.clean_content.lower().strip() in ["@pipebot", "@pipe|bot"]
        or client.user in ctx.mentions
    ):
        pass

    ##### Process pipe commands
    elif re.search(command_pattern, ctx.clean_content) is not None:
        await ctx.channel.send(process_text(ctx.clean_content))


client.run(key)
