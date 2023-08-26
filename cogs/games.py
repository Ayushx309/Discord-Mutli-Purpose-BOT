import logging
from random import choice
import json
import requests
import openai
import datetime
import nextcord
from nextcord.ext import commands
from global_functions import BOT_USER_ID,APIKEY,ban_msg
import random
import asyncio
import time
import os
import psutil
from datetime import datetime
from nextcord.ext import commands, tasks
from typing import Union
import aiohttp
from io import BytesIO
from nextcord import ButtonStyle, SlashOption, ChannelType 
from nextcord.ui import button, View, Button
from gtts import gTTS
import nextcord.ext.commands
import PIL.Image as image123
import giphy_client
from sympy import content
from giphy_client.rest import ApiException
from typing import *
import games.tictactoe
import games.wumpus
import games.minesweeper
import games.hangman
import games.twenty



logging.basicConfig(level=logging.DEBUG,filemode="w",filename="logs/logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='tictactoe', aliases=['ttt'], description="""Play Tic-Tac-Toe""")
    async def ttt(self, ctx):
        # """Play Tic-Tac-Toe"""
        await games.tictactoe.play_game(self.client, ctx, chance_for_error=0.2)

    @commands.command(name='wumpus',description="""Play Wumpus game""")
    async def _wumpus(self, ctx):
        # """Play Wumpus game"""
        await games.wumpus.play(self.client, ctx)

    @commands.command(name='minesweeper', aliases=['ms'],description="Play Minesweeper")
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        # """Play Minesweeper"""
        await games.minesweeper.play(ctx, columns, rows, bombs)

    @commands.command(name='hangman', aliases=['hang'],description="Play Hangman")
    async def hangman(self, ctx):
        """Play Hangman"""
        await games.hangman.play(self.client, ctx)

    @commands.command(name='2048',description="Play 2048 game")
    async def twenty(self, ctx):
        """Play 2048 game"""
        await games.twenty.play(bot=self.client,ctx=ctx)

    @commands.command(name='toss', aliases=['flip'],description="Flips a Coin")
    async def toss(self, ctx):
        """Flips a Coin"""
        coin = ['+ heads', '- tails']
        await ctx.send(f"```diff\n{random.choice(coin)}\n```")


    
    @commands.command(name='poll', description="""Create a quick poll[~poll "question" choices]""")
    async def quickpoll(self, ctx, question, *options: str):
        # """Create a quick poll[~poll "question" choices]"""
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = nextcord.Embed(title=question, description=''.join(description), color=nextcord.Colour(0xFF355E))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)


    @commands.command(name='rps', aliases=['rockpaperscissors'], description="Play Rock, Paper, Scissors game")
    async def rps_(self, ctx):
        """Play Rock, Paper, Scissors game"""
        def check_win(p, b):
            if p=='🌑':
                return False if b=='📄' else True
            if p=='📄':
                return False if b=='✂' else True
            # p=='✂'
            return False if b=='🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.client.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t:\t{reaction.emoji}\n\n:robot:\t:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")



    @commands.command(name='tally', description="Tally the created poll")
    @commands.has_permissions(administrator=True)
    async def tally(self, ctx, pid):
        """Tally the created poll"""
        poll_message = await ctx.message.channel.fetch_message(pid)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != self.client.user:
            return
        if not embed.footer.text.startswith('Poll ID:'):
            return
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.client.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)

        output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)


    @commands.command(name='teams', aliases=['team'], description="Makes random teams with specified number(def. 2)")
    async def teams(self, ctx, num=2):
        """Makes random teams with specified number(def. 2)"""
        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel :mute:")
        members = ctx.author.voice.channel.members
        memnames = []
        for member in members:
            memnames.append(member.name)

        remaining = memnames
        if len(memnames)>=num:
            for i in range(num):
                team = random.sample(remaining,len(memnames)//num)
                remaining = [x for x in remaining if x not in team]
                await ctx.send(f"Team {chr(65+i)}\n" + "```CSS\n" + '\n'.join(team) + "\n```")
        if len(remaining)> 0:
            await ctx.send("Remaining\n```diff\n- " + '\n- '.join(remaining) + "\n```")


 

def setup(client):
    client.add_cog(Games(client))