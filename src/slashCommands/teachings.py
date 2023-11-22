# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teachings Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

import pychatbot
from helpers import general as helpers
from helpers import discord as discordHelpers

# // ---- Variables
displayedKnowledgeAmount = 30

# // ---- Main
# // create command
def command():
    # // get vars
    # discord-related
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = helpers.globals.get("commandTree")

    # other
    chatbot: pychatbot.chatbot = helpers.globals.get("chatbot")

    # // main command
    # slash command
    @tree.command(
        name = "teachings",
        description = "Displays everything you have taught the chatbot."
    )
    async def command(interaction: discord.Interaction):
        # get knowledge made by this person
        knowledgeList = chatbot.knowledgeBase.getKnowledgeWithSource(interaction.user.id)
        
        # sort responses by time
        if len(knowledgeList) >= 1:
            knowledgeList.sort(key = lambda knowledge: knowledge.getTimestamp(), reverse = True)
        
        # format them
        strippedQueries = [helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(knowledge.getQuery()), 50) for knowledge in knowledgeList][:displayedKnowledgeAmount] if len(knowledgeList) > 0 else "N/A"
        formattedQueries = "- " + "\n- ".join(set(strippedQueries)) # using "set()" to avoid duplicates

        knowledgeCreated = len(knowledgeList)
        
        # send
        await interaction.response.send_message(
            embed = discordHelpers.embeds.info(f"**You have taught the bot responses to the following __{knowledgeCreated}__ queries:**\n```{formattedQueries}```").set_footer(text = f"Showing {displayedKnowledgeAmount} out of {knowledgeCreated}")
        )

# // start command
command()