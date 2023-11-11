
# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] On Report
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import chatbot
import config
from helpers import general as helpers
from helpers import discord as discordHelpers

from . import events

# // ---- Main
@events.on_report.attach
async def callback(data: dict[str, any]):
    # // get needed vars
    # get discord stuffs
    client: discord.Client = helpers.globals.get("client")
    message: discord.Message = data.get("message")
    
    # get chatbot response
    response: chatbot.response = data.get("response")
    
    # get report stuffs
    reasons: list[str] = data.get("reasons")
    
    # // checks
    # quick check
    if not response.isSuccessful():
        return
    
    # // get things
    # get channel
    channel = client.get_channel(config.responseReportsChannelID)
    
    # strip text of " ` " to prevent messing up the code block format
    query = discordHelpers.utils.stripHighlightMarkdown(response.getQuery())
    responseText = discordHelpers.utils.stripHighlightMarkdown(response.getText())
    source = discordHelpers.utils.stripHighlightMarkdown(response.getSource())
    messageContent = discordHelpers.utils.stripHighlightMarkdown(message.content)
    
    # format reasons
    reasons = "-" + "\n- ".join(reasons) if len(reasons) >= 1 else "N/A"
    
    # // send report
    # msg stuffs
    content = "\n".join([
        "`Message:`",
        f"```{messageContent}```",
        "`Query:`",
        f"```{query}```",
        "`Response:`",
        f"```{responseText}```",
        "`Source:`",
        f"```{source}```",
        "`Report Reason",
        f"```{reasons}```"
    ])

    # send report message
    await channel.send(
        embed = discordHelpers.embeds.warning(f"**A response was reported by @{discordHelpers.utils.formattedName(message.author)}.**\n{content}")
    )