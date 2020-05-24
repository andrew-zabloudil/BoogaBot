#! python3

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from cogs.regular_commands import RegularCommands
from cogs.admin_commands import AdminCommands
from cogs.bot_listeners import BotListeners

load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.getenv('DISCORD_TEST_TOKEN')
bot = commands.Bot(command_prefix='!')

bot.add_cog(RegularCommands(bot))
bot.add_cog(AdminCommands(bot))
bot.add_cog(BotListeners(bot))
bot.run(TOKEN)
