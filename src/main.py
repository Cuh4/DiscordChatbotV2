# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import config
import chatbot
import learn
import slashCommands

from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Variables
# // Chatbot
chatbot = chatbot.bot("Bob")
chatbot.knowledge.addTag("AUTHOR", "Cuh4")
chatbot.knowledge.addTag("GENDER", "Male")

learn.learn(chatbot) # teach everything necessary i guess

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
# // Register commands
slashCommands.learn(tree, chatbot)

# // Bot start
@client.event
async def on_ready():    
    # notify
    helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(client.user)} has started.")
    
    # sync
    await tree.sync()

# // Message send
@client.event
async def on_message(message: discord.Message):
    global processingResponse
    
    # Ignore messages sent by bots
    if message.author.bot:
        return

    # ignore self
    if message.author == client.user:
        return
    
    # Ignore message if not mentioned
    if not discordHelpers.utils.isMentioned(message.mentions, client.user):
        return
    
    # Ignore message if user is on cooldown
    if discordHelpers.cooldown.cooldown(message.author, config.chatCooldown, "chat"):
        return await message.add_reaction("🕰")
    
    # remove mentions from message content
    content = message.content

    for user in message.mentions:
        content = content.replace(f"<@{user.id}>", "")
    
    # Send loading message
    sentMessage = await message.channel.send(
        embed = discord.Embed(
            description = config.loadingEmoji,
            color = discord.Colour.from_rgb(225, 225, 255)
        ),
        
        reference = message,
        mention_author = True
    )

    helpers.prettyprint.info(f"🧑| Received a message from {discordHelpers.utils.formattedName(message.author)}: {content}")

    # Get chatbot response
    helpers.prettyprint.info(f"💻| Retrieving response.")
    response, success, reason = chatbot.respond(content)

    # Reply with response
    if success:
        # successful
        helpers.prettyprint.success(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)}: {response}")

        # reply with chatbot response
        return await sentMessage.edit( # using return statement to prevent running timeout code below
            embed = discord.Embed(
                description = f"> :robot: :white_check_mark: | **{response}**",
                color = discord.Colour.from_rgb(125, 255, 125)
            )
        )
    else:
        # unsuccessful (timed out or couldn't find appropriate respond)
        helpers.prettyprint.error(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)} timed out/couldn't find an appropriate response.")
        
        # notify cuh4 to add more training data
        logChannel = client.get_channel(1167331643363696640) #testing @ https://discord.gg/CymKaDE2pj

        await logChannel.send( # only so i can train the chatbot
            embed = discordHelpers.embeds.warning(f"Failed to respond to:\n```{content.replace('`', '')}```")
        )
        
        # reply with error message
        errorMsg = {
            "profanity" : "Your message was deemed NSFW and has therefore been ignored.",
            "unknown_query" : "Sorry! I couldn't come up with a response.",
            "no_answer" : "Sorry, I couldn't think of a response."
        }[reason]
    
        return await sentMessage.edit(
            embed = discord.Embed(
                description = f"> :robot: :x: | **{errorMsg}**",
                color = discord.Colour.from_rgb(255, 125, 125)
            )
        )
    
# // Start the bot
client.run(config.botToken)