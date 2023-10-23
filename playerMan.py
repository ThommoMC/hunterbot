import config
import requests
import scanner 

def linkDiscord(username, discordID):
    usernames = config.Storage.load_json("usernames.json")
    discord = usernames.setdefault("discord", {})
    discord[str(discordID)] = username
    config.Storage.write_json("usernames.json", usernames)

def getDiscord(username):
    usernames = config.Storage.load_json("usernames.json")
    discord_ids = []
    for key, name in usernames["discord"].items():
        if name.lower() == username.lower():
            discord_ids.append(key)
    return discord_ids
