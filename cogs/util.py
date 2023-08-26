import logging
import time
import nextcord
import os
import psutil
import random
from datetime import datetime
from nextcord.ext import commands, tasks
from global_functions import ban_msg, kick_msg, BOT_USER_ID, EMOJIS_TO_USE_FOR_CALCULATOR as etufc
from global_functions import giphy_apikey,PREFIX
import aiohttp
from io import BytesIO
import requests
from nextcord import ButtonStyle, SlashOption, ChannelType 
from nextcord.ui import button, View, Button
from gtts import gTTS
import nextcord.ext.commands
import PIL.Image as image123
from io import BytesIO
import json
import giphy_client
import asyncio
from sympy import content
from giphy_client.rest import ApiException
import pywhatkit
from typing import Optional
from PIL import Image
import discord
import os
import io
import wave
import speech_recognition as sr





logging.basicConfig(level=logging.DEBUG,filemode="w",filename="logs/logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")


green_button_style = ButtonStyle.success
grey_button_style = ButtonStyle.secondary
blue_button_style = ButtonStyle.primary
red_button_style = ButtonStyle.danger


class CalculatorButtons(View):
    def __init__(self, owner, embed, message):
        self.embed = embed
        self.owner = owner
        self.message = message
        self.expression = ""
        super().__init__(timeout=300.0)

    @button(emoji=etufc['1'], style=grey_button_style, row=1)
    async def one_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "1"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['2'], style=grey_button_style, row=1)
    async def two_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "2"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['3'], style=grey_button_style, row=1)
    async def three_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "3"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['4'], style=grey_button_style, row=2)
    async def four_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "4"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['5'], style=grey_button_style, row=2)
    async def five_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "5"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['6'], style=grey_button_style, row=2)
    async def six_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "6"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['7'], style=grey_button_style, row=3)
    async def seven_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "7"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['8'], style=grey_button_style, row=3)
    async def eight_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "8"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['9'], style=grey_button_style, row=3)
    async def nine_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "9"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['0'], style=grey_button_style, row=4)
    async def zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "0"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="00 ", style=grey_button_style, row=4)
    async def double_zero_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "00"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['.'], style=grey_button_style, row=4)
    async def dot_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "."
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['x'], style=blue_button_style, row=1, custom_id="*")
    async def multiplication_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "x"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['÷'], style=blue_button_style, row=2, custom_id="/")
    async def division_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "÷"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['+'], style=blue_button_style, row=3)
    async def addition_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "+"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(emoji=etufc['-'], style=blue_button_style, row=4)
    async def subtraction_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression += "-"
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="←", style=red_button_style, row=1)
    async def back_space_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = self.expression[:-1]
        self.embed.description = self.expression
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Clear", style=red_button_style, row=2)
    async def clear_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        self.expression = ""
        self.embed.description = "Cleared Calculator"
        await interaction.response.edit_message(embed=self.embed)

    @button(label="Exit", style=red_button_style, row=3)
    async def exit_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Abandoned Calculator", color=nextcord.Color.red())
        await interaction.response.edit_message(embed=embed, view=self)

    @button(label="=", style=green_button_style, row=4)
    async def equal_to_callback(self, button, interaction: nextcord.Interaction):
        if interaction.user.id != self.owner.id:
            return
        expression = self.expression
        expression = expression.replace("÷", "/").replace("x", "*")
        try:
            result = str(eval(expression))
            self.expression = result
        except:
            result = "An Error Occured ;-;"
        self.embed.description = result
        await interaction.response.edit_message(embed=self.embed)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        embed = nextcord.Embed(title="Time Up", color=nextcord.Color.red())
        await self.message.edit(embed=embed, view=self)


us = 0
um = 0
uh = 0
ud = 0


