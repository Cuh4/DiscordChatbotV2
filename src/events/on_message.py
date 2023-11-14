
# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] On Message Event
# // ---------------------------------------------------------------------

# // ---- Imports
import discord
import random

import pychatbot
import config
import ui
from helpers import discord as discordHelpers
from helpers import general as helpers

from . import events

# // ---- Main
# // Chatbot Responses
@events.on_message.attach
async def callback(**data):
    # // get needed vars
    # get discord stuffs
    client: discord.Client = helpers.globals.get("client")
    message: discord.Message = data.get("message")
    
    # get chatbot
    chatbot: pychatbot.chatbot = helpers.globals.get("chatbot")
    
    # // basic checks
    # ignore messages sent by bots
    if message.author.bot:
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
    if pychatbot.helpers.isTextProfane(content) and not config.allowProfanity:
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
    response = chatbot.respond(content)

    # reply with response
    if response.isSuccessful():
        text = response.getResponse()
        query = response.getQuery()
        source = response.getSource()
        data = response.getData()
        isBuiltIn = not data.get("is_created_by_discord_user", False)
        
        # setup source
        if not isBuiltIn:
            source = "@" + data.get("cached_username")
        
        # response length check check
        if len(text) > config.maxResponseLength:
            text = "Whoops! My original response was too long."
            
        # remove profanity
        text = pychatbot.helpers.censorProfaneText(text)
            
        # get rid of markdown
        text = discordHelpers.utils.stripMarkdown(text)
        query = discordHelpers.utils.stripMarkdown(query)

        # print success message to terminal
        helpers.prettyprint.success(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)}: {text}")

        # setup response embed
        responseEmbed = discord.Embed(
            description = f"> :robot: :speech_balloon: `{chatbot.name}` | **{text}**",
            color = discord.Colour.from_rgb(125, 255, 125)
        )
        
        responseEmbed.set_footer(text = f"Response produced by {source} | Response may be inaccurate. | Response Confidence: {round(response.getResponseConfidence() * 100, 1)}%", icon_url = message.author.display_avatar.url)

        # reply with response
        feedbackView = ui.views.wrap(
            botMessage, # to allow for future edits
            ui.views.feedback(response, message)
        )

        await botMessage.edit(
            embed = responseEmbed,
            view = feedbackView
        )
    else:
        failureReason = response.getFailureReason()
        
        # unsuccessful (timed out or couldn't find appropriate response)
        helpers.prettyprint.warn(f"🤖| Reply to {discordHelpers.utils.formattedName(message.author)} failed. Reason: {failureReason}")

        # reply with error message
        errorMsg = {
            "no_query" : random.choice([
                "Sorry, I don't understand.",
                "Can you rephrase? I don't understand what you said.",
                "Sorry! I do not understand.",
                "I don't understand. Sorry.",
                "I don't understand. Could you say something else?"
            ]) + f" You can teach me a response with </teach:1168118613249622016>.",
            "no_answer" : "Sorry, I couldn't think of a response.",
            "profanity" : "Sorry, my response contained profanity and was therefore not sent."
        }[failureReason]
    
        await botMessage.edit(
            embed = discord.Embed(
                description = f"> :robot: :x: | **{errorMsg}**",
                color = discord.Colour.from_rgb(255, 125, 125)
            )
        )