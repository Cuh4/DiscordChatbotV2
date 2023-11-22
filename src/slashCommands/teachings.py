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
        
        # sort knowledge by time
        if len(knowledgeList) >= 1:
            knowledgeList.sort(key = lambda knowledge: knowledge.getTimestamp(), reverse = True)
        
        # format knowledge
        uniqueQueries = set([knowledge.getQuery() for knowledge in knowledgeList])
        strippedQueries = [helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(query), 50) for query in uniqueQueries][:displayedKnowledgeAmount]
        formattedQueries = "- " + "\n- ".join(set(strippedQueries)) if len(knowledgeList) >= 1 else "N/A" # using "set()" to avoid duplicates
        
        # send
        await interaction.response.send_message(
            embed = discordHelpers.embeds.info(f"**You have taught the bot responses to the following __{len(uniqueQueries)}__ queries:**\n```{formattedQueries}```").set_footer(text = f"Showing {len(strippedQueries)} out of {len(uniqueQueries)}")
        )

# // start command
command()