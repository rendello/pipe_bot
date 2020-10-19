#!/usr/bin/python3.8

from text_transform import process_text
import discord

from config import key


client = discord.Client()

@client.event
async def on_ready():
    pass


@client.event
async def on_message(ctx):

    ##### Ignore messages from self
    if (ctx.author.id == client.user.id):
        return

    await ctx.channel.send(process_text(ctx.clean_content))


client.run(key)
