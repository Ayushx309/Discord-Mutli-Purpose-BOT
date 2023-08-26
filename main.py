import logging
from logging import exception
import nextcord
import traceback
import datetime
from nextcord.colour import Color
from nextcord.embeds import Embed
from nextcord.ext import commands, tasks
from global_functions import (
    PREFIX,
    responses,
    TOKEN,
    ERROR_CHANNELS,
    UPDATE_CHANNEL,
    MEMBERCOUNT_CHANNEL,
    read_database,
    write_database
)
import random, json, os, sys
from difflib import get_close_matches
import asyncio
import aiohttp
from urllib.request import urlopen
import json
from nextcord.voice_client import VoiceClient
import asyncio
import random
from random import choice
import json
import os
import aiosqlite
from typing import *
from cogs.utils import settings
from cogs.utils import permissions
from typing import Optional
from PIL import Image
import PIL.Image as image123
from io import BytesIO


logging.basicConfig(level=logging.DEBUG,filemode="w",filename="logs/logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")



intents = nextcord.Intents().all()
client = commands.Bot(
    command_prefix=str(PREFIX), intents=intents, case_insensitive=True
)
client.remove_command("help")

for fn in os.listdir("./cogs"):
    if fn.endswith(".py") and fn != "global_functions.py":
        client.load_extension(f"cogs.{fn[:-3]}")


@tasks.loop(minutes=10)
async def member_count():
    try:
        member_count_channel = await client.fetch_channel(MEMBERCOUNT_CHANNEL)
    except:
        return print(f"Error!\nThe member count channel id is invalid!")
    if not isinstance(member_count_channel, nextcord.VoiceChannel):
        return print(
            f"Error!\nThe member count channel id that you gave is not a voice channel!"
        )
    ayush_git_repo = client.get_guild(1067403110449938503)

    for x in (member_count_channel_name := member_count_channel.name.split(" ")):
        if x.isdigit():
            member_count_channel_name[member_count_channel_name.index(x)] = str(
                ayush_git_repo.member_count
            )
    try:
        await member_count_channel.edit(
            name=" ".join(member_count_channel_name),
            reason="Automated Member Count Rename",
        )
    except:
        return print("Error in renaming the member channel ;-;")


async def startup():
    client.session = aiohttp.ClientSession()


client.loop.create_task(startup())


def apiReq(id, responseMSG):
    responseMSG = responseMSG.replace(" ", "-")

    url = f"http://api.brainshop.ai/get?bid=160228&key=nop&uid={id}&msg={responseMSG}"

    response = urlopen(url)
    data = json.loads(response.read())

    return data


@client.command()
async def chat(ctx, *, responseMSG):
    data = apiReq(ctx.author.id, responseMSG)
    await ctx.send(data)


