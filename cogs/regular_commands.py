#! python3

import random
import discord
import requests
import urllib
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from discord.ext import commands


# Regular commands
class RegularCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cryle-busch", help="Sends a fake crying Kyle Busch gif.")
    async def cryle_busch(self, ctx):
        await ctx.send("https://tenor.com/view/nascar-cry-kyle-busch-chicagoland-gif-12099166")

    @commands.command(name="roll_dice", help="Simulates rolling dice.")
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(", ".join(dice))

    @commands.command(name="wikirandom", help="Posts a random wikipedia page.")
    async def random_wiki(self, ctx):
        r = requests.head(
            "https://en.wikipedia.org/wiki/Special:Random", allow_redirects=True)
        await ctx.send(urllib.parse.unquote(r.url, encoding="utf-8"))

    @commands.command(name="covid", help="Displays current COVID-19 data. Defaults to global, country can be specified.")
    async def covid_data(self, ctx, location=None):

        location = '-'.join(location.lower().split(" "))

        # Adjusts the url to include the specified country, and includes some expected alternate inputs for the USA.
        if location:
            if location in ["america", "usa", "united-states"]:
                location = "us"
            elif location in ["uk", "united-kingdom"]:
                location = "uk"
            elif location in ["uae", "united-arab-emirates"]:
                location = "united-arab-emirates"
            elif location in ["drc", "dr-congo", "democratic-republic-of-the-congo", "democratic-republic-of-congo"]:
                location = "democratic-republic-of-the-congo"
            elif location in ["hong-kong", "hong-kong-sar", "china-hong-kong-sar"]:
                location = "china-hong-kong-sar"
            elif location in ["macao", "china-macao-sar"]:
                location = "china-macao-sar"
            elif location in ["falkland-islands", "falkland-islands", "malvinas", "falkland-islands-malvinas"]:
                location = "falkland-island-malvinas"
            elif location == "vietnam":
                location = "viet-nam"
            url = f'https://www.worldometers.info/coronavirus/country/{location}'
        else:
            url = "https://www.worldometers.info/coronavirus/"

        # Requests the data from Worldometers.info and checks for a 404 redirect.
        r = requests.get(url)
        if r.url == "https://www.worldometers.info/404.shtml":
            await ctx.send("That is not a valid country.")
        soup = BeautifulSoup(r.text, "html.parser")
        numbers = soup.findAll("div", {"class": "maincounter-number"})

        # Finds the numbers of Confirmed Cases, Confirmed Deaths, and Recovered Cases
        confirmed = numbers[0].find("span").text
        deaths = numbers[1].find("span").text
        recovered = numbers[2].find("span").text

        # Determines the title of the embed.
        if location:
            location = " ".join(location.split("-"))
            title = f'CURRENT COVID-19 DATA FOR {location.upper()}'
        else:
            title = "CURRENT GLOBAL COVID-19 DATA"

        # Builds the embed.
        covid_embed = discord.Embed(
            title=title,
            description=f'\n**Confirmed Cases:**  {confirmed}\n\n'
                        f'**Confirmed Deaths:** {deaths}\n\n'
                        f'**Recovered Cases:**  {recovered}\n\n',
            url=url,
            color=0xa3da50
        )
        covid_embed.set_footer(text="This data is taken from Worldometers",
                               icon_url="https://www.worldometers.info/favicon/apple-icon-180x180.png")

        # Sends the fully built embed to Discord.
        await ctx.send(embed=covid_embed)

    @commands.command(name="covid-news", help="Displays COVID-19 news. (Mixed, BBC, Reuters, NPR, The Hill)")
    async def covid_news(self, ctx, source="mixed"):

        # Checks the source against the dictionaries for expected misspellings, etc.
        source = source.lower()
        sources = {
            "mixed": ("mixed", "mix", "all"),
            "bbc": ("bbc"),
            "reuters": ("reuters", "reuter", "reuter's", "rueters", "rueter's"),
            "npr": ("npr"),
            "the hill": ("thehill", "the hill", "the-hill", "the_hill", "the")
        }
        for site, spelling in sources.items():
            if source in spelling:
                source = site

        # Lists the proper display names, urls, html tags, and colors to be used for the scraping and embedding.
        names = {
            "bbc": "BBC",
            "reuters": "Reuters",
            "npr": "NPR",
            "the hill": "The Hill"
        }
        urls = {
            "bbc": "https://www.bbc.com/news/coronavirus",
            "reuters": "https://www.reuters.com/live-events/coronavirus-6-id2921484",
            "npr": "https://www.npr.org/sections/coronavirus-live-updates",
            "the hill": "https://thehill.com/social-tags/coronavirus"
        }
        html_tags = {
            "bbc": ("h3", {"class": "lx-stream-post__header-title gel-great-primer-bold"}, "a"),
            "reuters": ("div", {"class": "FeedBox__container___3wxiT item-container LiveBlogStreamPage-post-3KSe2"}, "a"),
            "npr": ("div", {"class": "item-info"}, "a"),
            "the hill": ("h2", {"class": "node__title node-title"}, "a")
        }
        colors = {
            "mixed": 0xd22188,
            "bbc": 0xbb1919,
            "reuters": 0xfb8033,
            "npr": 0x237bbd,
            "the hill": 0x2a53c1
        }

        # Checks whether the feed being built will come from a single source or be a mixed feed from all sources.
        if source == "mixed":
            links = {}
            url = 'https://www.cdc.gov/coronavirus/2019-ncov/index.html'
            for site in urls:
                r = requests.get(urls[site])
                soup = BeautifulSoup(r.text, "html.parser")
                links[site] = soup.findAll(
                    html_tags[site][0], html_tags[site][1])
        else:
            url = urls[source]
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.findAll(html_tags[source][0], html_tags[source][1])

        # Makes the base Discord embed that the articles will be added to.
        covid_news_embed = discord.Embed(
            title=f"COVID-19 {source.upper()} LIVE NEWS",
            url=url,
            color=colors[source]
        )

        # Builds the news feed.
        if source == "mixed":
            for i in range(0, 10, len(urls)):
                for site in names:
                    try:
                        value_text = links[site][i].find(
                            html_tags[site][2]).text
                        value_link = urljoin(
                            urls[site],
                            links[site][i].find(
                                html_tags[site][2]).attrs["href"]
                        )
                        covid_news_embed.add_field(
                            name=names[site],
                            value=f'[{value_text}]({value_link})',
                            inline=False
                        )
                    except:
                        continue
        else:
            for i in range(min(10, len(links))):
                try:
                    value_text = links[i].find(html_tags[source][2]).text
                    value_link = urljoin(
                        urls[source],
                        links[i].find(html_tags[source][2]).attrs["href"]
                    )
                except:
                    continue

                covid_news_embed.add_field(
                    name=names[source],
                    value=f'[{value_text}]({value_link})',
                    inline=False
                )

        # Sends the fully built embed to Discord.
        await ctx.send(embed=covid_news_embed)

    @commands.command(name="gunpla-news", help="Displays the latest Gunpla news.")
    async def gunpla_news(self, ctx):

        # Requests the data from the Gundam.Info website
        url = f'https://en.gundam.info/news/gunpla.html'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        vertical_feed = soup.findAll(
            "div", {"class": "c-articleList__item--vertical"})
        horizontal_feed = soup.findAll(
            "div", {"class": "c-articleList__item--horizontal"})
        titles = soup.findAll("p", {"class": "c-articleList__mainTitle"})
        dates = soup.findAll("p", {"class": "c-articleList__mainDate"})

        # Constructs the base embed.
        gunpla_news_embed = discord.Embed(
            title=f"LATEST GUNPLA NEWS",
            url=url,
            color=0xfccf00
        )

        # Adds the articles from the feed of vertical cards to the embed.
        for i in range(len(vertical_feed)):
            title = titles[i].text
            params = vertical_feed[i].find("a").attrs["href"]
            value = f'[{title}](https://en.gundam.info{params})'
            gunpla_news_embed.add_field(
                name=dates[i].text,
                value=value,
                inline=False
            )

        # Adds the articles from the feed of horizontal cards to the embed.
        for i in range(len(horizontal_feed)):
            title = titles[i+len(vertical_feed)].text
            params = horizontal_feed[i].find("a").attrs["href"]
            value = f'[{title}](https://en.gundam.info{params})'
            gunpla_news_embed.add_field(
                name=dates[i+len(vertical_feed)].text,
                value=value,
                inline=False
            )

        # Sends the fully built embed to Discord.
        await ctx.send(embed=gunpla_news_embed)

    @commands.command(name="anime-news", help="Displays the latest anime news.")
    async def anime_news(self, ctx):

        # Requests the news page from MyAnimeList
        url = f'https://myanimelist.net/news'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        feed = soup.findAll("div", {"class": "news-unit clearfix rect"})
        times = soup.findAll("p", {"class": "info di-ib"})

        # Builds the base embed.
        anime_news_embed = discord.Embed(
            title=f"LATEST ANIME NEWS",
            url=url,
            color=0x2f52a2
        )

        # Adds the news articles to the embed, with a maximum limit of 10.
        for i in range(min(len(feed), 10)):
            title = feed[i].find("p").text.strip("\n")
            url = feed[i].find("a").attrs["href"]
            value = f'[{title}]({url})'
            anime_news_embed.add_field(
                name=times[i].text.split(" by ")[0],
                value=value,
                inline=False
            )

        # Sends the fully built embed to Discord.
        await ctx.send(embed=anime_news_embed)

    @commands.Cog.listener(name=None)
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")
