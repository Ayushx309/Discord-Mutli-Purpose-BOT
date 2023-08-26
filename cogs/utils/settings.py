import nextcord
from nextcord.ext import commands
import asyncio
import codecs
import datetime
import json
from time import sleep
import os
from global_functions import PREFIX

async def check_servers(loggy):
    print("\033[1;36;48m Checking Servers... \n")
    for server in loggy.guilds:
        if get_settings(server.id):
            print("\033[1;36;48m Connected to {} : {}".format(server.id, server.name))
            sleep(1) 
        else:
            print("\033[1;33;48m New Server {} : {}".format(server.id, server.name))
            sleep(1)
            print("\033[1;35;48m Creating defaults for {} ...".format(server.name))
            new = {}
            new["log-channels"] = {"games": "", "general": "", "status": ""}
            new["enabled_logs"] = {"status": "off","games": "off"}
            new["admins"] = {}
            new["welcome-message"] = ""
            save_all_settings(server.id, new)
            
        if get_settings(server.id)["log-channels"]["general"] == "":
            channel = server.system_channel
            #await  channel.send(f"**TESTING Ignore!**\n No General logs channel! Logging functions will not work! \n"
            #                                            f"Please set the general logs channel using `{PREFIX}logchannel general (ID)`")
    print("\033[1;32;48m\nDone!\n")
            
    
def get_cogs():
    try:
        with open("log-bot.loaded_cogs", encoding='utf-8', mode="r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False
    except json.decoder.JSONDecodeError:
        return False
    finally:
        return data

def save_cogs(cogs):
    with open("log-bot.loaded_cogs","w") as cog_file:
        json.dump(cogs, cog_file)
        cog_file.close()
        print(" Cog file updated.")
        

def get_settings(server_id):
    try:
        os.makedirs(os.path.dirname("settings/{}.settings".format(server_id)), exist_ok=True)
        with open("settings/{}.settings".format(server_id), encoding='utf-8', mode="r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False
    except json.decoder.JSONDecodeError:
        return False
    return data
        
    
def save_all_settings(server_id, settings):
    os.makedirs(os.path.dirname("settings/{}.settings".format(server_id)), exist_ok=True)
    with open("settings/{}.settings".format(server_id) ,"w+") as save_state:
        json.dump(settings, save_state)
        save_state.close()
        complete = "Settings were successfully saved!"
    return complete
    
def save_setting(server, dkey, key, value):
    update = get_settings(server)
    if dkey == None:
        update[key] = value
    else:
        if value == update[dkey][key]:
            return
        else:
            update[dkey][key] = value
    save_all_settings(server, update)
    
def remove_setting(server, dkey, key):
    update = get_settings(server)
    if dkey == None:
        try:
            del update[key]
        except KeyError:
            pass
    else:
        try:
            del update[dkey][key]
        except KeyError:
            pass
    save_all_settings(server, update)
    
def log(server, log_file, log_message):
    log_message += " -- {}".format(datetime.datetime.now())
    os.makedirs(os.path.dirname("logs/{}/{}.log".format(server, log_file)), exist_ok=True)
    with codecs.open("logs/{}/{}.log".format(server, log_file), "a", encoding="UTF-8") as logf:
        logf.write(log_message)
        logf.write("\n")
        logf.close() 
        