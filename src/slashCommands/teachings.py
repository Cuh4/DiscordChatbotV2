# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teachings Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from modules import pychatbot
from modules import general as helpers
from modules import discord as discordHelpers

# // ---- Variables
displayedKnowledgeAmount = 30

# // ---- Functions
def uniqueList(input: list):
    new = []
    
    for value in input:
        if value in new:
            continue
        
        new.append(value)
        
    return new

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
        
        # sort unique queries by time
        knowledgeList.sort(key = lambda knowledge: knowledge.getTimestamp(), reverse = True)
        
        # get unique knowledge, plus format a little
        queries = [knowledge.getQuery() for knowledge in knowledgeList]

        strippedQueries = [helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(query), 50) for query in uniqueList(queries)[:50]]
        
        formattedQueries = "- " + "\n- ".join(strippedQueries) if len(knowledgeList) >= 1 else "N/A"
        
        # send
        await interaction.response.send_message(
            embed = discordHelpers.embeds.info(f"**You have taught the bot responses to the following __{len(strippedQueries)}__ queries:**\n```{formattedQueries}```").set_footer(text = f"Showing {len(strippedQueries)}")
        )

# // start command
command()