#! python3

import os
import random
from dotenv import load_dotenv


import discord
from discord.ext import commands

from bot_commands import regular_commands
from bot_commands import admin_commands
from bot_commands import bot_listeners

load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = os.getenv('DISCORD_TEST_TOKEN')
bot = commands.Bot(command_prefix='!')


bot.add_cog(regular_commands.RegularCommands(bot))
bot.add_cog(admin_commands.AdminCommands(bot))
bot.add_cog(bot_listeners.BotListeners(bot))
bot.run(TOKEN)
