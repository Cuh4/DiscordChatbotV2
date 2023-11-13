# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
import pychatbot
import learn
import slashCommands
from events import events
from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Variables
# // Chatbot
# create chatbot
chatbot = pychatbot.chatbot(
    name = "Bob",
    confidence = 0.53,
    allowProfanity = True # we'll just censor the profanity instead
)

# knowledge
learn.learn(learn.getDefaults(), chatbot) # teach everything necessary i guess

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

# // ---- Main
# // Register Globals
helpers.globals.save("client", client)
helpers.globals.save("chatbot", chatbot)
helpers.globals.save("commandTree", tree)

# // Register Commands
slashCommands.start()

# // Discord Events
# On Ready
@client.event
async def on_ready():
    await events.on_ready.asyncFire({})

# On Message
@client.event
async def on_message(message: discord.Message):
    # fire event
    await events.on_message.asyncFire({
        "message" : message
    })
    
# // Start Bot
client.run(config.botToken, log_handler = None)