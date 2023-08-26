import asyncio
import nextcord
from nextcord.ext import commands
from nextcord.ext.commands.context import Context
import db.db_adapter as database
from datetime import datetime, timedelta
from typing import *
from db.birthday import Birthday


class BirthdayCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        # Today starts as yesterday to make the loop run the first time
        self.today = (datetime.today() - timedelta(days=1)).date()
        self.client.loop.create_task(self.birthday_loop())

    today = None

    # @commands.command(name="birthday-add",pass_context=True)
    # @commands.has_role("Member's")
    # async def birthday_add(self, ctx: Context,member: Optional[Union[nextcord.Member,nextcord.User]],day, month, year=-1):
    #     """<Day Mont [Year]> Adds your birthday."""
    #     if member == None:
    #         member: nextcord.Member = ctx.message.author
    #     # Just in case don't add bots to the database
    #     # if member.client:
    #     #     return
    #     database.create_birthday(user_id=member.id, day=day, month=month, year=year)
    #     await ctx.reply('Birthday added')

    @commands.command(name="birthday-add",pass_context=True)
    async def birthday_add(self, ctx: Context,day, month, year=-1):
        """<Day Mont [Year]> Adds your birthday."""
       
        member: nextcord.Member = ctx.message.author
        # Just in case don't add bots to the database
        # if member.client:
        #     return
        database.create_birthday(user_id=member.id, day=day, month=month, year=year)
        await ctx.reply('Birthday added')

    

    @commands.command(name="birthday-update",pass_context=True)
    async def birthday_update(self, ctx: Context, day, month, year=-1):
        """<Day Mont [Year]> Update your birthday."""
        member: nextcord.Member = ctx.message.author
        database.update_birthday(user_id=member.id, day=day, month=month, year=year)
        await ctx.reply('Birthday updated')

    @commands.command(name="birthday-delete",pass_context=True)
    @commands.has_permissions(administrator=True)
    async def birthday_delete(self, ctx: Context):
        """Delete your birthday."""
        member: nextcord.Member = ctx.message.author
        birthday = Birthday(user_id=member.id)
        database.delete_birthday(user_id=member.id)
        await ctx.reply('Birthday deleted')

    @commands.command(name="birthday",pass_context=True)
    async def birthday(self, ctx: Context, member: nextcord.Member = None):
        """<[Member]> Show a member's birthday. Displays your birthday by default."""
        if member is None:
            member = ctx.message.author
        birthday: Birthday = database.get_birthday_one(user_id=member.id)
        if birthday is None:
            message = f'\n{member.display_name}: no registered.'
        else:
            message = f'\n{member.display_name}\'s birthday is on {birthday.printable_date()}.'
        await ctx.reply(message)

    @commands.command(name="birthday-all",pass_context=True)
    async def birthday_all(self, ctx: Context, show=None):
        """[show not registered?] Show everyone's birthday"""
        server = ctx.message.guild
        message = 'Birthdays:'
        for member in server.members:
            # if member.client.user:
            #     # Ignore bots
            #     continue
            birthday = database.get_birthday_one(user_id=member.id)
            if birthday is None:
                if show is not None:
                    message += f'\n{member.display_name}: no registered.'
            else:
                message += f'\n{member.mention}\'s birthday is on {birthday.printable_date()}.'
        await ctx.reply(message)

    @commands.command(name="birthday-today",pass_context=True)
    @commands.has_permissions(administrator=True)
    async def birthday_today(self, ctx: Context):
        """Show today's birthday"""
        server = ctx.message.guild
        birthdays = birthdays_today_server(server)

        if len(birthdays) == 0:
            message = "No birthdays today."
        else:
            jump = ''
            message = '@here\n'
        
            for bd in birthdays:
                member = nextcord.utils.get(server.members, id=bd.user_id)
                message += f'{jump} It\'s <@{bd.user_id}> birthday! 🎂'
                jump = '\n'
        await ctx.reply(message)

    async def birthday_loop(self):
        while not self.client.is_closed:
            await asyncio.sleep(3600)
            if datetime.today().date() != self.today:
                # When day changes
                
                self.today = datetime.today().date()
                for server in self.client.servers:
                    birthdays = birthdays_today_server(server)
                    if len(birthdays) != 0:
                        for channel in server.channels:
                            if channel.permissions_for(server.me).send_messages \
                                    and channel.type is nextcord.ChannelType.text:
                                jump = ''
                                message = '@everyone\n'
                                for bd in birthdays:
                                    member = nextcord.utils.get(server.members, id=bd.user_id)
                                    message = f'{jump} It\'s {member.mention}\' birthday!'
                                    jump = '\n'
                                await self.client.send_message(channel, message)
                                break


def birthdays_today_server(server):
    birthdays = []
    today = datetime.today().date()
    for member in server.members:
        # if member.client.user:
        #     # Ignore bots
        #     continue
        birthday = database.get_birthday_one(user_id=member.id)
        if birthday is not None:
            if today.day == birthday.day and today.month == birthday.month:
                birthdays.append(birthday)
    return birthdays


def setup(client):
    client.add_cog(BirthdayCommands(client))