class util(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.clientuptime.start()

    @commands.command(description="A handy Calculator!", aliases=["calc"])
    async def calculator(self, ctx):
        message = await ctx.send("Loading Calculator....")
        embed = nextcord.Embed(
            title=f"{ctx.author}'s Calculator",
            color=nextcord.Color.green(),
            description="This is the start of the calculator!",
        )
        view = CalculatorButtons(ctx.author, embed, message)
        await message.edit(content=None, embed=embed, view=view)

    @commands.command(description="Shows the user's info.")
    async def userinfo(self, ctx, *, user: nextcord.Member = None):  # b'\xfc'
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = nextcord.Embed(color=0xDFA3FF, description=user.mention)
        embed.set_author(name=str(user.name), icon_url=user.display_avatar)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(
                name="Roles [{}]".format(len(user.roles) - 1),
                value=role_string,
                inline=False,
            )
        perm_paginator = commands.Paginator(prefix="```diff", max_size=1000)
        for p in user.guild_permissions:
            perm_paginator.add_line(
                f"{'+' if p[1] else '-'} {str(p[0]).replace('_', ' ').title()}"
            )
        embed.add_field(
            name="Guild permissions", value=f"{perm_paginator.pages[0]}", inline=False
        )
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        return await ctx.send(embed=embed)

    @commands.command(description="Shows the server's description.")
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embed2 = nextcord.Embed(
            timestamp=ctx.message.created_at, color=ctx.author.color
        )
        embed2.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(
            name="Verification Level",
            value=str(ctx.guild.verification_level),
            inline=True,
        )
        embed2.add_field(name="Highest role", value=ctx.guild.roles[-1], inline=True)
        embed2.add_field(name="Number of roles", value=str(role_count), inline=True)
        embed2.add_field(
            name="Number Of Members", value=ctx.guild.member_count, inline=True
        )
        embed2.add_field(
            name="Created At",
            value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
            inline=True,
        )
        embed2.add_field(name="Bots:", value=(", ".join(list_of_bots)), inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon.url)
        embed2.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed2.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed2)

    @commands.command(
        aliases=["cs", "ci", "channelinfo"], description="Shows the channel's stats."
    )
    async def channelstats(self, ctx, channel: nextcord.TextChannel = None):
        if channel == None:
            channel = ctx.channel

        embed = nextcord.Embed(
            title=f"{channel.name}",
            description=f"{'Category - `{}`'.format(channel.category.name) if channel.category else '`This channel is not in a category`'}",
        )
        embed.add_field(name="Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="Channel Id", value=channel.id, inline=True)
        embed.add_field(
            name="Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic'}",
            inline=False,
        )
        embed.add_field(name="Channel Position", value=channel.position, inline=True)
        embed.add_field(name="Slowmode", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW", value=channel.is_nsfw(), inline=True)
        embed.add_field(name="Annoucement", value=channel.is_news(), inline=True)
        embed.add_field(
            name="Channel Permissions", value=channel.permissions_synced, inline=True
        )
        embed.add_field(name="Channel Hash", value=hash(channel), inline=False)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)
        embed.set_footer(
            text=self.client.user.name, icon_url=self.client.user.display_avatar
        )
        await ctx.send(embed=embed)

    @commands.command(alisas=["adde"], description="Adds an emoji to the server.")
    async def emojiadd(self, ctx, url: str, *, name):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            async with aiohttp.ClientSession() as ses:
                async with ses.get(url) as r:

                    try:
                        img_or_gif = BytesIO(await r.read())
                        b_value = img_or_gif.getvalue()
                        if r.status in range(200, 299):
                            emoji = await guild.create_custom_emoji(
                                image=b_value, name=name
                            )
                            em = nextcord.Embed(
                                title="Emoji Success",
                                description=f"Successfully created emoji: <:{name}:{emoji.id}>",
                            )
                            await ctx.send(embed=em)
                            await ses.close()
                        else:
                            em = nextcord.Embed(
                                title="Emoji Error",
                                description=f"Error when making request | {r.status} response.",
                            )
                            await ctx.send(embed=em)
                            await ses.close()

                    except nextcord.HTTPException:
                        em = nextcord.Embed(
                            title="Emoji Error", description="File size is too big!"
                        )
                        await ctx.send(embed=em)

    @commands.command(
        alisas=["removee"], description="Removes the specified emoji from the server."
    )
    async def emojiremove(self, ctx, emoji: nextcord.Emoji):
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            em = nextcord.Embed(
                title="Emoji Success",
                description=f"Successfully deleted (or not :P) {emoji}",
            )
            await ctx.send(embed=em)
            await emoji.delete()

    @commands.command(name="toggle", description="Enable or disable a command!")
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx, *, command):
        command = self.client.get_command(command)

        if command is None:
            embed = nextcord.Embed(
                title="ERROR", description="I can't find a command with that name"
            )
            await ctx.send(embed=embed)

        elif ctx.command == command:
            embed = nextcord.Embed(
                title="ERROR", description="You cannot disable this command "
            )
            await ctx.send(embed=embed)

        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            embed = nextcord.Embed(title="Toggle", description=f"{PREFIX}{command} is {ternary}")
            await ctx.send(embed=embed)
    
    @commands.command(name="steal", description="Steals an emoji form a server")
    async def steal(self, ctx, emoji: nextcord.PartialEmoji, *, text=None):

        if ctx.author.guild_permissions.manage_emojis:

            if text == None:
                text = emoji.name
            else:
                text = text.replace(" ", "_")

            r = requests.get(emoji.url, allow_redirects=True)

            if emoji.animated == True:
                open("emoji.gif", "wb").write(r.content)
                with open("emoji.gif", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=text, image=f.read())
                os.remove("emoji.gif")

            else:
                open("emoji.png", "wb").write(r.content)
                with open("emoji.png", "rb") as f:
                    z = await ctx.guild.create_custom_emoji(name=text, image=f.read())
                os.remove("emoji.png")

            embed = nextcord.Embed(
                title="Success",
                description=f"Succesfully Cloned {z}",
                color=nextcord.Color.green(),
            )
            await ctx.send(embed=embed)

    @commands.command(description="Shows the ping of the bot")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ping(self, ctx):
        em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
        em.add_field(
            name="My API Latency is:", value=f"{round(self.client.latency*1000)} ms!"
        )
        em.set_footer(
            text=f"Ping requested by {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)



    @tasks.loop(seconds=2.0)
    async def clientuptime(self):
        global uh, us, um, ud
        us += 2
        if us == 60:
            us = 0
            um += 1
            if um == 60:
                um = 0
                uh += 1
                if uh == 24:
                    uh = 0
                    ud += 1

    @clientuptime.before_loop
    async def before_clientuptime(self):
        print("\033[1;37;48mWaiting...")
        await self.client.wait_until_ready()

    @commands.command(
        aliases=["statistics", "stat", "statistic"],
        description="Shows the bot's statistics",
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, ctx):
        global ud, um, uh, us
        em = nextcord.Embed(title="How long have I been up?")
        em.add_field(name="Days:", value=ud, inline=False)
        em.add_field(name="Hours:", value=uh, inline=False)
        em.add_field(name="Minutes:", value=um, inline=False)
        em.add_field(name="Seconds:", value=us, inline=False)
        em.add_field(name="CPU usage:", value=f"{psutil.cpu_percent()}%", inline=False)
        em.add_field(
            name="RAM usage:", value=f"{psutil.virtual_memory()[2]}%", inline=False
        )
        em.set_footer(
            text=f"Stats requested by: {ctx.author}", icon_url=ctx.author.display_avatar
        )
        await ctx.send(embed=em)
    
    
    @commands.command(name="say",description="test to speech")
    async def tts(self, ctx, *args):
        
        text =" ".join(args)
        user = ctx.message.author
        if user.voice != None:
            try: 
                vc = await user.voice.channel.connect()
            except:
                vc = ctx.voice_client

            sound = gTTS(text=text,lang="en",slow=False)
            sound.save("audio/tts-audio.mp3")

            if vc.is_playing():
                vc.stop()

            source = await nextcord.FFmpegOpusAudio.from_probe("audio/tts-audio.mp3", method="fallback")
            vc.play(source)
        else:
            await ctx.reply("You need to be in VC to run this command!")


    @commands.command(name="wanted",description="Set Bounty")
    async def wanted(self, ctx, user: nextcord.User = None ):
        if user == None:
            user = ctx.author

        wanted = image123.open("assets/wanted2.jpg")
        data = BytesIO(await user.display_avatar.read())
        pfp = image123.open(data)
        pfp = pfp.resize((177, 177))
        wanted.paste(pfp, (120, 212))
        wanted.save("assets/profile.jpg")
        await ctx.reply(file=nextcord.File("assets/profile.jpg"))


    
    # @commands.command(name="bomb",description="bomber")
    # async def bomber(self, ctx,):
    #         """
    #         choice
    #         delay time
            
    #         country code
    #         target number
    #         """
    #         ...








def setup(client):
    client.add_cog(util(client))
