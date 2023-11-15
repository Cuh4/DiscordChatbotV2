
# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] On Report
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import pychatbot
import config
from helpers import general as helpers
from helpers import discord as discordHelpers

from . import events

# // ---- Main
@events.on_report.attach
async def callback(**data):
    # // get needed vars
    # get discord stuffs
    client: discord.Client = helpers.globals.get("client")
    message: discord.Message = data.get("message")
    
    # get chatbot response
    response: pychatbot.chatbotResponse = data.get("response")
    
    # get report stuffs
    report: str = data.get("report")
    user: discord.User = data.get("user") # dont worry about stripping username of highlight markdown. discord doesnt allow the highlight character in usernames
    
    # // checks
    # quick check
    if not response.isSuccessful():
        return
    
    # // get things
    # get channel
    channel = client.get_channel(config.responseReportsChannelID)
    
    # strip text of " ` " to prevent messing up the code block format
    query = helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(response.getQuery()), 200)
    responseText =helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(response.getResponse()), 200)
    source = discordHelpers.utils.stripHighlightMarkdown(response.getSource())
    messageContent = helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(message.content), 200)
    report = discordHelpers.utils.stripHighlightMarkdown(report)
    
    # // send report
    # msg stuffs
    content = "\n".join([
        "`Message:`",
        f"```@{discordHelpers.utils.formattedName(message.author)}: {messageContent}```",
        "`Query:`",
        f"``` {query}```",
        "`Response:`",
        f"``` {responseText}```",
        "`Source:`",
        f"``` {source}```",
        "`Report:`",
        f"``` {report}```"
    ])

    # send report message
    await channel.send(
        embed = discordHelpers.embeds.warning(f"**A response was reported by @{discordHelpers.utils.formattedName(user)}.**\n{content}")
    )