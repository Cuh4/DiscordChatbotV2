# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Main
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

import config
import chatbot
import learn
import slashCommands
import ui

from helpers import discord as discordHelpers
from helpers import general as helpers

# // ---- Variables
# // Chatbot
bot = chatbot.bot(
    name = "Bob",
    confidence = 0.53
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

# // ---- Events
# report response event - called when a user clicks "report response" button
report_response = helpers.events.event("report_response").save()

@report_response.attach
async def callback(user: discord.User, response: chatbot.response):
    # quick check
    if not response.success:
        return
    
    # get channel
    channel = client.get_channel(config.responseReportsChannelID)
    
    # strip text of " ` " to prevent messing up the code block format
    query = response.query.replace("`", "'")
    responseText = response.text.replace("`", "'")
    source = response.source.replace("`", "'")

    # send message
    await channel.send(
        embed = discordHelpers.embeds.warning(f"**A response was reported by @{discordHelpers.utils.formattedName(user)}.**\n`Query:` ```{query}```\n`Response:` ```{responseText}```\n`Source:` ```{source}```")
    )

# // ---- Main
# // Register commands
teachCMD = slashCommands.teach.command(client, tree, bot)
slashCommands.restart.command(client, tree)

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
    
    # // basic checks
    # ignore messages sent by bots
    if message.author.bot:
        return

    # ignore self
    if message.author == client.user:
        return
    
    # ignore message if not mentioned
    if not discordHelpers.utils.isMentioned(message.mentions, client.user):
        return
    
    # ignore message if user is on cooldown
    if discordHelpers.cooldown.cooldown(message.author, config.chatCooldown, "chat"):
        return await message.add_reaction("🕰")
    
    # // filtering
    # remove mentions from message content
    content = message.content

    for user in message.mentions:
        content = content.replace(f"<@{user.id}>", "")
    
    # // waiting
    # send loading message
    botMessage = await message.channel.send(
        embed = discord.Embed(
            description = config.loadingEmoji,
            color = discord.Colour.from_rgb(225, 225, 255)
        ),
        
        reference = message,
        mention_author = True
    )

    helpers.prettyprint.info(f"🧑| Received a message from {discordHelpers.utils.formattedName(message.author)}: {content}")
    
    # // more checks
    messageBlocked = False
    messageBlockReason = ""
    
    # check for profanity
    if chatbot.isTextProfane(content) and not config.allowProfanity:
        messageBlocked, messageBlockReason = True, "contains_profanity"
    
    # check message length
    if len(content) > config.maxQueryLength:
        messageBlocked, messageBlockReason = True, "character_limit"
        
    # // failure message if checks failed
    if messageBlocked:
        failureMessage = {
            "contains_profanity" : "Your message contains profanity and was therefore ignored.",
            "character_limit" : "Your message goes over the character limit."
        }[messageBlockReason]
        
        helpers.prettyprint.warn(f"A message from {discordHelpers.utils.formattedName(message.author)} was ignored due to: {messageBlockReason}")
        
        return await botMessage.edit(
            embed = discord.Embed(
                description = f"> :robot: :x: | **{failureMessage}**",
                color = discord.Colour.from_rgb(255, 125, 125)
            )
        ) 

    # // chatbot response
    # get chatbot response
    helpers.prettyprint.info(f"💻| Retrieving response.")
    response = bot.respond(content)

    # reply with response
    if response.success:
        # response length check check
        if len(response.text) > config.maxResponseLength:
            response.text = "Whoops! My original response was too long."
            
        # profanity check
        if chatbot.isTextProfane(response.text) and not config.allowProfanity:
            response.text = "Oops! My original response was inappropriate."
            
        # get rid of markdown
        response.query = discordHelpers.utils.stripMarkdown(response.query)
        response.text = discordHelpers.utils.stripMarkdown(response.text)

        # successful
        helpers.prettyprint.success(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)}: {response.text}")

        # setup response embed
        responseEmbed = discord.Embed(
            description = f"> :robot: :white_check_mark: | **{response.text}**",
            color = discord.Colour.from_rgb(125, 255, 125)
        )
        
        if response.source != "Built-In":
            responseEmbed.set_footer(text = f"Response produced by {response.source} | Response may be inaccurate.", icon_url = message.author.display_avatar.url)

        # reply with response
        feedbackView = ui.views.wrap(
            message,
            ui.views.feedback(bot, response)
        )

        await botMessage.edit(
            embed = responseEmbed,
            view = feedbackView
        )
    else:
        # unsuccessful (timed out or couldn't find appropriate respond)
        helpers.prettyprint.warn(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)} failed. Reason: {response.failureReason}")
        
        # notify cuh4 to add more training data
        logChannel = client.get_channel(1167331643363696640) # testing @ https://discord.gg/CymKaDE2pj

        await logChannel.send( # only so i can train the chatbot
            embed = discordHelpers.embeds.warning(f"Failed to respond to:\n```{content.replace('`', '')}```")
        )
        
        # reply with error message
        errorMsg = {
            "no_query" : random.choice([
                "Sorry, I don't understand.",
                "Can you rephrase? I don't understand what you said.",
                "Sorry! I do not understand.",
                "I don't understand. Sorry.",
                "I don't understand. Could you say something else?"
            ]) + f" You can teach me a response with </{teachCMD.name}:1168118613249622016>.",
            "no_answer" : "Sorry, I couldn't think of a response."
        }[response.failureReason]
    
        await botMessage.edit(
            embed = discord.Embed(
                description = f"> :robot: :x: | **{errorMsg}**",
                color = discord.Colour.from_rgb(255, 125, 125)
            )
        )
    
# // Start the bot
client.run(config.botToken, log_handler = None)