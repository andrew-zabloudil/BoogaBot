import os
import random
import discord
from discord.ext import commands


class BotListeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name=None)
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
        try:
            with open('change_log.txt', 'r') as change_log:
                changes = change_log.read()
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == "boogabot-updates":
                        await channel.send(changes)
            try:
                with open('change_log_history.txt', 'a') as history:
                    history.write(f'{changes}\n\n')
                with open('change_log.txt', 'w') as change_log:
                    change_log.write('')
            except:
                os.rename('change_log.txt', 'change_log_history.txt')
                with open('change_log.txt', 'w') as change_log:
                    change_log.write('')
        except:
            pass

    @commands.Cog.listener(name=None)
    async def on_message(self, message):
        """
        Automatically replies to certain messages.
        """
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
            '🐰': 'https://tenor.com/view/bunny-rabbit-eating-food-munchies-gif-17294792',
            '🧀': 'https://cdn.discordapp.com/emojis/716293527054843914.gif',
            '🧅': 'https://tenor.com/view/shrek-surprise-bathroom-ogre-gif-11492547',
            'f': f'{message.author.display_name} has paid respects.',
            'uhoh': 'Stinky.'
        }

        clean_message = ''.join(
            message.content.lower().strip('.?!¡¿').split(' ').split('-'))
        if clean_message in replies:
            await message.channel.send(replies[clean_message])