@client.command()
async def load(ctx, extension):
    if ctx.author.id == 410321996463996930:
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog loaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 410321996463996930:
        client.unload_extension(f"cogs.{extension}")
        await asyncio.sleep(1)
        client.load_extension(f"cogs.{extension}")
        await ctx.send("Cog reloaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 410321996463996930:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send("Cog unloaded")
    else:
        await ctx.send("Only bot devs can run this command")


@client.command()
async def check(ctx, cog_name):
    if ctx.author.id == 410321996463996930:
        try:
            client.load_extension(f"cogs.{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("Cog is loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Cog not found")
        else:
            await ctx.send("Cog is unloaded")
            client.unload_extension(f"cogs.{cog_name}")
    else:
        await ctx.send("Only bot devs can run this command")


status = [' !help ;)']


async def get_last_message(channel):
    messages = await channel.history(limit=1).flatten()
    if messages:
        last_message = messages[0]
        return int(last_message.content)
    else:
        return 0

async def send_msg(channel, number):
    await channel.send(f"{number}")





@client.event
async def on_ready():


    member_count.start()
    change_status.start()

    
    await settings.check_servers(client)
    print(f"\033[1;33;48m{client.user} is Ready")

    


    try:
        update_channel = await client.fetch_channel(int(UPDATE_CHANNEL))
        embed = nextcord.Embed(
            title="I am online!",
            description=f"🤖   I got online at {nextcord.utils.format_dt(nextcord.utils.utcnow(), 'F')}",
            colour=0x42f5c5
        )
        await update_channel.send(embed=embed)
    except:
        print(
            f"\033[1;31;48m Can't Fetch The Update Channel!\nMake Sure That You Kept The Right ID, If You Did Try And Contact |OogaBooga0112|"
        )
    error_channels = []
    error_in_loading_channel = []
    for ERROR_CHANNEL in ERROR_CHANNELS:
        try:
            channel = await client.fetch_channel(int(ERROR_CHANNEL))
            error_channels.append(
                f"https://discord.com/channels/{channel.guild.id}/{channel.id}"
            )
        except:
            error_in_loading_channel.append(str(ERROR_CHANNEL))
    error_channels = ", ".join(error_channels)
    print(f"\033[1;37;48mMy errors will be logged to {error_channels}")
    smthing = "\n".join(error_in_loading_channel)
    print(
        f"\033[1;31;48m Can't fetch my error channel with id `{smthing}`, I can't log the errors ;-;"
    ) if len(error_in_loading_channel) > 0 else ...

    CHANNEL_ID = 1130870720436650044
    Cchannel = client.get_channel(CHANNEL_ID)
    
    # while True:
    #     last_number = await get_last_message(Cchannel)
    #     next_number = last_number + 1

    #     await send_msg(Cchannel, next_number)
    #     await asyncio.sleep(40)


@client.event
async def on_member_join(member):
    if member.guild.id != 410321996463996930:
        return
    channel = client.get_channel(1065924929071091763)
    await channel.send(f"{member.name} has joined")


@client.command(alaises=["halt"])
@permissions.are_you_my_mummy()
async def shutdown():
    """ Shutdown the bot """
    client.logout
    
@client.event
async def on_server_join(server):
    print("\033[1;32;48m Bot was added to {} : {}".format(server.id, server.name))
    await settings.check_servers(client)

    


@client.event
async def on_message_delete(message):
    embed=nextcord.Embed(title=f"{message.author.name} has deleted a message 🗑️", description=f"{message.author.mention} Deleted message:\n {message.content}",timestamp= datetime.datetime.now(),colour=0x42f5c5)
    embed.set_thumbnail(url=f"{message.author.display_avatar}")
    embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",icon_url=f"{message.author.display_avatar}")
    embed.set_footer(text=f"User ID: {message.author.id}")
    channel = client.get_channel(1068909904473104436)
    await channel.send(embed=embed)     

@client.event
async def on_message_edit(message_before,message_after):
    embed=nextcord.Embed(title=f"{message_before.author.name} has edited the message",description=f"{message_before.author.mention}",timestamp= datetime.datetime.now(),colour=0x42f5c5)
    embed.set_thumbnail(url=f"{message_after.author.display_avatar}")
    embed.add_field(name="📄  Original Message", value=f"`{message_before.content}`", inline=False)
    embed.add_field(name="📝  Edited Message", value=f"`{message_after.content}`", inline=False)
    embed.set_footer(text=f"User ID: {message_before.author.id}")
    channel = client.get_channel(1068909904473104436)
    await channel.send(embed=embed)





@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) != "⭐":
        return
    database = read_database()
    try:
        guild_starboard_settings = database[str(payload.guild_id)]['starboard']
        guild_starboard_settings['on or off']
        guild_starboard_settings['channel']
        guild_starboard_settings['minimum stars']
    except:
        return
    try:
        if not guild_starboard_settings["on or off"]:
            return
    except:
        return
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    for react in message.reactions:
        if str(react.emoji) == "⭐":
            react_count = react.count
            break
    if react_count >= 1:
        try:
            starboard_channel = client.get_channel(
                    guild_starboard_settings["channel"])
            try:
                sent_msg = await starboard_channel.fetch_message(
                        guild_starboard_settings[str(message.id)]
                    )
                await sent_msg.edit(
                        content=f":star2: {react_count} {channel.mention}"
                    )
            except:
                embed = nextcord.Embed(
                        description=f"{message.content}\n**Source**\n[Jump!]({message.jump_url})"
                    )
                embed.set_author(
                        name=message.author.display_name,
                        icon_url=message.author.display_avatar,
                    )
                embed.set_footer(text=str(message.id))
                sent_msg = await starboard_channel.send(
                        f":star2: {react_count} {channel.mention}", embed=embed
                    )
                guild_starboard_settings[str(message.id)] = sent_msg.id
                write_database(data=database)

        except:
            ...


#############################################          slash_commands         #########################################################


@client.slash_command(name='credits',description="Shows Bot developers")
async def credits(ctx: nextcord.Interaction):
    await ctx.response.send_message('Made by `oogaBooga0112`')


@client.slash_command(name="ascii")
async def ascii_img(ctx: nextcord.Interaction,image: nextcord.Attachment = nextcord.SlashOption(name="image",description="Please select image.",required=True)):
   
   data = BytesIO(await image.read())
   ascii = image123.open(data)
   ascii.save("assets/ascii_art.jpg")
   ascii_art = image_to_ascii_art("assets/ascii_art.jpg")
   print(f"""{ascii_art}""")
   await ctx.response.send_message(file=nextcord.File(r'D:\Python\Projects\OogaBooga Bot\asciiart.txt'))


def image_to_ascii_art(img_path: str, output_file: Optional[str] = "asciiart") -> str:
    """Convert an Image to ASCII Art"""
    img = Image.open(img_path).convert("L")
    width, height = img.size
    aspect_ratio = height / width
    new_width = 80
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    pixels = img.getdata()
    chars = ["*", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = "".join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [
        new_pixels[index : index + new_width]
        for index in range(0, new_pixels_count, new_width)
    ]
    ascii_image = "\n".join(ascii_image)
    with open(f"{output_file}.txt", "w") as f:
        f.write(ascii_image)
    return ascii_image



#############################################          slash_commands         #########################################################


@client.event
async def on_message(message):
    mention = f"<@{client.user.id}>"
    if message.content == mention:
        await message.channel.send(
            f"Eyoo Nerds my prefix is `{PREFIX}` for help use the command `{PREFIX}help`"
        )
    await client.process_commands(message)

# @tasks.loop(seconds=30)
# async def counter():
#     CHANNEL_ID = 1130870720436650044
#     channel = client.get_channel(CHANNEL_ID)
#     if channel:
#         messages = await channel.history(limit=1).flatten()
#         if messages:
#             message = messages[0]

#             count = int(message.content)
#             print(f'Last message in #{message.channel} User : {message.author.name} Message: {message.content}')
#             count += 1
#             channel = client.get_channel(CHANNEL_ID)
        
#             await client.channel.send(count)





class UrlButton(nextcord.ui.Button):
    def __init__(self, *, label, url, emoji=None):
        super().__init__(label=label, url=url, emoji=emoji)


class HelpDropdown(nextcord.ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()
        self.add_item(
            UrlButton(label="Support Server", url="https://discord.gg/QXFgRdSA27")
        )


        ######### Set the options that will be presented inside the dropdown ############

    @nextcord.ui.select(
        placeholder="Choose your help page",
        min_values=1,
        max_values=1,
        options=[
            nextcord.SelectOption(
                label="Moderation", description=f"`{PREFIX}help moderation`", emoji="⚒️"
            ),
            nextcord.SelectOption(
                label="Utility", description=f"`{PREFIX}help utility`", emoji="⚙️"
            ),
            nextcord.SelectOption(
                label="Music", description=f"`{PREFIX}help music`", emoji="🎵"
            ),
                nextcord.SelectOption(
                label="Ai Commands", description=f"`{PREFIX}help ai`", emoji="🤖"
            ),
                nextcord.SelectOption(
                label="Games", description=f"`{PREFIX}help Games`", emoji="🕹️"
            ),
                nextcord.SelectOption(
                label="More Commands", description=f"`{PREFIX}help morecommand`", emoji="📃"
            )
            
        ]
    )

    async def help_callback(self, select, interaction: nextcord.Interaction):
        if interaction.user.id != self.user.id:
            em = nextcord.Embed(
                title="No U",
                description="This is not for you!",
                color=nextcord.Color.red(),
            )
            return await interaction.response.send_message(embed=em, ephemeral=True)
        select.placeholder = f"{select.values[0]} Help Page"
        if select.values[0] == "Moderation":
            embed = nextcord.Embed(
                title=f"{client.user.name} Moderation Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            for index, command in enumerate(client.get_cog("Moderation").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)


        elif select.values[0] == "Games":
            embed = nextcord.Embed(
                title=f"{client.user.name} Games:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            for index, command in enumerate(client.get_cog("Games").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )

            # embed.add_field(
            #         name=f"`{PREFIX}start`",
            #         value=f"Tetris in Discord",
            # )
            await interaction.response.edit_message(embed=embed, view=self)


        elif select.values[0] == "Ai Commands":
            embed = nextcord.Embed(
                title=f"{client.user.name} Ai Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            for index, command in enumerate(client.get_cog("ai").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "More Commands":
            embed = nextcord.Embed(
                title=f"{client.user.name} More Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            for index, command in enumerate(client.get_cog("morecommands").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "Utility":
            embed = nextcord.Embed(
                title=f"{client.user.name} Utility Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            for index, command in enumerate(client.get_cog("util").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            for index, command in enumerate(client.get_cog("BirthdayCommands").get_commands()):# add this in others too! #######
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            for index, command in enumerate(client.get_cog("Levelsys").get_commands()):# add this in others too! #######
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
            await interaction.response.edit_message(embed=embed, view=self)

        elif select.values[0] == "Music":
            embed = nextcord.Embed(
                title=f"{client.user.name} Music Commands:",
                description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
                 color=0x2b2d31


            )
            # embed.add_field(name=f'`{PREFIX}play`',value='Plays music ',inline=True)
            # embed.add_field(name=f'`{PREFIX}queue`',value='To add music to queue ',inline=True)
            # embed.add_field(name=f'`{PREFIX}volume`',value='Changes the bots volume ',inline=True)
            # embed.add_field(name=f'`{PREFIX}join`',value='Makes the bot join the voice channel ',inline=True)
            # embed.add_field(name=f'`{PREFIX}leave`',value='Stops the music and makes the bot leave the voice channel ',inline=False)
            # embed.add_field(name=f'`{PREFIX}loop`',value='Toggles loop mode ',inline=True)
            # embed.add_field(name=f'`{PREFIX}volume`',value='Changes the bots volume ',inline=True)
            # embed.add_field(name=f'`{PREFIX}pause`',value='Pauses the song ',inline=True)
            # embed.add_field(name=f'`{PREFIX}resume`',value='Resumes the song ',inline=True)
            # embed.add_field(name=f'`{PREFIX}view`',value='Shows the queue ',inline=True)
            # embed.add_field(name=f'`{PREFIX}skip`',value='Skip music ',inline=True)
            for index, command in enumerate(client.get_cog("Music").get_commands()):
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )


            await interaction.response.edit_message(embed=embed, view=self)






@client.group(invoke_without_command=True)
async def help(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Help",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for more information.",
         color=0x2b2d31


    )
    embed.set_thumbnail(url=f"{client.user.display_avatar}")
    embed.add_field(
        name="Moderation:", value=f"`{PREFIX}help moderation`", inline=False
    )
    embed.add_field(name="Utility:", value=f"`{PREFIX}help utility`", inline=False)
    embed.add_field(name="Music:", value=f"`{PREFIX}help music`", inline=False)
    embed.add_field(name="Ai Commands:", value=f"`{PREFIX}help ai`", inline=False)
    embed.add_field(name="Games:", value=f"`{PREFIX}help games`", inline=False)
    embed.add_field(name="More Commands:", value=f"`{PREFIX}help morecommands`", inline=False)
    dank_lord = await client.fetch_user(915223835656220672)
    embed.set_footer(
        text=f"Requested by {ctx.author} | Created by: Ninja#0112 ",
        icon_url=f"{ctx.author.display_avatar}",
    )
    # | Improved by: {dank_lord}
    await ctx.send(embed=embed, view=view)


@help.command(aliases=['sb','starb'])
async def starboard(ctx):
    embed=Embed(title="Help with Starboard", description=f"""
`{PREFIX}starboard setup`
Setup the starboard!

`{PREFIX}starboard toggle [on/off]`
Toggle the starboard

`{PREFIX}starboard channel [channel]`
Get/Change the starboard channel settings

`{PREFIX}starboard minstars [number]`
Get/Change the starboard minimum star settings""")
    await ctx.send(embed=embed)


###########################     moderation

@help.command()
async def moderation(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Moderation Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
    )
    embed = nextcord.Embed(
        title=f"{client.user.name} Moderation Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
         color=0x2b2d31


    )
    for command in client.get_cog("Moderation").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


####################################  games


@help.command()
async def games(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Games:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
    )
    embed = nextcord.Embed(
        title=f"{client.user.name} Games:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
         color=0x2b2d31


    )
    for command in client.get_cog("Games").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )

    # embed.add_field(
    #     name=f"`{PREFIX}start`",
    #     value=f"Tetris in Discord",
    # )
    await ctx.send(embed=embed, view=view)


############################################ morecommands


@help.command()
async def morecommands(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} More Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
    )
    embed = nextcord.Embed(
        title=f"{client.user.name} More Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
        color=0x2b2d31


    )
    for command in client.get_cog("morecommands").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


###############################   utility

@help.command()
async def utility(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Utility Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
        color=0x2b2d31


    )
    for command in client.get_cog("util").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
        for command in client.get_cog("BirthdayCommands").walk_commands():
            description = command.description
            if not description or description is None or description == "":
                description = "No description"
            embed.add_field(
                name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                value=description,
            )
        for command in client.get_cog("Levelsys").walk_commands():
                description = command.description
                if not description or description is None or description == "":
                    description = "No description"
                embed.add_field(
                    name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
                    value=description,
                )
    await ctx.send(embed=embed, view=view)


########################################  ai


@help.command()
async def ai(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Ai Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
        color=0x2b2d31


    )
    for command in client.get_cog("ai").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )
    await ctx.send(embed=embed, view=view)


############################   music


@help.command()
async def music(ctx):
    view = HelpDropdown(ctx.author)
    embed = nextcord.Embed(
        title=f"{client.user.name} Music Commands:",
        description=f"Support Server: [Click Here!](https://discord.gg/QXFgRdSA27) || `{PREFIX}help [category]` for other information.",
        color=0x2b2d31


    )
    # embed.add_field(name=f'`{PREFIX}play`',value='Plays music ',inline=True)
    # embed.add_field(name=f'`{PREFIX}queue`',value='To add music to queue ',inline=True)
    # embed.add_field(name=f'`{PREFIX}join`',value='Makes the bot join the voice channel ',inline=True)
    # embed.add_field(name=f'`{PREFIX}leave`',value='Stops the music and makes the bot leave the voice channel ',inline=False)
    # embed.add_field(name=f'`{PREFIX}loop`',value='Toggles loop mode ',inline=True)
    # embed.add_field(name=f'`{PREFIX}volume`',value='Changes the bots volume ',inline=True)
    # embed.add_field(name=f'`{PREFIX}pause`',value='Pauses the song ',inline=True)
    # embed.add_field(name=f'`{PREFIX}resume`',value='Resumes the song ',inline=True)
    # embed.add_field(name=f'`{PREFIX}view`',value='Shows the queue ',inline=True)
    # embed.add_field(name=f'`{PREFIX}skip`',value='Skip music ',inline=True)
    for command in client.get_cog("Music").walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "No description"
        embed.add_field(
            name=f"`{PREFIX}{command.name}{command.signature if command.signature is not None else ''}`",
            value=description,
        )



    await ctx.send(embed=embed, view=view)




###############################################################################################################




@client.event
async def on_error(error, *args, **kwargs):
    try:
        formatted_args = '\n'.join([f'{args.index(arg)+1}) {str(arg)} ({type(arg)})' for arg in args])
        formatted_args = f"```py\n{formatted_args}```"
        for ERROR_CHANNEL in ERROR_CHANNELS:
            try:
                error_channel = await client.fetch_channel(int(ERROR_CHANNEL))
            except:
                print(f"Can't log errors to the channel with id `{ERROR_CHANNEL}`")
                continue
            exception = sys.exc_info()
            exc = "\n".join(
                traceback.format_exception(exception[0], exception[1], exception[2])
            )
            error_em = nextcord.Embed(
                title=exception[0].__name__,
                color=nextcord.Color.red(),
                description=f"**Error in**: `{error}`\n```py\n{exc}```\n{f'Args: {formatted_args}' if len(args) > 0 else ''}\n{f'Kwargs: {kwargs}' if len(kwargs) > 0 else ''}",
            )
            try:
                await error_channel.send(embed=error_em)
            except:
                ...
        print(exc)
    except:
        exception = sys.exc_info()
        exc = "\n".join(
            traceback.format_exception(exception[0], exception[1], exception[2])
        )
        formatted_args = '\n'.join([f'{args.index(arg)+1}) {str(arg)} ({type(arg)})' for arg in args])
        print(exc, "Args: \n"+formatted_args)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in client.commands]
        matches = get_close_matches(cmd, cmds)
        if len(matches) > 0:
            embed = nextcord.Embed(
                title="Invalid Command!",
                description=f"Command `{str(PREFIX)}{cmd}` not found, maybe you meant `{str(PREFIX)}{matches[0]}`?",
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed(
                title="Invalid Command!",
                description=f"Please type `{str(PREFIX)}help` to see all commands",
            )
            await ctx.send(embed=embed, delete_after=25.0)
        return
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f"You must wait `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em, delete_after=25.0)
        elif int(h) == 0 and int(m) != 0:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f" You must wait `{int(m)}` minutes and `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em, delete_after=25.0)
        else:
            em = nextcord.Embed(
                title="**Command on cooldown**",
                description=f" You must wait `{int(h)}` hours, `{int(m)}` minutes and `{int(s)}` seconds to use this command!",
            )
            await ctx.send(embed=em, delete_after=25.0)
        return
    if isinstance(error, commands.DisabledCommand):
        em = nextcord.Embed(
            title="Command Disabled",
            description="It seems the command you are trying to use has been disabled",
        )
        await ctx.send(embed=em, delete_after=25.0)
        return
    if isinstance(error, commands.MissingPermissions):
        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in error.missing_perms
        ]
        if len(missing) > 2:
            fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = " and ".join(missing)
        _message = "You require the `{}` permission to use this command.".format(fmt)
        em = nextcord.Embed(title="Invalid Permissions", description=_message)
        await ctx.send(embed=em, delete_after=25.0)
        return
    if isinstance(error, commands.MissingRequiredArgument):
        embed=Embed(title="Missing Required Arguments!", description=error, color=Color.red())
        await ctx.send(embed=embed, delete_after=25.0)
    if isinstance(error, commands.BotMissingPermissions):
        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in error.missing_perms
        ]
        if len(missing) > 2:
            fmt = "{}, and {}".format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = " and ".join(missing)
        _message = "I require the `{}` permission to use this command.".format(fmt)
        em = nextcord.Embed(title="Invalid Permissions", description=_message)
        await ctx.send(embed=em, delete_after=25.0)
        return
    if isinstance(error, commands.BadArgument):
        em = nextcord.Embed(
            title="Bad Argument",
            description="The library ran into an error attempting to parse your argument.",
        )
        await ctx.send(embed=em, delete_after=25.0)
        return
    if isinstance(error, nextcord.NotFound) and "Unknown interaction" in str(error):
        return
    exception = "\n".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    for ERROR_CHANNEL in ERROR_CHANNELS:
        try:
            error_channel = await client.fetch_channel(int(ERROR_CHANNEL))
        except:
            print(f"Can't Fetch The Error Channel With ID: `{ERROR_CHANNEL}`")
            return print(exception)
        error_em = nextcord.Embed(
            title=error.__class__.__name__,
            description=f"""
Message: ```txt\n{ctx.message.content}```
Command: {ctx.command}
Error Treaceback: ```py\n{exception}```""",
            color=nextcord.Color.red(),
        )
        try:
            await error_channel.send(embed=error_em)
        except:
            print(
                f"Was Not Able To Send The Error In The Channel With ID: `{error_channel.id}`"
            )
    em = nextcord.Embed(
        title="Error ;-;",
        description=f"There was an error in the command `{ctx.command}`\nThe developers have been informed about the error, please refrain from using this command again!",
    )
    await ctx.channel.send(
        embed=em,
        delete_after=25.0
    )  # Doing this so even when slash commands are implemented, the error handler still works just fine.
    print(exception)




@tasks.loop(seconds=69)
async def change_status():
    await client.change_presence(activity=nextcord.Game((choice(status))),status=nextcord.Status.idle)

client.run(TOKEN)