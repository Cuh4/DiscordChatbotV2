# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import asyncio

import config
from modules import pychatbot
import learn
import slashCommands
import events
from modules import general as helpers

# // ---- Variables
# // Chatbot
# create chatbot
chatbot = pychatbot.chatbot(
    name = "Greggory",
    confidence = 0.53,
    allowProfanity = True # we'll just censor the profanity instead
)

# quick print
helpers.prettyprint.success(f"Created chatbot named {chatbot.name}. Database path: {chatbot.knowledgeBase.fullPath}")

# knowledge
learn.learnDefaults(chatbot) # teach everything necessary i guess

# // Discord
# intents
intents = discord.Intents.default()
intents.message_content = True

# client
client = discord.Client(
    intents = intents,
    
    status = discord.Status.do_not_disturb,
    activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = config.activityText
    )
)

tree = discord.app_commands.CommandTree(client)

# // ---- Setup
# // Setup Function
async def setup():
    # // Register Globals
    helpers.globals.save("client", client)
    helpers.globals.save("chatbot", chatbot)
    helpers.globals.save("commandTree", tree)

    # // Register Commands
    slashCommands.start()
    
    # // Register Events
    await events.setup(client)
    
# // Start Setup
asyncio.run(setup())

# // Start Bot
client.run(config.botToken, log_handler = None)