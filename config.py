import json
import discord
from discord.ext import commands

class Storage:
    def load_json(json_file):
        with open(json_file) as f:
            data = json.load(f)
        return data
    
    def write_json(json_file, data):
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
    
    def add_hunter(hunter):
        data = Storage.load_json("usernames.json")
        hunters = data.setdefault("hunters", [])
        if isinstance(hunters, str):
            hunters = [hunters]  # Convert to list if it's a string
        if hunter not in hunters:
            hunters.append(hunter)    
            data["hunters"] = hunters
            Storage.write_json("usernames.json", data)
            return True
        else: return False
    
    def get_server_details(server_id):
        data = load_json("config.json")
        


#class Commands(commands.Cog):
#    def __init__(self, bot):
#        self.bot = bot
#    
#    config = discord.commands.SlashCommandGroup("config", "Bot configuration commands")
#    @add_hunter.error
#    async def add_hunter_error(self, ctx, error):
##        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
 #           await ctx.respond("Looks like you don't have enough permissions to use this command!")
    
#def setup(bot):
#        bot.add_cog(Commands(bot))