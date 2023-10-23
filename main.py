import discord
import requests
import config
import scanner
import math
from discord.ext import tasks
import playerMan

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    hunterProtection.start()

@bot.command(description="Links your Minecraft Account to the Hunter Bot!")
async def link(ctx: discord.ApplicationContext, username: str):
    playerMan.linkDiscord(username, ctx.author.id)
    await ctx.respond("Added/Updated Username!")


@tasks.loop(seconds=10)
async def hunterProtection():
    onlineHunters = scanner.Logic.onlinePlayers(getHunters=True)
    onlinePlayers = scanner.Logic.onlinePlayers()
    nation = scanner.Logic.lookup("nation", "Laurentia")
    allnations = scanner.Logic.lookup("nation", "bulk")
    residents = []
    for resident in nation['residents']:
        for player in onlinePlayers:
            if resident == player['name']:
                residents.append(resident)
    channel = bot.get_channel(1138306306474782791)
    for hunter in onlineHunters:
        for player in onlinePlayers:
            for resident in residents:
                if player["name"] == resident:
                    point1 = (player['x'], player['y'], player['z'])
                    point2 = (hunter['x'], hunter['y'], hunter['z'])
                    distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)
                    if (distance <= 500 and player["underground"] == False):
                        print(resident)
                        print(distance)
                        message_contents = ""
                        discordID = playerMan.getDiscord(resident)
                        if discordID != []:
                            message_contents = f"<@{discordID[0]}>"
                        embed = discord.Embed(  
                            title = "__**HUNTER SPOTTED**__",
                            description = "**REMAIN AWARE OF YOUR SURROUNDINGS**",
                            color = discord.Color.red())
                        embed.add_field(name="Name", value=hunter['nickname'])
                        embed.add_field(name="Location", value=f"X: {hunter['x']}, Y: {hunter['y']}, Z: {hunter['z']}")
                        embed.add_field(name="Distance (Beta)", value=distance)
                        await channel.send(message_contents, embed=embed, delete_after=10) 


#bot.load_extension('config')
bot.load_extension('scanner')
bot.run("MTE1ODY0Mjk5OTA2MDg2NTAyNg.GYnVYf.5JV-pNtnIaLywmCDLGKQwtq8OJ3cE6lXaL2Ltg")