#! python3

import os
import random
from dotenv import load_dotenv


import discord
from discord.ext import commands

from bot_commands import regular_commands
from bot_commands import admin_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TEST_TOKEN')
bot = commands.Bot(command_prefix='!')


# Bot Events

@ bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@ bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@ bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    replies = {
        'ooga': 'Booga',
        'epic': 'WOW',
        'oof': 'Thanks for contributing nothing to the conversation.'
    }

    anime_replies = [
        "https://tenor.com/view/really-anime-seriously-kiruya-momochi-karyl-anime-faces-gif-17024702",
        "https://tenor.com/view/cal-princess-connect-disgusting-cry-gif-16950076",
        "https://tenor.com/view/princess-connect-re-dive-anime-smile-thumbs-up-gif-17119800",
        "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-blushing-gif-16984580",
        "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984595",
        "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984597",
        "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984575"
    ]

    for reply_key in replies:
        if message.content.lower() == reply_key:
            await message.channel.send(replies[reply_key])
        elif ''.join(message.content.lower().split(' ')) == reply_key:
            await message.channel.send(replies[reply_key])

    if ''.join(message.content.lower().split(' ')) == "animewasamistake":
        await message.channel.send(anime_replies[random.randrange(0, len(anime_replies))])

    await bot.process_commands(message)

bot.add_cog(regular_commands.RegularCommands(bot))
bot.add_cog(admin_commands.AdminCommands(bot))
bot.run(TOKEN)
