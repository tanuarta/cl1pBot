import discord
from discord.ext import commands
import logging
import os, subprocess
from googleapiclient.discovery import build
import config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot('!')

@bot.event
async def on_ready(): # When the bot starts
    print(f"Bot online and logged in as {bot.user}")

def author_check(author):
    return lambda ctx: ctx.author == author
    



@bot.command()
async def clip(ctx):
    video_types = ["mp4", "mov"]

    print("found one video")
    for attachment in ctx.message.attachments:
        if any(attachment.filename.lower().endswith(video) for video in video_types):
            await attachment.save(attachment.filename)

    await ctx.send("Please reply with a **title**")
    title = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)

    output = subprocess.check_output("youtube-upload --title=\'" + title.content + "' " + attachment.filename, shell=True)

    msg = "Upload Complete: https://www.youtube.com/watch?v=" + output.decode("utf-8")

    await ctx.message.channel.send(msg)

    os.remove(attachment.filename)
    return

@bot.command()
async def convo(ctx):
    await ctx.send("hey i only respond to my author, what is my author name")
    reply = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)
    await ctx.send("hi " + reply.content)


bot.run(config.discord_token)


"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('$hey'):
        dude = message.author.id
        await message.channel.send("i can only respond to my caller")
        
        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            if message.author.id == dude:
                await message.channel.send("hi caller")
            else:
                await message.channel.send("you are not my caller")

    
    if message.content.startswith('$suck'):
        await message.channel.send("sucky sucky")
"""