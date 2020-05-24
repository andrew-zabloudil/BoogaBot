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

    @commands.command(name='covidnews', help='Displays COVID-19 news. (Mixed, BBC, or Reuters)')
    async def covid_news(self, ctx, source=None):

        if source:
            source = source.lower()
        else:
            source = 'mixed'

        if source == 'bbc':
            url = 'https://www.bbc.com/news/coronavirus'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.findAll("a", {'class': 'qa-heading-link'})
            color = 0xbb1919

        elif source == 'reuters':
            url = 'https://www.reuters.com/live-events/coronavirus-6-id2921484'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            links = soup.findAll("div", {
                                 'class': 'FeedBox__container___3wxiT item-container LiveBlogStreamPage-post-3KSe2'})
            color = 0xfb8033

        elif source == 'mixed':
            urls = ['https://www.bbc.com/news/coronavirus',
                    'https://www.reuters.com/live-events/coronavirus-6-id2921484']
            links = []
            for url in urls:
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                links.append(soup.findAll("a", {'class': 'qa-heading-link'}))
                links.append(soup.findAll("div", {
                    'class': 'FeedBox__container___3wxiT item-container LiveBlogStreamPage-post-3KSe2'}))
            links = [item for item in links if item != []]
            color = 0x0073b1
        covid_news_embed = discord.Embed(
            title=f"COVID-19 {source.upper()} LIVE NEWS",
            url=url,
            color=color
        )

        if source == 'bbc' or source == 'reuters':
            for i in range(len(links)):
                if source == 'bbc':
                    name = 'BBC'
                    value = f'[{links[i].find("span").text}](https://www.bbc.com{links[i].attrs["href"]})'

                elif source == 'reuters':
                    name = 'Reuters'
                    value = f'[{links[i].find("a").text}]({links[i].find("a").attrs["href"]})'

                covid_news_embed.add_field(
                    name=name,
                    value=value,
                    inline=False
                )

        if source == "mixed":
            for i in range(0, 5):
                covid_news_embed.add_field(
                    name='BBC',
                    value=f'[{links[0][i].find("span").text}](https://www.bbc.com{links[0][i].attrs["href"]})',
                    inline=False
                )
                covid_news_embed.add_field(
                    name='Reuters',
                    value=f'[{links[1][i].find("a").text}]({links[1][i].find("a").attrs["href"]})',
                    inline=False
                )
        await ctx.send(embed=covid_news_embed)

    @commands.Cog.listener(name=None)
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')