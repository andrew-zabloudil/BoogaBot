#! python3

import os
import random
import re
import requests
import urllib.parse
from bs4 import BeautifulSoup

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

# Regular commands


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
    await ctx.send(urllib.parse.unquote(r.url, encoding='utf-8'))


@bot.command(name="covid", help='Displays current COVID-19 data. Defaults to global, country can be specified.')
async def covid_data(ctx, location=None):

    if location:
        if location.lower() in ['america', 'usa', 'united states']:
            location = 'us'
        url = f'https://www.worldometers.info/coronavirus/country/{location.lower()}'
    else:
        url = 'https://www.worldometers.info/coronavirus/'

    r = requests.get(url)

    if r.url == 'https://www.worldometers.info/404.shtml':
        await ctx.send("That is not a valid country.")

    soup = BeautifulSoup(r.text, 'html.parser')
    numbers = soup.findAll("div", {'class': 'maincounter-number'})

    confirmed = numbers[0].find('span').text
    deaths = numbers[1].find('span').text
    recovered = numbers[2].find('span').text

    if location:
        title = f'CURRENT COVID-19 DATA FOR {location.upper()}'
    else:
        title = "CURRENT GLOBAL COVID-19 DATA"

    covid_embed = discord.Embed(
        title=title,
        description=f'\n**Confirmed Cases:**  {confirmed}\n\n'
                    f'**Confirmed Deaths:** {deaths}\n\n'
                    f'**Recovered Cases:**  {recovered}\n\n',
        url=url,
        color=0xb73131
    )
    covid_embed.set_footer(text='This data is taken from Worldometers',
                           icon_url='https://www.worldometers.info/favicon/apple-icon-180x180.png')

    await ctx.send(embed=covid_embed)


@bot.command(name='covidnews', help='Displays COVID-19 news from BBC.')
async def covid_news(ctx):
    url = 'https://www.bbc.com/news/coronavirus'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.findAll("a", {'class': 'qa-heading-link'})
    times = soup.findAll("span", {'class': 'qa-meta-time'})

    covid_news_embed = discord.Embed(
        title="COVID-19 BBC LIVE NEWS",
        url=url,
        color=0x2f89ef
    )
    for i in range(len(links)):
        value = f'[{links[i].find("span").text}](https://www.bbc.com{links[i].attrs["href"]})'
        covid_news_embed.add_field(
            name=f'{times[i].find("span").text} (UTC+1)',
            value=value,
            inline=False
        )

    await ctx.send(embed=covid_news_embed)

# Admin commands


@ bot.command(name='create-channel', help='ADMIN: Creates new text channel.')
@ commands.has_role('admin')
async def create_channel(ctx, channel_name='New-Channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


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

bot.run(TOKEN)
