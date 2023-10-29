# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Discord Embeds
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import config

# // ---- Functions
def __setup(emoji: str, msg: str):
    return f">>> {emoji} | {msg}"

def success(msg: str):
    embed = discord.Embed(
        description = __setup(":white_check_mark:", msg), 
        color = discord.Colour.from_rgb(0, 255, 0)
    )

    return embed

def failure(msg: str):
    embed = discord.Embed(
        description = __setup(":x:", msg), 
        color = discord.Colour.from_rgb(255, 0, 0)
    )

    return embed

def warning(msg: str):
    embed = discord.Embed(
        description = __setup(":warning:", msg), 
        color = discord.Colour.from_rgb(255, 125, 0)
    )

    return embed

def load(msg: str):
    embed = discord.Embed(
        description = __setup(config.loadingEmoji, msg), 
        color = discord.Colour.from_rgb(255, 255, 255)
    )

    return embed