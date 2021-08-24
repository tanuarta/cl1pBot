import discord
import logging
import os, subprocess
from googleapiclient.discovery import build
import config

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$clip'):
        video_types = ["mp4"]

        print("found one video")
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(video) for video in video_types):
                await attachment.save(attachment.filename)
        
        fp = open('temp.txt', 'w')
        output = os.popen("youtube-upload --title=\'" + attachment.filename + "' " + attachment.filename).read()
        fp.write(output)
        fp.close()

        fp = open('temp.txt', 'r')
        lines = fp.readlines() 


        msg = 'temp lol'
        for line in lines:
            if 'URL' in line:
                await message.channel.send(line)

        


client.run(config.discord_token)