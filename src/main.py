# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
import chatbot
import learn
import slashCommands
from events import events
from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Variables
# // Chatbot
# bot
bot = chatbot.bot(
    name = "Bob",
    confidence = 0.53,
    allowProfanity = True # we'll just censor the profanity instead
)

# tags
bot.knowledge.addTag("AUTHOR", "Cuh4")
bot.knowledge.addTag("GENDER", "Male")

# knowledge
learn.learn(learn.get(), bot) # teach everything necessary i guess

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
helpers.globals.save("chatbot", bot)
helpers.globals.save("commandTree", tree)

# // Register Commands
slashCommands.start()

# // Discord Events
# on ready
@client.event
async def on_ready():
    await events.on_ready.asyncFire({
        "tree" : tree
    })

# on message
@client.event
async def on_message(message: discord.Message):
    # fire event
    await events.on_message.asyncFire({
        "message" : message,
        "bot" : bot,
    })
    
# // Start Bot
client.run(config.botToken, log_handler = None)