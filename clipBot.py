import discord
from discord.ext import commands
import logging
import os, subprocess
import config
from googleapiclient.discovery import build
from uploadGdrive import upload

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
async def gdrive(ctx):
    await ctx.send("https://drive.google.com/drive/u/1/folders/1SvBMA88yCqetZbf6ICxyZ47HkBX5n919")

@bot.command()
async def clip(ctx):
    video_types = ["mp4", "mov"]

    print("found one video")
    for attachment in ctx.message.attachments:
        if any(attachment.filename.lower().endswith(video) for video in video_types):
            await attachment.save(attachment.filename)

    
    await ctx.send("Please reply with a **title**")
    reply = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)
    title = reply.content
    
    filename = attachment.filename

    await ctx.send("Upload to youtube or google drive? (yt/gd)")
    reply = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)
    if "gd" in reply.content:
        drive_title = title + ".mp4"
        os.rename(filename, drive_title)
        await ctx.send('Uploading file. This can take a few minutes')

        fileId = upload(drive_title)

        await ctx.send('Uploaded file to {url}'.format(url='https://drive.google.com/open?id=' + fileId))

        os.remove(drive_title)

    else:
        await ctx.send("Please reply with **public**, **private** or **unlisted** for the video privacy settings, default is unlisted")
        reply = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)
        if "public" in reply.content:
            privacy = "public"
        elif "private" in reply.content:
            privacy = "private"
        else:
            privacy = "unlisted"

        await ctx.send("Uploading with title: **" + title + "**. This can take a few minutes")

        try:
            output = subprocess.check_output("youtube-upload --privacy='" + privacy + "' --title=\'" + title + "' " + filename, shell=True)
        except Exception as e:
            output = e.output

        if output.decode("utf-8") == "":
            await ctx.send("An error has occurred most likely I ran out of YT upload quotas, would you like to upload to Google Drive instead? (y/n)")
            reply = await bot.wait_for("message", check=author_check(ctx.author), timeout=30)
            if reply.content == "y":
                drive_title = title + ".mp4"
                os.rename(filename, drive_title)
                await ctx.send("Beginning upload to Google Drive")
                fileId = upload(drive_title)
                await ctx.send('Uploaded file to {url}'.format(url='https://drive.google.com/open?id=' + fileId))
                os.remove(drive_title)
            else:
                await ctx.send("Please wait a few hours until my quota is refilled")

        else:
            msg = "Upload Complete: https://www.youtube.com/watch?v=" + output.decode("utf-8")
            await ctx.send(msg)
            
        os.remove(filename)

bot.run(config.discord_token)