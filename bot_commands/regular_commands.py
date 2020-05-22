#! python3

import random
import discord
import requests
import urllib
from bs4 import BeautifulSoup
from discord.ext import commands


# Regular commands
class RegularCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='roll_dice', help='Simulates rolling dice.')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(name='wikirandom', help='Posts a random wikipedia page.')
    async def random_wiki(self, ctx):
        r = requests.head(
            'https://en.wikipedia.org/wiki/Special:Random', allow_redirects=True)
        await ctx.send(urllib.parse.unquote(r.url, encoding='utf-8'))

    @commands.command(name="covid", help='Displays current COVID-19 data. Defaults to global, country can be specified.')
    async def covid_data(self, ctx, location=None):

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

    @commands.command(name='covidnews', help='Displays COVID-19 news from BBC.')
    async def covid_news(self, ctx):
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
