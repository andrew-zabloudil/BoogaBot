#! python3
"""
This file creates the bot item for BoogaBot.
All commands are located in the files found in the cogs folder.
"""
import os
import discord
from discord.ext import commands

from cogs.regular_commands import RegularCommands
from cogs.mod_commands import ModCommands
from cogs.bot_listeners import BotListeners

TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))

bot.add_cog(RegularCommands(bot))
bot.add_cog(ModCommands(bot))
bot.add_cog(BotListeners(bot))

bot.run(TOKEN)
