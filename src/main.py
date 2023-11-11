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
bot = chatbot.bot(
    name = "Bob",
    confidence = 0.53,
    allowProfanity = True # we'll just censor the profanity instead
)

bot.knowledge.addTag("AUTHOR", "Cuh4")
bot.knowledge.addTag("GENDER", "Male")

learn.learn(learn.get(), bot) # teach everything necessary i guess

# // Discord Bot
intents = discord.Intents.default()
intents.message_content = True

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
# // Register Commands
teachCMD = slashCommands.teach.command(client, tree, bot)
slashCommands.restart.command(client, tree)
slashCommands.unlearn.command(client, tree, bot)

# // Discord Events
# on ready
@client.event
async def on_ready():
    events.on_ready.asyncFire({
        "client" : client,
        "tree" : tree
    })

# on message
@client.event
async def on_message(message: discord.Message):
    # fire event
    events.on_message.asyncFire({
        "client" : client,
        "message" : message,
        "bot" : bot,
    })
    
# // Start Bot
client.run(config.botToken, log_handler = None)