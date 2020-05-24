#! python3

import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @ commands.command(name='create-channel', help='ADMIN: Creates new text channel.')
    @ commands.has_permissions(administrator=True)
    async def create_channel(self, ctx, channel_name='New-Channel'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)
