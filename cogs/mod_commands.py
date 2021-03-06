#! python3

import discord
from discord.ext import commands


class ModCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create-channel', help='MOD: Creates new text channel.')
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx, channel_name='New-Channel'):
        """
        Creates a channel on the current server with a specified name,
        or New-Channel if none is given.
        """
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            await ctx.send(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)

    @commands.command(name='kick', help='MOD: Kicks the specified user.')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, user_name=None, reason=None):
        """
        Kicks the user and sends them a DM.
        If a reason is given, it will be included in the DM.
        """
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
        """
        Bans the user and sends them a DM.
        If a reason is given, it will be included in the DM.
        """
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
        """
        Assigns a role to a user.
        """
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

    @commands.command(name="remove-role", help="MOD: Give a user and a role to remove from them.")
    @commands.has_permissions(manage_roles=True)
    async def remove_role(self, ctx, user_name=None, new_role=None, reason=None):
        """
        Removes a role from a user.
        """
        if not user_name or not new_role:
            await ctx.send('You must input both a user and a role to remove.')

        else:
            role = [r for r in ctx.guild.roles if r.name == new_role]
            member = [m for m in ctx.guild.members if m.display_name == user_name]
            if role and member:
                role = role[0]
                member = member[0]
                await member.remove_roles(role, reason=reason)

                if not reason:
                    await ctx.send(f'The role {role.name} has been removed from {member.display_name}')
                else:
                    await ctx.send(f'The role {role.name} has been removed from {member.display_name} because {reason}.')

            else:
                await ctx.send('One or more inputs was invalid.')

    @commands.Cog.listener(name=None)
    async def on_command_error(self, ctx, error):
        """
        Lets the user know if they do not have a role required to use a command.
        """
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send("You do not have the correct role for this command.")
