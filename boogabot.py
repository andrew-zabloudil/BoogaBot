#! python3

import os
import random
import requests
import urllib.parse

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# Regular commands


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


@bot.command(name='wikirandom', help='Posts a random wikipedia page.')
async def random_wiki(ctx):
    r = requests.head(
        'https://en.wikipedia.org/wiki/Special:Random', allow_redirects=True)
    await ctx.send(print(urllib.parse.unquote(r.url, encoding='utf-8')))

# Admin commands


@ bot.command(name='create-channel')
@ commands.has_role('admin')
async def create_channel(ctx, channel_name='New-Channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


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

bot.run(TOKEN)
