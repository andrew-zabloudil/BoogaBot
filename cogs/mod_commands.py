#! python3

import discord
from discord.ext import commands


class ModCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-channel', help='MOD: Creates new text channel.')
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name='New-Channel'):
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

    @commands.command(name='kick', help='MOD: Kicks the specified user.')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user_name=None, reason=None):

        guild = ctx.guild

        if user_name:
            for member in guild.members:
                if user_name == member.display_name:
                    if reason:
                        await ctx.send(f'Kicked {user_name} for {reason}.')
                        await member.create_dm()
                        await member.dm_channel.send(f'You were kicked from {guild.name} for {reason}.')
                    else:
                        await ctx.send(f'Kicked {user_name}.')
                        await member.create_dm()
                        await member.dm_channel.send(f'You were kicked from {guild.name}.')
                    await member.kick(reason=reason)
                    return
            await ctx.send('That user does not exist.')
        else:
            await ctx.send('You must input a valid user.')

    @commands.command(name='ban', help='MOD: Bans the specified user.')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, user_name=None, reason=None, days=1):
        guild = ctx.guild

        if days > 7:
            days = 7

        if user_name:
            for member in guild.members:
                if user_name == member.display_name:
                    if reason:
                        await ctx.send(f'Banned {user_name} for {reason}.')
                        await member.create_dm()
                        await member.dm_channel.send(f'You were banned from {guild.name} for {reason}.')
                    else:
                        await ctx.send(f'Banned {user_name}.')
                        await member.create_dm()
                        await member.dm_channel.send(f'You were banned from {guild.name}.')
                    await member.ban(delete_message_days=days, reason=reason)
                    return
            await ctx.send('That user does not exist.')
        else:
            await ctx.send('You must input a valid user.')

    @commands.command(name="assign-role", help="MOD: Give a user and a role to assign to them.")
    @commands.has_permissions(manage_roles=True)
    async def assign_role(self, ctx, user_name=None, new_role=None, reason=None):
        if not user_name or not new_role:
            await ctx.send('You must input both a user and a role to assign.')

        else:
            guild = ctx.guild
            role = [r for r in guild.roles if r.name == new_role]
            member = [m for m in guild.members if m.display_name == user_name]
            if role and member:
                role = role[0]
                member = member[0]
                await member.add_roles(role, reason=reason)

                if not reason:
                    await ctx.send(f'{member.display_name} has been assigned the role of {role.name}.')
                else:
                    await ctx.send(f'{member.display_name} has been assigned the role of {role.name} because {reason}.')

            else:
                await ctx.send('One or more inputs was invalid.')
