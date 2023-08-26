import nextcord
from nextcord.ext import commands
from cogs.utils import settings
from global_functions import PREFIX

def is_setup():
    def predicate(ctx):
        server = ctx.message.guild
        if settings.get_settings(server.id)["log-channels"]["general"] == "":
            raise commands.CheckFailure("Cannot Process Actions; General Logs Channel not set!")
        else:
            return True
    return commands.check(predicate)
     
def are_you_my_mummy():
    def predicate(ctx):
        return ctx.message.author.id == "410321996463996930"
    
    return commands.check(predicate)

def has_permission():
    def predicate(ctx):
        server = ctx.message.guild
        server_settings = settings.get_settings(server.id)
        # The server owner + STiGYFishh will always have permissions.
        if ctx.message.author.id == server.owner.id or ctx.message.author.id == "410321996463996930":
            return True
        else:
            return ctx.message.author.id in server_settings["admins"].values()
    
    return commands.check(predicate)