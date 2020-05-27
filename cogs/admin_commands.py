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

    @commands.command(name='kick', help='ADMIN: Kicks the specified user.')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user_name=None, reason=None):
        guild = ctx.guild

        if user_name:
            for member in guild.members:
                if user_name == member.display_name:
                    await member.kick(reason=reason)
                    if reason:
                        await ctx.send(f'Kicked {user_name} for {reason}.')
                    else:
                        await ctx.send(f'Kicked {user_name}.')
                    return
            await ctx.send('That user does not exist.')
        else:
            await ctx.send('You must input a valid user.')

    @commands.command(name='ban', help='ADMIN: Bans the specified user.')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, user_name=None, reason=None, days=0):
        guild = ctx.guild

        if days > 7:
            days = 7

        if user_name:
            for member in guild.members:
                if user_name == member.display_name:
                    await member.ban(reason=reason, delete_message_days=days)
                    if reason:
                        await ctx.send(f'Banned {user_name} for {reason}.')
                    else:
                        await ctx.send(f'Banned {user_name}.')
                    return
            await ctx.send('That user does not exist.')
        else:
            await ctx.send('You must input a valid user.')
