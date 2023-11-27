# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Discord Cooldown Module
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import asyncio
# // ---- Variables
cooldowns = {}

# // ---- Functions
def __key(user: discord.User, key: str):
    return str(user.id) + key

def __hasCooldown(fullKey: str):
    return cooldowns.get(fullKey, None) != None

async def __handler(fullKey: str, duration: float|int):
    await asyncio.sleep(duration)
    cooldowns.pop(fullKey)

def cooldown(user: discord.User, time: float|int, key: str) -> bool:
    # get the full key
    fullKey = __key(user, key)

    # check if a cooldown with the same key already exists
    if __hasCooldown(fullKey):
       return True
   
   # create cooldown
    cooldowns[fullKey] = True

    # remove it after some time
    asyncio.get_event_loop().run_until_complete(__handler(fullKey, time))

    # return
    return False 