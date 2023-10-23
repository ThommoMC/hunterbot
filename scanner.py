import requests
import discord
from discord.ext import commands
import math
import config

class Logic():
    
    API = "https://emc-toolkit.vercel.app/api/"
    EarthMC_API = "https://api.earthmc.net/v2/"

    def loadHunters():
        usernames = config.Storage.load_json("usernames.json")
        return usernames["hunters"]

    def onlinePlayers(getHunters = False):
        hunters = Logic.loadHunters()
        if getHunters == False:
            return requests.get(Logic.API + "aurora/onlineplayers").json()
        elif getHunters == True:
            online = requests.get(Logic.API + "aurora/onlineplayers").json()
            return [item for item in online if item["name"].lower() in [hunter.lower() for hunter in hunters]]
    
    def lookup(type, name):
        if type == "nation":
            if name == "bulk":
                return requests.get(Logic.EarthMC_API + f"aurora/nations/").json()
            return requests.get(Logic.EarthMC_API + f"aurora/nations/{name}/").json()
        elif type == "town":
            return requests.get(Logic.EarthMC_API + f"aurora/towns/{name}/").json()


class ScanCommand(commands.Cog):
    def __init__(self, bot: discord.Bot()):
        self.bot = bot

    hunters = discord.commands.SlashCommandGroup("hunters", "Hunter commands")

    @hunters.command(guild=1158643397574279168, description="Add a hunter")
    async def report(self, ctx: discord.ApplicationContext, hunter: discord.SlashCommandOptionType.string):
        user = self.bot.get_user(1122051453431840818)
        embed = discord.Embed(title="Add Hunter?", color=discord.Colour.blurple(), description=f"Should player {hunter} be added to the hunter list?")
        await user.send(embed=embed)

    @hunters.command(description="Scan nearby players")
    async def nearby(self, ctx: discord.ApplicationContext, town: discord.SlashCommandOptionType.string):
        onlineHunters = Logic.onlinePlayers(getHunters=True)
        town = Logic.lookup("town", town)
        location = town["coordinates"]["spawn"]
        foundHunters = []
        print(location)
        for hunter in onlineHunters:
            print(hunter)
            if math.isclose(location["x"], hunter["x"], abs_tol=500) or math.isclose(location["z"], hunter["z"], abs_tol=500):
                foundHunters.append(hunter)
                await ctx.respond(f"Hunter Spotted {hunter}")
        if foundHunters == []:
            await ctx.respond("No Hunters Found!")
    
    @hunters.command(description="Lists hunters")
    async def list(self, ctx: discord.ApplicationContext):
        usernames = config.Storage.load_json("usernames.json")
        embed = discord.Embed(
            title="Known Hunters",
            description="List of all known hunters",
            color=discord.Color.blurple()
        )
        for hunter in usernames['hunters']:
            embed.add_field(name = "Hunter", value = hunter)
        await ctx.respond(embed=embed)
    
    @hunters.command(description="Lists online hunters")
    async def online(self, ctx: discord.ApplicationContext):
        onlineHunters = Logic.onlinePlayers(True)
        embed = discord.Embed(
            title="Online Hunters",
            description="All online hunters",
            color=discord.Color.blurple()
        )
        for hunter in onlineHunters:
            embed.add_field(name=hunter['name'], value=f"X: {hunter['x']}, Y: {hunter['y']}, Z: {hunter['z']}")
        await ctx.respond(embed=embed)

def setup(bot):
        bot.add_cog(ScanCommand(bot))