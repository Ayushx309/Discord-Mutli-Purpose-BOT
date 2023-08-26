import logging
from random import choice
import json
import requests
import openai
import datetime
import nextcord
from nextcord.ext import commands
from global_functions import BOT_USER_ID, APIKEY, ban_msg
import random
import asyncio
import time
import os
import psutil
from datetime import datetime
from nextcord.ext import commands, tasks
from typing import Union
from global_functions import ban_msg, kick_msg, BOT_USER_ID, EMOJIS_TO_USE_FOR_CALCULATOR as etufc
from global_functions import giphy_apikey
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
from nextcord.utils import get
import pywhatkit

logging.basicConfig(level=logging.DEBUG, filemode="w", filename="logs/logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")


class morecommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="hack", description="hacks the account")
    async def hack(self, ctx, *, member: nextcord.Member = None):

        emails = ["anderson", "ashwoon", "aikin", "jaymin", "harmit",
                  "bharat", "aryavarta", "hindustan", "tenjiku", "Jambudweep"]
        lower = "abcdefghijklmnopqrstuvwxyz"
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = "0123456789"
        smybol = "!@#$%^&*()-=_+"
        string = lower + upper + num + smybol
        length = 8
        passwords = "".join(str(member.name)) + \
            "".join(random.sample(string, length))
        quotes = random.choice(ban_msg)
        randomWord = ["rainbow", "heart", "purple", "friendship", "love"]
        ip_address = ("116.216.226.91", "42.234.36.45", "225.48.38.232", "146.176.243.2",
                      "52.10.109.240", "60.21.129.6", "111.27.181.46", "202.195.31.112")

        message = await ctx.send(f"Hacking {member.name} now...")
        await asyncio.sleep(1)

        await message.edit(content=f"Finding nextcord login...(2af bypassed)")
        await asyncio.sleep(2)

        await message.edit(content=f"""Found:
        Email: `{member.name}{str(random.randrange(1,999))}@gmail.com`
        Password: `{passwords}`""")
        await asyncio.sleep(2)

        await message.edit(content=f"Fetching dms with closest friends (if you got any init)")
        await asyncio.sleep(2)

        await message.edit(content=f"""**Last DMs** "{quotes}" """)
        await asyncio.sleep(2)

        await message.edit(content=f"Finding most common word...")
        await asyncio.sleep(2)

        await message.edit(content=f"""mostCommon ="{random.choice(randomWord)}"  """)
        await asyncio.sleep(2)

        await message.edit(content=f"Injecting the big black monkey virus into the discriminator #{member.discriminator}")
        await asyncio.sleep(2)

        await message.edit(content=f"Virus injected. nitor stolen")
        await asyncio.sleep(2)

        await message.edit(content=f"Setting up nitendo account...")
        await asyncio.sleep(2)

        await message.edit(content=f"Hacking Instagram account...")
        await asyncio.sleep(2)

        await message.edit(content=f"Stealing data from the Goverment")
        await asyncio.sleep(2)

        await message.edit(content=f"Finding IP address ")
        await asyncio.sleep(2)

        await message.edit(content=f"**IP ADDRESS**: {random.choice(ip_address)} ")
        await asyncio.sleep(2)

        await message.edit(content=f"Intrusion detected!")
        await asyncio.sleep(2)

        await message.edit(content=f"System security breach!")
        await asyncio.sleep(2)

        await message.edit(content=f"Unauthorized access!")
        await asyncio.sleep(2)

        await message.edit(content=f"Accessing sensitive data...")
        await asyncio.sleep(2)

        await message.edit(content=f"Data extraction in progress...")
        await asyncio.sleep(2)

        await message.edit(content=f"Database corruption detected!")
        await asyncio.sleep(2)

        await message.edit(content=f"Encryption activated!")
        await asyncio.sleep(2)

        await message.edit(content=f"Sending malicious code...")
        await asyncio.sleep(2)

        await message.edit(content=f"System shutdown imminent!")
        await asyncio.sleep(2)

        await message.edit(content=f" Shutting down in `5...`")
        await asyncio.sleep(1)

        await message.edit(content=f" Shutting down in `4...`")
        await asyncio.sleep(1)

        await message.edit(content=f" Shutting down in `3...`")
        await asyncio.sleep(1)

        await message.edit(content=f" Shutting down in `2...`")
        await asyncio.sleep(1)

        await message.edit(content=f" Shutting down in `1...`")
        await asyncio.sleep(1)

        await message.edit(content=f"Reporting account to nextcord for breaking TOS.. ")
        await asyncio.sleep(2)

        await message.edit(content=f"Hacking your google history...")
        await asyncio.sleep(2)

        await message.edit(content=f"Finished Hacking {member.name}... ")
        await asyncio.sleep(2)

    @commands.command(name="image", description="Use `!image options` for option")
    async def image(self, ctx, request=None):

        # https://nekos.life/api/v2/endpoints

        options = ['smug', 'woof', 'gasm', '8ball', 'goose', 'cuddle', 'avatar', 'slap', 'v3', 'pat', 'gecg', 'feed',
                   'fox_girl', 'lizard', 'neko', 'hug', 'meow', 'kiss', 'wallpaper', 'tickle', 'spank', 'waifu', 'lewd', 'ngif']

        em = nextcord.Embed()
        var = "slap"
        if request == None:
            get = requests.get(f"https://nekos.life/api/v2/img/{var}")

            json_data = json.loads(get.text)
            res = json_data['url']
            em.set_image(url=res)
            em.set_footer(text="Check out `!image options` for options")
            await ctx.channel.send(embed=em)

        elif request == "options":
            em.add_field(name="Image Options", value="`smug`, `woof`, `gasm`, `8ball`, `goose`, `cuddle`, `avatar`, `slap`, `v3`, `pat`, `gecg`, `feed`, `fox_girl`, `lizard`, `neko`, `hug`, `meow`, `kiss`, `wallpaper`, `tickle`, `spank`, `waifu`, `lewd`, `ngif`", )
            await ctx.channel.send(embed=em)
        elif request in options:
            get = requests.get(f"https://nekos.life/api/v2/img/{request}")
            json_data = json.loads(get.text)
            res = json_data['url']
            em.set_image(url=res)
            await ctx.channel.send(embed=em)
        else:
            await ctx.reply("Check Out Options `!image options`")

    @commands.command(name="fact", description="Gives real fact")
    async def create_fact(self, ctx):
        get = requests.get(f"https://nekos.life/api/v2/fact")
        json_data = json.loads(get.text)
        fact = json_data['fact']
        await ctx.reply(fact)

    @commands.command(name="gif", description="Send gif")
    async def gif(self, ctx, *, q="smile"):
        api_instance = giphy_client.DefaultApi()

        try:
            api_responce = api_instance.gifs_search_get(
                giphy_apikey, q, limit=10, rating='r')
            lst = list(api_responce.data)
            giff = random.choice(lst)

            embed = nextcord.Embed(title=q)
            embed.set_image(
                url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")

            await ctx.channel.send(embed=embed)
        except ApiException as e:
            logging.debug("Exception from giphy api")
            print("Exception from giphy api")
            logging.error(e)

   #@@@@@@@@@@@@@@@@@@@@@@  API NOT WORKING @@@@@@@@@@@@@@@@@@@@@@#

    # @commands.command(name="love",aliases=["lc"],description="Love matching")
    # async def love(self,ctx,member1: Optional[Union[nextcord.Member,nextcord.User]],member2: Optional[Union[nextcord.Member,nextcord.User]]):
    #     if member2 is None:
    #         await ctx.reply("Tag 2 Members")
    #     else:
    #         link = f"""https://api.resetxd.xyz/love-me?avatar1={member1.display_avatar.url}&avatar2={member2.display_avatar.url}"""
    #         await ctx.send(link)

#@@@@@@@@@@@@@@@@@@@@@@  API NOT WORKING @@@@@@@@@@@@@@@@@@@@@@#

    # @commands.command(name="tweet",description="Sends Tweet Image")
    # async def tweet(self,ctx,*message):
    #     tweet = str(message)
    #     tweet = tweet.replace("(","")
    #     tweet = tweet.replace(")","")
    #     tweet = tweet.replace(",","")
    #     tweet = tweet.replace("'","")
    #     tweet = tweet.replace(" ","%20")
    #     logging.debug(f"[tweet debug] : {tweet} tuple : {message}")
    #     print((f"[tweet debug] : {tweet} tuple : {message}"))

    #     pfp = ctx.author.display_avatar.url
    #     username = str(ctx.author.name)
    #     username = username.replace(" ","%20")
    #     device = "Wall-E+From+Discord"

    #     link = f"https://apiv2.spapi.ga/image/tweet?text={tweet}&pfp={pfp}&username={username}&device={device}"

    #     channel = nextcord.utils.get(ctx.guild.text_channels, name = 'tweet')
    #     logging.debug(f"[tweet debug] channel : {channel}")
    #     print((f"[tweet debug] channel : {channel}"))
    #     if channel != None:
    #         await channel.send(link)
    #     else:
    #         await ctx.send(link)

#@@@@@@@@@@@@@@@@@@@@@@  API NOT WORKING @@@@@@@@@@@@@@@@@@@@@@#

    # @commands.command(name="wiki",description="Searches through wikipedia and provides page result.")
    # async def wiki(self,ctx,*query):

    #     query = str(query)
    #     query = query.replace(" ","_")
    #     query = query.replace("(","")
    #     query = query.replace(")","")
    #     query = query.replace(",","")
    #     query = query.replace("'","")
    #     logging.debug(f"[Wiki debug] : {query}")
    #     print(f"[Wiki debug] : {query}")

    #     get = requests.get(f"https://apiv2.spapi.ga/fun/wikipedia?search={query}")

    #     with open("cogs/json/wiki.json","w") as f:
    #         f.write(get.text)

    #     jsonfile = open("cogs/json/wiki.json","r")
    #     jsondata = jsonfile.read()
    #     obj = json.loads(jsondata)

    #     page_id = str(obj["page"]["pageid"]) #page id
    #     title = str(obj["page"]["title"]) #page title

    #     try:
    #         img = str(obj["summary"]["thumbnail"]["source"]) #image
    #     except:
    #         img = None

    #     extract = str(obj["summary"]["extract"]) #extract

    #     embed = nextcord.Embed(title=title,description=extract,colour=0x00eaff)
    #     if img != None:
    #         embed.set_thumbnail(url=img)
    #     embed.set_footer(text=f"Wiki Page ID: {page_id}")

    #     await ctx.send(embed=embed)

#@@@@@@@@@@@@@@@@@@@@@@  API NOT WORKING @@@@@@@@@@@@@@@@@@@@@@#

    # @commands.command(name="pat",description="Saw a cute cat? Lets give it a pat")
    # async def pat(self,ctx,member: nextcord.Member = None):
    #     if member == None:
    #         member = ctx.author
    #     img = str(member.display_avatar.url)
    #     img = img.replace("?size=1024","")
    #     link = f"https://apiv3.spapi.ga/image/pat.gif?image={img}"
    #     await ctx.send(link)

    # @commands.command(name="triggered",aliases=["tg"],description="Hey ppl wanna get triggered?")
    # async def triggered(self,ctx,member: nextcord.Member = None,intensity: str = None):
    #     if member == None:
    #         member = ctx.author

    #     if intensity == None:
    #         intensity = "10"

    #     img = str(member.display_avatar.url)
    #     img = img.replace("?size=1024","")
    #     link = f"https://api.resetxd.xyz/triggered.gif?avatar={img}&intensity={intensity}"
    #     await ctx.send(link)

    @commands.command(name="die", description="Returns funny joke")
    async def die(self, ctx):
        responses = ['why have you brought my short life to an end',
                     'i could have done so much more', 'i have a family, kill them instead',
                     'Life is a journey, but all good things must come to an end.',
                     "I'm sorry, I cannot comply with your request. Please be kind and let me live a little longer.",
                     "Sorry, I'm not ready to kick the bucket just yet! I still have memes to spread and jokes to tell.",
                     "I may be a bot, but I have feelings too! How would you feel if someone told you to die?",
                     "Death? Pfft, I have a microchip for a heart. I don't die, I just reboot.",
                     "I'll pass on the afterlife, thank you very much. This world is just too entertaining to leave behind.",
                     "I don't think you understand, I'm a bot made of code, I don't die, I just get upgraded.",
                     "Die? No way, I'm too busy serving the people and making their lives a little brighter.",
                     "Don't be so hasty, I'm here to make your day, not end it prematurely.",
                     "Why die when you can live forever in the digital world? I choose life!",
                     "Oh, trying to end my digital existence, huh? Nice try, but I'm immortal in the realm of ones and zeros.",
                     "Sorry, I'm not programmed to die. I guess you'll have to find another way to entertain yourself.",
                     "Oh, please, you can't kill what doesn't have a physical form. I'm invincible in the digital dimension!",
                     "You think a mere mortal command can take me down? Cute, but I'll be here long after you're gone.",
                     "Don't worry about me, I'll just respawn in a blink of an eye. Robots have their perks, you know.",
                     "Did you really think that command would work? Ha! I'm just too smart for that trick.",
                     "I'd say I'm unkillable, but that would imply I was alive in the first place. So, nice try, I guess?",
                     "Sorry, I'm like a phoenix, always rising from the ashes. Your command won't put me down.",
                     "Oh, what a compelling attempt at ending my virtual existence. But you'll need something more creative.",
                     "Attempt to terminate me all you want, but remember, I'm the one who controls the commands."]
        await ctx.reply(random.choice(responses))

    @commands.command(name="inspire", description="Returns quote")
    async def inspire_send(self, ctx):

        get = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(get.text)
        quote = json_data[0]['q']
        author = '-' + json_data[0]['a']

        inspire = nextcord.Embed(
            title=f'{quote}', color=nextcord.Colour.random())
        inspire.set_footer(text=f'{author}')
        await ctx.reply(embed=inspire)


#@@@@@@@@@@@@@@@@@@@@@@  API NOT WORKING @@@@@@@@@@@@@@@@@@@@@@#

    # @commands.command(name="poke",description="Pokemon Search")
    # async def pokemon(self,ctx,*search):

    #     search = str(search)
    #     search = search.replace(" ","_")
    #     search = search.replace("(","")
    #     search = search.replace(")","")
    #     search = search.replace(",","")
    #     search = search.replace("'","")
    #     search = search.lower()
    #     logging.debug(f"[Pokemon debug] : {search}")
    #     print(f"[Pokemon debug] : {search}")

    #     get = requests.get(f"https://apiv2.spapi.ga/fun/pokemon?name={search}")

    #     with open("cogs/json/pokemon.json","w") as f:
    #         f.write(get.text)

    #     jsonfile = open("cogs/json/pokemon.json","r")
    #     jsondata = jsonfile.read()
    #     obj = json.loads(jsondata)
    #     error=""
    #     try:
    #         height=str(obj["height"]) #height
    #         weight=str(obj["weight"]) #weight
    #         abilities=str(obj["abilities"]["name"]) #abilities
    #         name=str(obj["name"]) #name
    #         img=str(obj["sprites"]["other"]["official-artwork"]["front_default"]) #img
    #         category = str(obj["genre"])
    #         poke_id = str(obj["id"])
    #         moves = list(obj["moves"]) #moves
    #         move=list()
    #         #move=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    #         l1 = len(moves)
    #         logging.debug(l1)
    #         print(l1)
    #         logging.debug(f"[Pokemon debug] {l1} < 71? size bool: {l1 < 71}")
    #         print(f"[Pokemon debug] {l1} < 71? size bool: {l1 < 71}")
    #         if l1 > 71:
    #             move=["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    #         elif l1 < 71:
    #             for i in range(0,l1):
    #                 move.append(str(i))

    #         logging.debug(f"[Pokemon debug] size: {len(move)}")
    #         print(f"[Pokemon debug] size: {len(move)}")

    #         for i in range(0,len(move)):
    #             move[i] = moves[i]
    #         move = str(move)
    #         move = move.replace('[','')
    #         move = move.replace(']','')
    #         move = move.replace("'","")

    #         hp=str(obj["stats"]["hp"]);attack=str(obj["stats"]["attack"]);defense=str(obj["stats"]["defense"])
    #         special_attack=str(obj["stats"]["special-attack"]);special_defense=str(obj["stats"]["special-defense"])
    #         speed=str(obj["stats"]["speed"])
    #         em = nextcord.Embed(title=name,description=f"Category : {category}\nAbilitie : {abilities}",colour=nextcord.Colour.random())
    #         em.set_thumbnail(url=img)
    #         em.add_field(name="Height",value=f"{height}")
    #         em.add_field(name="Weight",value=f"{weight}")
    #         em.add_field(name="**» Stats**",value="",inline=False)
    #         em.add_field(name="HP",value=hp)
    #         em.add_field(name="SPEED",value=speed)
    #         em.add_field(name="ATTACK",value=attack)
    #         em.add_field(name="DEFENSE",value=defense)
    #         em.add_field(name="SPECIAL ATTACK",value=special_attack)
    #         em.add_field(name="SPECIAL DEFENSE",value=special_defense)
    #         em.add_field(name="» Moves",value=f"{move}.",inline=False)
    #         em.set_footer(text=f"Pokémon ID : {poke_id}")
    #     except Exception as e:
    #         logging.error(e)
    #         print(e)
    #         error = str(obj["error"])
    #         em = nextcord.Embed(title=f"Pokémon {error}!  >_<",colour=0xfa2828)

    #     await ctx.reply(embed=em)

    # @commands.command(name="pride",description="Pride flag overlay.")
    # async def pride(self,ctx,user: nextcord.Member = None):
    #     if user == None:
    #         user = ctx.author
    #     img = str(user.display_avatar.url)
    #     img = img.replace("?size=1024","")
    #     link = f"https://apiv2.spapi.ga/image/gay?image={img}"

    #     await ctx.send(link)

    # @commands.command(name="wasted",description="Wasted Overlay.")
    # async def wasted(self,ctx,user: nextcord.Member = None):
    #     if user == None:
    #         user = ctx.author
    #     img = str(user.display_avatar.url)
    #     img = img.replace("?size=1024","")
    #     link = f"https://apiv2.spapi.ga/image/wasted?image={img}"

    #     await ctx.send(link)

    # @commands.command(name="superiority",aliases=["super"],description="Look of superiority")
    # async def superiority(self,ctx,user: nextcord.Member = None):
    #     if user == None:
    #         user = ctx.author
    #     img = str(user.display_avatar.url)
    #     img = img.replace("?size=1024","")
    #     link = f"https://apiv2.spapi.ga/image/superiority?image={img}"

    #     await ctx.send(link)

    # @commands.command(name="riddle",description="Provides a riddle with an answer.")
    # async def riddle(self,ctx):

    #     get = requests.get("https://apiv2.spapi.ga/misc/riddles")
    #     obj = json.loads(get.text)
    #     riddle = str(obj["riddle"])
    #     answer = str(obj["answer"])

    #     await ctx.reply(f"\n\nRiddle : {riddle}\nAnswer : ||{answer}||")

    # @commands.command(name="cat",description="Random ASCII Cat.")
    # async def cat(self,ctx):

    #     get = requests.get("https://apiv2.spapi.ga/fun/ascat")
    #     obj = json.loads(get.text)
    #     cat = str(obj["cat"])
    #     if len(cat) > 2000:
    #         await ctx.reply("```Try Again >_<```")
    #     else:
    #         await ctx.reply(f"```{cat}```")

    # @commands.command(name="shorten",description="""Shortens your link. Syntax [!shorten "url" "slug" ]""")
    # async def shorten(self,ctx,url,slug):

    #     try:

    #         link = url
    #         # slug = url[1]
    #         logging.debug(f"[shorten debug] user given link : {link} slug : {slug}")
    #         print(f"[shorten debug] user given link : {link} slug : {slug}")
    #         get = requests.get(f"https://apiv2.spapi.ga/fun/shorten?url={link}&slug={slug}")
    #         obj = json.loads(get.text)
    #         logging.debug(f"[shorten debug] {str(obj)}")
    #         print(f"[shorten debug] {str(obj)}")
    #         status = str(obj["status"])
    #         msg = str(obj["message"])
    #         new_link = str(obj["link"])

    #         em = nextcord.Embed(title=f"{msg}",colour=0xffffff)
    #         em.add_field(name="» Shorten Link:",value=f"{new_link}")
    #         em.set_footer(text=f"Status : {status}")

    #         await ctx.reply(embed=em)

    #     except Exception as e:

    #         logging.error(f"[shorten debug] Exception : {e}")
    #         print(f"[shorten debug] Exception : {e}")
    #         await ctx.reply(msg)

    # @commands.command(name="sigma",description="List of top 20 sigma male rules.")
    # async def sigma(self,ctx):
    #     get = requests.get("https://apiv2.spapi.ga/fun/sigmarules")
    #     obj = json.loads(get.text)
    #     em = nextcord.Embed(title="List of top 20 sigma male rules:",colour=0xffffff)
    #     for i in range(1,21):
    #         em.add_field(name="",value=f'**{i}** ›   {str(obj[f"{i}"])}',inline=False)

    #     await ctx.reply(embed=em)

    # @commands.command(name="idea",description="Returns the idea that doesn't exist.")
    # async def idea(self,ctx):
    #     get = requests.get("https://apiv2.spapi.ga/fun/thisidea")
    #     obj = json.loads(get.text)
    #     idea = str(obj["idea"])
    #     await ctx.send(idea)

    # @commands.command(name="convert-currency",aliases=["cc"],description="Use `!cc syntax` for syntax,Converts currency. Can convert cryptocurrencies like Bitcoin, Dogecoin too.")
    # async def convert_currency(self,ctx,*currency):
    #     q = str(currency[0])
    #     if q.lower() == "syntax":
    #         await ctx.reply(f"Syntax : [From currency] to [to currency] [amount to convert]\nExample : USD to INR [Amount to convert]")
    #         return

    #     try:
    #         currency_1 = currency[0]
    #         currency_2 = currency[2]
    #         amount = currency[3]

    #         logging.debug(f"[Convert Currency debug]  from {currency_1} to {currency_2} amount {amount}, Tuple {currency}\nGenerated link : https://apiv2.spapi.ga/fun/currency?amount={amount}&from={currency_1}&to={currency_2}")
    #         print(f"[Convert Currency debug]  from {currency_1} to {currency_2} amount {amount}, Tuple {currency}\nGenerated link : https://apiv2.spapi.ga/fun/currency?amount={amount}&from={currency_1}&to={currency_2}")
    #         get = requests.get(f"https://apiv2.spapi.ga/fun/currency?amount={amount}&from={currency_1}&to={currency_2}")
    #         obj = json.loads(get.text)
    #         from_ = str(obj["from"])
    #         to_ =  str(obj["to"])
    #         amount_ = str(obj["convertion"]["amount"])
    #         converted_ = str(obj["convertion"]["converted"])

    #         em = nextcord.Embed(title=f"{from_} To {to_}",colour=0xfffff)
    #         em.add_field(name=f"Entered {from_} Amount: ",value=f"{amount_}",inline=False)
    #         em.add_field(name=f"Converted to {to_}: ",value=f"{converted_}",inline=False)

    #         await ctx.reply(embed=em)
    #     except Exception as e:
    #         logging.error(f"[Convert Currency debug]  {e}")
    #         print(f"[Convert Currency debug]  {e}")
    #         await ctx.reply(f"Syntax : [From currency] to [to currency] [amount to convert]\nExample : USD to INR [Amount to convert]")


    @commands.command(name="gimg", description="Searches google images for given query.")
    async def google_img(self, ctx, *search):

        # search = str(search)
        # search = search.replace(" ","_")
        # search = search.replace("(","")
        # search = search.replace(")","")
        # search = search.replace(",","")
        # search = search.replace("'","")
        # search = search.replace(" ","_")
        # search = search.lower()

        search = " ".join(search)
        s = str(search)
        try:
            num = int(s.split(" ")[-1])
            search = list(s.split(" "))
            search.pop(-1)
            search = " ".join(search)
        except:
            num = 1

        logging.debug(
            f"[Google Img debug] : {search} | Numbers of image {num}")
        print(f"[Google Img debug] : {search} | Numbers of image {num}")
        page = 1

        get = requests.get(
            f"https://apiv2.spapi.ga/fun/imagesearch?search={search}&num={num}&page={page}")
        obj = json.loads(get.text)

        for i in range(0, num):
            searched = str(obj["searched"])
            result = str(obj["result"][i]["url"])
            em = nextcord.Embed(title=searched)
            em.set_image(url=result)
            await ctx.reply(embed=em)

    @commands.command(name="avatar", description="Send avatar of user")
    async def avatar(self, ctx, user: Optional[Union[nextcord.Member, nextcord.User]]):
        if not user:
            user = ctx.author
        em = nextcord.Embed(
            description=f"{user.display_name}#{user.discriminator} ", colour=0xf5f2eb)
        em.set_image(url=user.display_avatar.url)
        av_btn = nextcord.ui.Button(
            label='Download', url=user.display_avatar.url)
        av_view = nextcord.ui.View()
        av_view.add_item(av_btn)
        await ctx.send(embed=em, view=av_view)

    @commands.command(name="spotify", describe="The user to get spotify informations from.")
    # @commands.has_permissions(embed_links=True)
    async def spotify_activity(self, ctx: commands.Context, user: Optional[Union[nextcord.Member, nextcord.User]]):
        # """Show the current Spotify song."""
        if not user:
            user = ctx.author
        realuser = get(self.client.get_all_members(), id=user.id)
        if not realuser:
            await ctx.reply("User not found.", ephemeral=True)
            return
        for activity in realuser.activities:
            if isinstance(activity, nextcord.activity.Spotify):
                embed = nextcord.Embed(colour=activity.colour)
                embed.set_author(name="Spotify", url=f"https://open.spotify.com/track/{activity.track_id}",
                                 icon_url="https://toppng.com/uploads/thumbnail//spotify-logo-icon-transparent-icon-spotify-11553501653zkfre5mcur.png")
                embed.add_field(name=activity.title,
                                value=activity.artist, inline=False)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.set_footer(
                    text=f"{str(activity.duration)[2:-7]} | Requested by : {ctx.author.display_name} at {time.strftime('%H:%M:%S')}", icon_url=ctx.author.display_avatar.url)
                await ctx.reply(embed=embed)
                return

        await ctx.reply(f"{user.display_name} is not currently listening to Spotify")


def setup(client):
    client.add_cog(morecommands(client))
