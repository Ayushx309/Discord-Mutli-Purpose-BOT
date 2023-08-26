import asyncio
import nextcord
import typing
from nextcord.voice_client import VoiceClient
import youtube_dl
from nextcord.ext import commands
from nextcord.ext.commands import MissingRequiredArgument
from timeit import default_timer as timer
from global_functions import PREFIX
import logging
import requests
import json
import functools
import datetime
import random
import time



logging.basicConfig(level=logging.DEBUG,filemode="w",filename="logs/logs.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")







class Music(commands.Cog):
    
    

    def __init__(self, client):
        self.client = client
        self.loop = False
        self.playing = False
        self.is_connected = False
        self.joinfromplay = False
        self.queue = []
        self.currentsonginfo = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.opts = {'extract_flat': True, 'skip_download': True}
        self.youtube_url = "https://www.youtube.com/watch?v="
        self.indexinfoqueue = 0
        self.message = None 
        self.playing_ctx = None
        
        
            
    
    # @staticmethod
    # def getUrl(URL):
    #     print(f"[URL] {URL}")
    #     with open("cogs/text_files/music_url.txt","w") as f:
    #         f.write(str(URL))
        
    


    @commands.command(description="Makes the bot join the voice channel.")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in any channel!")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
                await ctx.send("🎆 Connected and Ready to Play")
                if not self.joinfromplay:
                    await self.timer(ctx)
            else:
                await ctx.voice_client.move_to(voice_channel)
            self.is_connected = True

    @commands.command(description="Plays music.")
    async def play(self, ctx, url:str):
        
        if url.startswith("https://"):
            pass
        else:
            temp = f'ytsearch:{url}'
            url = temp
            print("✅ {}".format(url))

        if not self.is_connected:
            self.joinfromplay = True
            await self.join(ctx)    
        if self.is_connected:
            with youtube_dl.YoutubeDL(self.opts) as ydl:
                try:
                    ydl.cache.remove()
                    info = ydl.extract_info(url, download=False)
                    logging.info(info)
                    # with open('cogs/text_files/music_info.txt','w') as f:
                    #     f.write(str(info))
                except youtube_dl.DownloadError as error:
                    await ctx.send("Errore:" + str(error))
            if '_type' in info:
                if info.get('_type') == 'playlist':
                    for x in info.get('entries'):
                        raw_url_song = self.youtube_url + x['id']
                        if 'title' in x.keys():
                            titleartist = x['title']
                        if 'duration' in x.keys():
                            duration = x['duration']
                        try:
                            self.queue.append([raw_url_song, titleartist, duration])
                        except:
                            if titleartist:
                                self.queue.append([raw_url_song, titleartist, ' '])
                            else:
                                self.queue.append([raw_url_song, '', duration])
                        print(titleartist + " Adding to Queue, Total Songs in Queue: " + str(len(self.queue)))
                    if not self.playing:
                        await ctx.send("Playlist Detected")
                        self.playing = True
                        await self.real_play(ctx, ctx.voice_client, self.queue[0][0])
                    else:
                        await ctx.send("Playlist Added to Queue ✅")
            else:
                raw_url_song = info['formats'][0]['url']
                if 'title' in info.keys():
                    titleartist = info['title']
                if 'duration' in info.keys():
                    duration = info['duration']
                self.queue.append([raw_url_song, titleartist, duration])
                if self.playing:
                    await ctx.send("Song Added to Queue ✅")
                else:
                    self.playing = True
                    await self.real_play(ctx, ctx.voice_client, raw_url_song)

    async def real_play(self, ctx, vc, url):
        if self.loop:
            source = await nextcord.FFmpegOpusAudio.from_probe(url, **self.FFMPEG_OPTIONS)
            await asyncio.sleep(0.5)
            vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.real_play(ctx, vc, url), self.client.loop))
            await self.info(ctx)
        else:
            if len(self.queue) > 0:
                self.currentsonginfo = self.queue.pop(0)
                with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
                    try:
                        ydl.cache.remove()
                        await asyncio.sleep(0.5)
                        info = ydl.extract_info(self.currentsonginfo[0], download=False)
                    except youtube_dl.DownloadError as error:
                        await ctx.send("Errore:" + str(error))
                processed_url_song = info['formats'][0]['url']
                # self.music_url = info['formats'][0]['url']
                # self.thumbnail = info.get('thumbnail')
                # with open('cogs/text_files/music_thumbnail.txt','w') as f:
                #     f.write(str(self.thumbnail))

                
                with open('cogs/json/music_info.json','w') as file:
                    data = {
                        'musicUrl': str(info.get('url')),
                        'musicThumbnail': str(info.get('thumbnail')),
                        'musicTitle': str(info.get('title')),
                        'musicDuration': str(info.get('duration')),
                        'musicUploader': {'uploaderName': str(info.get('uploader')), 'uploaderUrl': str(info.get('uploader_url'))}
                    }
                    json.dump(data,file)


                source = await nextcord.FFmpegOpusAudio.from_probe(processed_url_song, **self.FFMPEG_OPTIONS)
                await asyncio.sleep(0.5)
                vc.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.real_play(ctx, vc, processed_url_song), self.client.loop))
                await self.info(ctx)
            else:
                self.playing = False
                await self.timer(ctx)

    @commands.command(description="Skip music.")
    async def skip(self, ctx):
        try:
            if len(self.queue) > 0:
                next_song_url = self.queue[0][0]
                ctx.voice_client.stop()
                await ctx.send("⏩ Skipped Song")
                await self.real_play(ctx, ctx.voice_client, next_song_url)
            else:
                ctx.voice_client.stop()
                self.reset()
                await ctx.send("⏭ Skipped Song: No other Songs in Queue")
        except AttributeError as e:
            await ctx.send("Error: " + str(e))

    @commands.command(name="skipx", description="Skips N numbers of music.")
    async def skipx(self, ctx, number_skip:int):
        try:
            if number_skip is None:
                await ctx.send("❗️Command !skipx Requires a Value!")
            else:
                if len(self.queue) > number_skip:
                    for x in range(1, number_skip-1):
                        self.currentsonginfo = self.queue.pop(0)
                    ctx.voice_client.stop()
                    await ctx.send("⏭ Hai Skippato:  " + str(number_skip) + "Songs")
                    await self.real_play(ctx, ctx.voice_client, self.currentsonginfo[0])
        except MissingRequiredArgument as e:
            print("Error: " + str(e))

    @commands.command(description="Stops the music.")
    async def stop(self, ctx):
        try:
            ctx.voice_client.stop()
            self.reset()
            await ctx.send("⏹ Stopped")
            await self.timer(ctx)
        except:
            await ctx.send("Error Stop!")

    @commands.command(description="Pauses the music.")
    async def pause(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.send("⏸ Music Paused")
        except:
            await ctx.send("Error Pause!")

    @commands.command(description="Resumes the music.")
    async def resume(self, ctx):
        try:
            ctx.voice_client.resume()
            await ctx.send("▶️ I start playing again")
        except:
            await ctx.send("Error Resume!")

    @commands.command(description="Toggles loop mode.")
    async def loop(self, ctx):
        if self.loop:
            self.loop = False
            await ctx.send("❗️Loop Disabled")
        else:
            self.loop = True
            await ctx.send("🔁 Loop Enable")

    @commands.command(description="Info of current playing music.")
    async def info(self, ctx):
        # with open("cogs/text_files/music_url.txt","r") as f:
        #     data_url = f.read()
        # self.music_url = data_url
        # print(f"[MUSIC URL] {self.music_url}")
        # # u = Song()
        # # u.create_embed()
        # # with open("cogs/text_files/music_thumbnail","r") as f:
        # #     data_thumbnail = f.read()
        # # self.thumbnail = data_thumbnail
        with open('cogs/json/music_info.json','r') as file:
            jsondata = file.read()
        data = json.loads(jsondata)
        self.music_url = data['musicUploader']['uploaderUrl']
        self.thumbnail = data['musicThumbnail']
        self.loopTime = data['musicDuration']
        self.playing_ctx = ctx



        try:
            async with ctx.typing():
                if self.loop:
                    if not len(self.currentsonginfo) == 0:
                        try:

                            minutes = "{:0>8}".format(str(datetime.timedelta(seconds=self.currentsonginfo[2])))
                            e = nextcord.Embed(title=f"🔂\tI play again",description=f"**[{str(self.currentsonginfo[1])}]({str(self.music_url)})**",color=0x2b2d31)
                            try:
                                # url = Music.gimg(str(self.currentsonginfo[1]))
                                e.set_image(url=self.thumbnail)
                            except:
                                ...
                            ### embed Two
                            e2 = nextcord.Embed(color=0x2b2d31)
                            e2.set_image(url="https://media1.tenor.com/images/b3b66ace65470cba241193b62366dfee/tenor.gif")
                        
                            e.set_footer(text=f"Duration: {str(minutes)}")
                
                            await ctx.send(embed=e)
                            self.message = await ctx.send(embed=e2)
                            reactions = {'▶️':"play",'⏸️':"pause",'⏭️':"skip",'🔀':"shuffle",'⏹️':"stop",'🔁':"loop"}
                            for i in reactions:
                                await self.message.add_reaction(str(i))
                            

                            # await ctx.send("🔂 I play again:  " + str(self.currentsonginfo[1]) + "\n" + "⏲️ Duration:  " + str(minutes))
                        except:

                            e = nextcord.Embed(title=f"🔂\tI play again",description=f"**[{str(self.currentsonginfo[1])}]({str(self.music_url)})**",color=0x2b2d31)
                            try:
                                # url = Music.gimg(str(self.currentsonginfo[1]))
                                e.set_image(url=self.thumbnail)
                            except:
                                ...
                            ### embed Two
                            e2 = nextcord.Embed(color=0x2b2d31)
                            e2.set_image(url="https://media1.tenor.com/images/b3b66ace65470cba241193b62366dfee/tenor.gif")
                        
                            e.set_footer(text=f"\nDuration: {str(self.currentsonginfo[2])}")
                
                            await ctx.send(embed=e)
                            self.message = await ctx.send(embed=e2)
                            reactions = {'▶️':"play",'⏸️':"pause",'⏭️':"skip",'🔀':"shuffle",'⏹️':"stop",'🔁':"loop"}
                            for i in reactions:
                                await self.message.add_reaction(str(i))

                
                            # await ctx.send("🔂 I play again:  " + str(self.currentsonginfo[1]) + "\n" + "⏲️ Duration:  " + str(self.currentsonginfo[2]))
                else:
                    if not len(self.currentsonginfo) == 0:
                        try:
                            
                            minutes = "{:0>8}".format(str(datetime.timedelta(seconds=self.currentsonginfo[2])))
                            e = nextcord.Embed(title=f"🎵\tNow playing",description=f"**[{str(self.currentsonginfo[1])}]({str(self.music_url)})**",color=0x2b2d31)
                            try:
                                # url = Music.gImg(str(self.currentsonginfo[1]))
                                e.set_image(url=self.thumbnail)
                            except:
                                ...
                            ### embed Two
                            e2 = nextcord.Embed(color=0x2b2d31)
                            e2.set_image(url="https://media1.tenor.com/images/b3b66ace65470cba241193b62366dfee/tenor.gif")
                        
                            e.set_footer(text=f"\nDuration: {str(minutes)}")
                
                            await ctx.send(embed=e)
                            self.message = await ctx.send(embed=e2)
                            reactions = {'▶️':"play",'⏸️':"pause",'⏭️':"skip",'🔀':"shuffle",'⏹️':"stop",'🔁':"loop"}
                            for i in reactions:
                                await self.message.add_reaction(str(i))
                            
                
                            # await ctx.send("🎵 Now playing:  " + str(self.currentsonginfo[1]) + "\n" + "⏲️ Duration:  " + str(minutes))
                        except:
                            
                            e = nextcord.Embed(title=f"🎵\tNow playing",description=f"**[{str(self.currentsonginfo[1])}]({str(self.music_url)})**",color=0x2b2d31)
                            try:
                                # url = Music.gimg(str(self.currentsonginfo[1]))
                                e.set_image(url=self.thumbnail)
                            except:
                                ...
                            ### embed Two
                            e2 = nextcord.Embed(color=0x2b2d31)
                            e2.set_image(url="https://media1.tenor.com/images/b3b66ace65470cba241193b62366dfee/tenor.gif")
                        
                            e.set_footer(text=f"\nDuration: {str(self.currentsonginfo[2])}")
                
                            await ctx.send(embed=e)
                            self.message = await ctx.send(embed=e2)
                            reactions = {'▶️':"play",'⏸️':"pause",'⏭️':"skip",'🔀':"shuffle",'⏹️':"stop",'🔁':"loop"}
                            for i in reactions:
                                await self.message.add_reaction(str(i))

                
                            # await ctx.send("🎵 Now playing:  " + str(self.currentsonginfo[1]) + "\n" + "⏲️ Duration:  " + str(self.currentsonginfo[2]))
        except:
            await ctx.send("Error Info!")

       
    @commands.Cog.listener()
    async def on_reaction_add(self,reaction, user):
       

        reactions = {'▶️':"play",'⏸️':"pause",'⏭️':"skip",'🔀':"shuffle",'⏹️':"stop",'🔁':"loop"}

        # print(f"[User] {user}")
        # print(f'[Author] {reaction.message.author}')
        # print(f'self message {self.message}')
        # print(f'reaction message {reaction.message}')
        # if user != self.client.user and user == user and (str(reaction.emoji) == '▶️' or '⏸️' or '⏭️'or '🔀'or '⏹️' or '🔁'):

        
        # server = self.playing_ctx.msg.guild
        server = reaction.message.guild
        vc = server.voice_client
        option = None

        
        if reaction.emoji == "▶️" and reaction.message.author != user:
            
            await Music.emoji_resume(self=self,ctx=self.playing_ctx)
            option = reactions.get("▶️")
            await reaction.message.remove_reaction("▶️", user)
            return

        if self.message == reaction.message and reaction.message.author != user and vc.is_playing():
                
            if reaction.emoji == "▶️":
                await Music.emoji_resume(self=self,ctx=self.playing_ctx)
                option = reactions.get("▶️")
                await reaction.message.remove_reaction("▶️", user)

            elif reaction.emoji == "⏸️":
                await Music.emoji_pause(self=self,ctx=self.playing_ctx)
                option = reactions.get("⏸️")
                await reaction.message.remove_reaction("⏸️", user)

            elif reaction.emoji == "⏭️":
                await Music.emoji_skip(self=self,ctx=self.playing_ctx)
                option = reactions.get("⏭️")
                await reaction.message.remove_reaction("⏭️", user)

            elif reaction.emoji == "🔀":
                await Music.emoji_shuffle(self=self,ctx=self.playing_ctx)
                option = reactions.get("🔀")
                await reaction.message.remove_reaction("🔀", user)

            elif reaction.emoji == "⏹️":
                await Music.emoji_stop(self=self,ctx=self.playing_ctx)
                option = reactions.get("⏹️")
                await reaction.message.remove_reaction("⏹️", user)


            elif reaction.emoji == "🔁":
                await Music.emoji_loop(self=self,ctx=self.playing_ctx)
                option = reactions.get("🔁")
                await reaction.message.remove_reaction("🔁", user)

        elif reaction.emoji in reactions.keys() and not vc.is_playing():
            await reaction.message.remove_reaction(reaction.emoji, user)
            await Music.emoji_send_msg(self=self,ctx=self.playing_ctx)



        if  reaction.emoji in reactions.keys() and reaction.message.author != user: 
            print(f"[User Reaction Emoji] Music Commands. {user} User selected value is {option}")

    async def emoji_send_msg(self,ctx):
        embed = nextcord.Embed(title="First play some music",color=0x2b2d31)
        await ctx.send(embed=embed, delete_after=10.0)


    async def emoji_shuffle(self, ctx: commands.Context):
        try:
            """Shuffles the queue."""
            if len(self.queue) == 0:
                await ctx.send(f'❗️  The queue is empty', delete_after=30.0)
                return
            else:
                random.shuffle(self.queue)
                await ctx.send(f'🔀 Shuffled', delete_after=30.0)
                # await ctx.message.add_reaction('✅')
                return 
        except:
            await ctx.send("Error Shuffle!", delete_after=30.0)
            return


    async def emoji_loop(self, ctx):
        if self.loop:
            self.loop = False
            await ctx.send(f"❗️  Loop Disabled", delete_after=30.0)
            return
        else:
            self.loop = True
            await ctx.send(f"🔁  Loop Enable", delete_after=30.0)
            return

    async def emoji_pause(self, ctx):
        try:
            ctx.voice_client.pause()
            await ctx.send(f"⏸  Paused Music", delete_after=30.0)
            return
        except:
            await ctx.send("Error Pause!", delete_after=30.0)
            return

    async def emoji_resume(self, ctx):

        server = ctx.message.guild
        vc = server.voice_client
        if vc.is_playing():
            await ctx.send(f"▶️  Already playing music", delete_after=30.0)
            return
        
        try:
            ctx.voice_client.resume()
            await ctx.send(f"▶️  I start playing again", delete_after=30.0)
            return
        except:
            await ctx.send("Error Resume!", delete_after=30.0)
            return

    async def emoji_stop(self, ctx):
        try:
            ctx.voice_client.stop()
            self.reset()
            await ctx.send(f"⏹  Stopped Music", delete_after=30.0)
            await self.timer(ctx)
            return
        except:
            await ctx.send("Error Stop!", delete_after=30.0)
            return

    async def emoji_skip(self, ctx):
        try:
            if len(self.queue) > 0:
                next_song_url = self.queue[0][0]
                ctx.voice_client.stop()
                await ctx.send(f"⏩  Skipped Song", delete_after=30.0)
                await self.real_play(ctx, ctx.voice_client, next_song_url)
                return
            else:
                ctx.voice_client.stop()
                self.reset()
                await ctx.send(f"⏭  Skipped Song: No other Songs in Queue", delete_after=30.0)
                return
        except AttributeError as e:
            await ctx.send("Error: " + str(e))
            return



    def up_index(self):
        self.indexinfoqueue+=1
        return self.indexinfoqueue

    @staticmethod
    def gImg(search):
        
        
        search = str(search)
        search = search.replace(" ","+")
        try:
            search = search.replace("(","")
            search = search.replace("/","")
            search = search.replace("","")
            search = search.replace(")","")
            search = search.replace("-","+")
            search = search.replace("++","+")
        except:
            ...
        search = search.lower()
        temp = f"song+{search}"
        search = temp


        num = 1

        logging.debug(f"[Google Img debug] : {search} | Numbers of image {num}")
        print(f"[Google Img debug] : {search} | Numbers of image {num}")
        page = 1

        get = requests.get(f"https://apiv2.spapi.ga/fun/imagesearch?search={search}&num={num}&page={page}")
        obj = json.loads(get.text)
        l = ['','','']
        for i in range(0,num):
            searched = str(obj["searched"])
            result = str(obj["result"][i]["url"])
            l[i] = result
        return random.choice(l)




    @commands.command(description="Display the music queue.")
    async def infoqueue(self, ctx: commands.Context):

        embed = nextcord.Embed(
            title=f"Queue songs: {len(self.queue)}",
            colour=0x2b2d31,
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        embed.add_field(name="I'm playing", value=self.currentsonginfo[1], inline=False)
        embed.add_field(
            name="Upcoming Songs",
            value="\n".join( (str(self.up_index()).capitalize() + "-" + "   " + t[1]) for t in self.queue ),
            inline=False
        )
        for index in range(len(self.queue)-1):
            song = self.queue[index]
            await ctx.send(str(index) + "  " + song[1])
        await ctx.send(embed=embed)


    def queue(self, ctx):
        embed = nextcord.Embed(
            title=f"Queue songs: {len(self.queue)}",
            colour=0x2b2d31,
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        embed.add_field(name="I'm playing", value=self.currentsonginfo[1], inline=False)
        embed.add_field(
            name="Upcoming Songs",
            value="\n".join( (str(self.up_index()).capitalize() + "-" + "   " + t[1]) for t in self.queue ),
            inline=False
        )
        for index in range(len(self.queue)-1):
            song = self.queue[index]
            # await ctx.send(str(index) + "  " + song[1])
        return embed


    @commands.command(description="Bot leave the voice channel.")
    async def leave(self, ctx):
        try:
            ctx.voice_client.stop()
            self.reset()
            self.is_connected = False
            await ctx.send("🕳 I'm logging out, Goodbye")
            await ctx.voice_client.disconnect()
        except:
            await ctx.send("Error Leave!")

    @commands.command(name='volume', description="Function Not Implemented yet.")
    async def volume(self, ctx, volume: int):
        # """Changes the player's volume"""
        # if 0 <= volume <= 100:
        # # if volume <= 100:
        #     current_volume = ctx.voice_client.source.volume()
        #     if volume < current_volume:
        #         ctx.voice_client.source.volume = volume / 100
        #         await ctx.send(f'**`{ctx.author}`**: He Turned The Volume Down a **{volume}%**')
        #     elif volume > current_volume:
        #         ctx.voice_client.source.volume = volume / 100
        #         await ctx.send(f'**`{ctx.author}`**: He Turned Up the Volume a **{volume}%**')
        #     else:
        #         await ctx.send("You have not changed the volume")
        # else:
        #     await ctx.send("Unsuitable Volume Value")
        await ctx.send("Function Not Implemented yet")



    @commands.command(description="Displays music panel.")
    async def panel(self, ctx: commands.Context):
        if not ctx.voice_client:
            server = ctx.message.guild
            vc = server.voice_client
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("join a voice channel first lol")
        else:
            vc = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("first play some music")
        
        em = nextcord.Embed(title="Music Panel", description="control the bot by clicking on the buttons below")
        view = ControlPanel(vc, ctx)
        await ctx.send(embed=em, view=view)



    # @commands.command()
    # async def volume(self, ctx, volume: int):
    #     # """Changes the player's volume"""
    #     if ctx.author.voice is None:
    #         await ctx.send("You are not in a voice channel.")
    #         return

    #         # current_volume = ctx.voice_client.source.volume * 100
    #     ctx.voice_client.source.volume = volume / 100
    #         # if volume < current_volume:
    #         #     await ctx.send(f'**`{ctx.author}`**: Volume turned down to **{volume}%**')
    #         # elif volume > current_volume:
    #         #     await ctx.send(f'**`{ctx.author}`**: Volume turned up to **{volume}%**')
    #         # else:
    #         #     await ctx.send("Volume remains the same")

    #     await ctx.send(f'**`{ctx.author}`**: Changed volume to **{volume}%**')





    @commands.command(name='shuffle', description="Shuffles the queue.")
    async def _shuffle(self, ctx: commands.Context):
        try:
            """Shuffles the queue."""
            if len(self.queue) == 0:
                await ctx.send('❗️The queue is empty')
            else:
                random.shuffle(self.queue)
                await ctx.send('Shuffled 🔀')
                await ctx.message.add_reaction('✅')
        except:
            await ctx.send("Error Shuffle!")

    @commands.command(name='search', description="Searches music.")
    async def _search(self, ctx: commands.Context, *, search: str):
        """Searches youtube.
        It returns an imbed of the first 10 results collected from youtube.
        Then the user can choose one of the titles by typing a number
        in chat or they can cancel by typing "cancel" in chat.
        Each title in the list can be clicked as a link.
        """
        if not self.is_connected:
            await self.join(ctx)
        if self.is_connected:
            async with ctx.typing():
                try:
                    source = await YTDLSource.search_source(ctx, self.client, search, loop=self.client.loop)
                except YTDLError as e:
                    await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
                else:
                    if source == 'sel_invalid':
                        await ctx.send('❌ Invalid input')
                    elif source == 'cancel':
                        await ctx.send('🟡️ Search cancelled')
                    elif source == 'timeout':
                        await ctx.send(':alarm_clock: **Time Expired to Choose**')
                    else:
                        song = Song(source)
                        await Music.addsong(self, ctx, song.source.url, song.source.title, song.source.duration)

    # @commands.command()
    # async def clear2(self, ctx, amount):
    #     try:
    #         await ctx.channel.purge(limit=amount, check=lambda msg: not msg.pinned)
    #         await ctx.send(f"✅ Latest {amount} Messages Deleted")
    #     except:
    #         await ctx.send("Errore")

    async def timer(self, ctx):
        time = 0
        server = ctx.message.guild
        voice_channel = server.voice_client

        while not self.playing:
            await asyncio.sleep(1)
            time = time + 1
            # if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            if voice_channel.is_playing() or voice_channel.is_paused():
                time = 0
            else:
                if time == 300:
                    await self.leave(ctx)

    def convert_duration(self, duration):
        count = duration.count(":")
        if count == 2:
            h, m, s = duration.split(":")
            return int(h) * 60 * 60 + int(m) * 60 + int(s)
        else:
            m, s = duration.split(":")
            return int(m) * 60 + int(s)

    async def addsong(self, ctx, song, title, temp_duration):
        duration = self.convert_duration(temp_duration)
        self.queue.append([song, title, duration])
        if not self.playing:
            await self.real_play(ctx, ctx.voice_client, self.queue[0][0])
            self.playing = True
        else:
            await ctx.send("Song Added to Queue")

    def reset(self):
        self.queue = []
        self.playing = False
        self.loop = False
        self.joinfromplay = False
        self.currentsonginfo = []
        self.indexinfoqueue = 0

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

class YTDLSource(nextcord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, client, source: nextcord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data
        self.client = client
        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(self, ctx: commands.Context, client, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(self.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(self.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return self(ctx, nextcord.FFmpegPCMAudio(info['url'], **self.FFMPEG_OPTIONS), data=info)

    @classmethod
    async def search_source(self, ctx: commands.Context, client, search: str, *, loop: asyncio.BaseEventLoop = None):
        channel = ctx.channel
        loop = loop or asyncio.get_event_loop()

        self.search_query = '%s%s:%s' % ('ytsearch', 10, ''.join(search))
        opts = {'extract_flat': True, 'skip_download': True}
        with youtube_dl.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(self.search_query, download=False)

        lst = []
        index = 1
        for e in info['entries']:
            # lst.append(f'`{info["entries"].index(e) + 1}.` {e.get("title")} **[{YTDLSource.parse_duration(int(e.get("duration")))}]**\n')
            VId = e.get('id')
            VUrl = 'https://www.youtube.com/watch?v=%s' % (VId)
            lst.append(f"**{str(index)}** " + "\t›\t" + f'`{e.get("title")}`')
            index += 1
        lst.append("\n**React to Choose, React ' ❌ ' to Cancel**\nNote » Wait for bot to complete the reactions | React again if not respond!")

        embed = nextcord.Embed(
            title=f'Results Found For:   **{search}**',
            description="\n".join(lst),
            type='rich',
            colour=0x2b2d31,
            timestamp=datetime.datetime.now()
        )
        embed.set_footer(text=f"requested by {ctx.author}", icon_url=ctx.author.display_avatar)
        reactions = {'1️⃣':1, '2️⃣':2, '3️⃣':3,'4️⃣':4,'5️⃣':5,'6️⃣':6,'7️⃣':7,'8️⃣':8,'9️⃣':9,'🔟':10,'❌':'cancel'}
        message = await ctx.send(embed=embed, delete_after=45.0)
        for i in reactions:
            await message.add_reaction(str(i))


        # def check(msg):
        #     return msg.content.isdigit() == True and msg.channel == channel or msg.content == 'cancel' or msg.content == 'cancel'

        def check(reaction, user):
            
            return user != client.user and user == ctx.author and (str(reaction.emoji) == '1️⃣' or '2️⃣' or '3️⃣'or '4️⃣'or '5️⃣' or '6️⃣'or '7️⃣'or '8️⃣'or '9️⃣'or '🔟'or '❌') 

        try:
            # m = await client.wait_for('message', check=check, timeout=45.0)
            m = None
            reaction, user = await client.wait_for('reaction_add', timeout=45.0, check=check)


            if str(reaction.emoji) == "1️⃣":
                m = reactions.get("1️⃣")

            elif str(reaction.emoji) == "2️⃣":
                m = reactions.get("2️⃣")

            elif str(reaction.emoji) == "3️⃣":
                m = reactions.get("3️⃣")

            elif str(reaction.emoji) == "4️⃣":
                m = reactions.get("4️⃣")

            elif str(reaction.emoji) == "5️⃣":
                m = reactions.get("5️⃣")

            elif str(reaction.emoji) == "6️⃣":
                m = reactions.get("6️⃣")

            elif str(reaction.emoji) == "7️⃣":
                m = reactions.get("7️⃣")

            elif str(reaction.emoji) == "8️⃣":
                m = reactions.get("8️⃣")

            elif str(reaction.emoji) == "9️⃣":
                m = reactions.get("9️⃣")

            elif str(reaction.emoji) == "🔟":
                m = reactions.get("🔟")
            
            elif str(reaction.emoji) == "❌":
                m = reactions.get("❌")
            

            print(f"[User Reaction Emoji] value is {m}")

        except asyncio.TimeoutError:
            rtrn = 'timeout'

        else:
            if isinstance(m, int):
                music_url = None
                await reaction.message.remove_reaction(reaction.emoji, user)
                sel = int(m)
                if 0 < sel <= 10:
                    for key, value in info.items():
                        if key == 'entries':
                            """data = value[sel - 1]"""
                            VId = list(value)[sel - 1]['id']
                            VUrl = 'https://www.youtube.com/watch?v=%s' % (VId)
                            # music_url = str(VUrl)
                            # Music.getUrl(music_url)
                            partial = functools.partial(self.ytdl.extract_info, VUrl, download=False)
                            data = await loop.run_in_executor(None, partial)
                    rtrn = self(ctx, client, nextcord.FFmpegPCMAudio(data['url'], **self.FFMPEG_OPTIONS), data=data)
                else:
                    rtrn = 'sel_invalid'
            elif m == 'cancel':
                rtrn = 'cancel'
            else:
                rtrn = 'sel_invalid'

        return rtrn

    @staticmethod
    def parse_duration(duration: int):
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            if days > 0:
                duration.append('{}'.format(days))
            if hours > 0:
                duration.append('{}'.format(hours))
            if minutes > 0:
                duration.append('{}'.format(minutes))
            if seconds > 0:
                duration.append('{}'.format(seconds))

            value = ':'.join(duration)

        elif duration == 0:
            value = "LIVE"

        return value

class Song():
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        # embed = nextcord.Embed(title='Now playing', description=f'```css\n{self.source.title}\n```',color=0x2b2d31)
        # embed.add_field(name='Duration', value=self.source.duration)
        # embed.add_field(name='Requested by', value=self.requester.mention)
        # embed.add_field(name='Uploader', value=f'[{self.source.uploader}]({self.source.uploader_url})')
        # embed.add_field(name='URL', value=f'[Click]({self.source.url})')
        # embed.set_thumbnail(url=self.source.thumbnail)
        # embed.set_author(name=self.requester.name, icon_url=self.requester.display_avatar)


        ...
    




class ControlPanel(nextcord.ui.View,Music):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx
    
    @nextcord.ui.button(label="Resume/Pause", style=nextcord.ButtonStyle.blurple)
    async def resume_and_pause(self, button: nextcord.ui.Button, ctx):
    
        if not ctx.user == self.ctx.author:
            return await ctx.send("You can't do that. run the command yourself to use these buttons")
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused():
            await self.vc.resume()
            await ctx.message.edit(content="Resumed", view=self)
        else:
            await self.vc.pause()
            await ctx.message.edit(content="Paused", view=self)

    # @nextcord.ui.button(label="Queue", style=nextcord.ButtonStyle.blurple)
    # async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    #     if not interaction.user == self.ctx.author:
    #         return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
    #     # for child in self.children:
    #     #     child.disabled = False
    #     # button.disabled = True
    #     # if self.vc.queue.is_empty:
    #     #     return await interaction.response.send_message("the queue is empty smh", ephemeral=True)
    
    #     # em = nextcord.Embed(title="Queue")
    #     # queue = self.vc.queue.copy()
    #     # songCount = 0

    #     # for song in queue:
    #     #     songCount += 1
    #     #     em.add_field(name=f"Song Num {str(songCount)}", value=f"`{song}`")
    #     # await interaction.message.edit(embed=em, view=self)
    #     e = Music.queue(self.ctx)
    #     await interaction.send(embed = e, delete_after= 25.0)
    
    # @nextcord.ui.button(label="Skip/Stop", style=nextcord.ButtonStyle.blurple)
    # async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    #     if not interaction.user == self.ctx.author:
    #         return await interaction.response.send_message("You can't do that. run the command yourself to use these buttons", ephemeral=True)
    #     for child in self.children:
    #         child.disabled = False
    #     button.disabled = True
    #     if self.vc.queue.is_empty:
    #         return await interaction.response.send_message("the queue is empty smh", ephemeral=True)

    #     try:
    #         next_song = self.vc.queue.get()
    #         await self.vc.play(next_song)
    #         await interaction.message.edit(content=f"Now Playing `{next_song}`", view=self)
    #     except Exception:
    #         return await interaction.response.send_message("The queue is empty!", ephemeral=True)
    
    @nextcord.ui.button(label="Disconnect", style=nextcord.ButtonStyle.red)
    async def disconnect(self, button: nextcord.ui.Button, ctx):
        if not ctx.user == self.ctx.author:
            return await ctx.send("You can't do that. run the command yourself to use these buttons")
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        await ctx.message.edit(content="Disconnect :P", view=self)


























def setup(client):
    client.add_cog(Music(client))