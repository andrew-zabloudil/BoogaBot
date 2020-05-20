#! python3

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}! Welcome to the server!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    replies = {'ooga': 'BOOGA', 'epic': 'WOW', 'wow': 'WOWZERS'}

    for key in replies:
        if message.content.lower() == key:
            response = replies[key]
            await message.channel.send(response)

client.run(TOKEN)
