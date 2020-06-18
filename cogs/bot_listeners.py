import discord
from discord.ext import commands

import random


class BotListeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name=None)
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')

    @commands.Cog.listener(name=None)
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith("!"):
            return

        anime_gifs = [
            "https://tenor.com/view/really-anime-seriously-kiruya-momochi-karyl-anime-faces-gif-17024702",
            "https://tenor.com/view/cal-princess-connect-disgusting-cry-gif-16950076",
            "https://tenor.com/view/princess-connect-re-dive-anime-smile-thumbs-up-gif-17119800",
            "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-blushing-gif-16984580",
            "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984595",
            "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984597",
            "https://tenor.com/view/karyl-kyaru-princess-connect-re-dive-anime-gif-16984575"
        ]

        replies = {
            'ooga': 'Booga',
            'epic': 'WOW',
            'oof': 'Thanks for contributing nothing to the conversation.',
            'wow': 'EPIC',
            'animewasamistake': anime_gifs[random.randrange(0, len(anime_gifs))],
            '🐡': 'https://tenor.com/view/pufferfish-carrot-meme-stfu-funny-gif-15837792',
            '🐇': 'https://tenor.com/view/bunny-rabbit-eating-food-munchies-gif-17294792',
            '🐰': 'https://tenor.com/view/bunny-rabbit-eating-food-munchies-gif-17294792'
        }

        clean_message = ''.join(
            message.content.lower().strip('.?!¡¿').split(' '))
        if replies[clean_message]:
            await message.channel.send(replies[clean_message])
