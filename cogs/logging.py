import nextcord
from nextcord.ext import commands
import asyncio
from cogs.utils import settings
from cogs.utils import permissions
import datetime

class Logging(commands.Cog):
    def __init__(self, loggy):
        self.loggy = loggy
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # When a user is removed from the server.
        log_message = u"{} Left the server!".format(member.name)
        channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(member.guild.id)["log-channels"]["general"]))
        await channel.send(log_message)
        settings.log(member.guild.id, "general", log_message)

    @commands.Cog.listener()    
    async def on_member_join(self, member):
        # When a user is registered with a server
        log_message = u"{} Joined the server!".format(member.name)
        # welcome_str = settings.get_settings(member.guild.id).get("welcome-messge", u"Welcome to {} {}!")
        # await channel.send(member, welcome_str.format(member.guild.name,member.name))
        channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(member.guild.id)["log-channels"]["general"]))
        await channel.send(log_message)
        settings.log(member.guild.id, "general", log_message)
    
    @commands.Cog.listener()
    async def on_member_ban(self, member):
        log_message = u"{} Was banned from {}!".format(member.name,member.server)
        channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(member.guild.id)["log-channels"]["general"]))
        await channel.send(log_message)
        settings.log(member.guild.id, "audit", log_message)
    
    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     # Triggered on channel change and mute/deafen
    #     if before.bot:
    #         return
    #     if(before.voice_channel == after.voice_channel):
    #         return
    #     elif(after.voice_channel is None):
    #         message = u'{0} Disconnected from {1}'
    #         channel = before.voice_channel
    #         settings.log(before.guild.id, "general", u'{0} Disconnected from {1}'.format(before.name,channel.name))
    #     else:
    #         message = u'{0} Moved to {1}'
    #         channel = after.voice_channel
    #         settings.log(before.guild.id, "general", message.format(before.name,channel.name))
        
    #     _channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"]))
    #     await _channel.send(message.format(before.name,channel.name))
   
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.bot:
            return
        # Nickname Changes
        if before.nick != after.nick:
            if after.nick is None:
                message = "{0} Reset their nickname"
                channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"]))
                await channel.send(message.format(before.name))
                settings.log(before.guild.id, "general", u"{0} reset their nickname".format(before.name)) 
            else:
                message = "{0} Changed their nickname to {1}"
                channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"]))
                await channel.send(message.format(before.name, after.nick))
                settings.log(before.guild.id, "general", u"{0} changed their nickname to {1}".format(before.name,after.nick))
        # Status Changes
        """ This is pretty spammy so it can be enabled and disabled in the settings or with the logs_toggle command """
        if settings.get_settings(before.guild.id)["enabled_logs"]["status"] == "on":
            if before.status != after.status:
                message = "{0}'s status changed to {1}"
                channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["status"]))
                await channel.send(message.format(before.name, after.status))
        if settings.get_settings(before.guild.id)["enabled_logs"]["games"] == "on":
            if before.game != after.game:
                if after.game is None:
                    message = "{0} Has stopped playing {1}"
                    channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["games"]))
                    await channel.send(message.format(before.name, before.game))
                else:
                    message = "{0} Is now playing {1}"
                    channel: commands.Context = self.loggy.get_channel(int(self.loggy.get_channel(settings.get_settings(before.guild.id)["log-channels"]["games"])))
                    await channel.send(message.format(before.name, after.game))


    @commands.Cog.listener()                                
    async def on_channel_create(self, channel):
        log_message = "Channel '{}' was created with topic '{}'".format(channel.name, channel.topic)
        _channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(channel.guild.id)["log-channels"]["general"]))
        await _channel.send(log_message)
        settings.log(channel.guild.id, "audit", log_message)

    @commands.Cog.listener()    
    async def on_channel_delete(self, channel):
        log_message = "Channel '{}' was deleted".format(channel.name)
        _channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(channel.guild.id)["log-channels"]["general"]))
        await _channel.send(log_message)
        settings.log(channel.guild.id, "audit", log_message)

    @commands.Cog.listener()    
    async def on_channel_update(self, before, after):
        if before.name != after.name:
            log_message = "Channel '{}' was renamed to '{}'"
            channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"]))
            await channel.send(log_message.format(before.name, after.mention))
            settings.log(before.guild.id, "audit", log_message.format(before.name, after.name))
        if before.topic != after.topic:
            log_message = "The topic for channel '{}' was changed to '{}'"
            channel: commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"])) 
            await channel.send(log_message.format(before.mention, after.topic))
            settings.log(before.guild.id, "audit", log_message.format(before.name, after.topic))

    @commands.Cog.listener()        
    async def on_message_edit(self, before, after):
        if before.pinned == False and after.pinned == True:
            log_message = "The follwing message was pinned: \n `{}`".format(after.content)
            channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"])) 
            await channel.send(log_message)
            settings.log(before.guild.id, "audit", log_message)
            
        if before.pinned == True and after.pinned == False:
            log_message = "The follwing message was unpinned: \n `{}`".format(after.content)
            channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"])) 
            await channel.send(log_message)
            settings.log(before.guild.id, "audit", log_message)
            
        if before.content != after.content:
            if before.pinned == True and after.pinned == True:
                log_message = "The following **pinned** message belonging to {} was edited: \n Original: \n `{}` \n Modified: \n `{}` \n".format(before.author.name, before.content, after.content)
                channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"])) 
                await channel.send(log_message)
                settings.log(before.guild.id, "audit", log_message)

        embed=nextcord.Embed(title=f"{before.author.name} has edited the message",description=f"{before.author.mention}",timestamp= datetime.datetime.now(),colour=0x42f5c5)
        embed.set_thumbnail(url=f"{after.author.display_avatar}")
        embed.add_field(name="📄  Original Message", value=f"`{before.content}`", inline=False)
        embed.add_field(name="📝  Edited Message", value=f"`{after.content}`", inline=False)
        embed.set_footer(text=f"User ID: {before.author.id}")
        channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(before.guild.id)["log-channels"]["general"])) 
        await channel.send(embed=embed)       
    
    @commands.Cog.listener()    
    async def on_message_delete(self, message):
        if message.author.bot:  
            return
        log_message = "The Following Message belonging to {} was deleted: \n `{}`".format(message.author.name, message.content)
        embed=nextcord.Embed(title=f"{message.author.name} has deleted a message 🗑️", description=f"{message.author.mention} Deleted message:\n `{message.content}`",timestamp= datetime.datetime.now(),colour=0x42f5c5)
        embed.set_thumbnail(url=f"{message.author.display_avatar}")
        embed.set_author(name=f"{message.author.name}#{message.author.discriminator}",icon_url=f"{message.author.display_avatar}")
        embed.set_footer(text=f"User ID: {message.author.id}")
        channel : commands.Context = self.loggy.get_channel(int(settings.get_settings(message.guild.id)["log-channels"]["general"]))
        await channel.send(embed=embed)  
        settings.log(message.guild.id, "audit", log_message)     
            
def setup(loggy):
    loggy.add_cog(Logging(loggy))
    