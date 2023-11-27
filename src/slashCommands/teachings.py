# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Teachings Slash Command
# // ---------------------------------------------------------------------

# // ---- Imports
from enum import unique
from site import removeduppaths
import discord

import pychatbot
from modules import general as helpers
from modules import discord as discordHelpers

# // ---- Variables
displayedKnowledgeAmount = 30

# // ---- Functions
def removeDuplicatesOfKnowledge(knowledgeList: list["pychatbot.knowledge.knowledge"]):
    new = knowledgeList.copy()
    previous = []
    
    for index, knowledge in enumerate(new):
        query = knowledge.getQuery()
        
        if query in previous:
            new.pop(index)
            
        previous.append(query)
        
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
        uniqueKnowledge = removeDuplicatesOfKnowledge(knowledgeList)
        
        # sort unique queries by time
        uniqueKnowledge.sort(key = lambda knowledge: knowledge.getTimestamp(), reverse = True)
        
        # format everything
        strippedQueries = [helpers.misc.truncateIfTooLong(discordHelpers.utils.stripHighlightMarkdown(knowledge.getQuery()), 50) for knowledge in uniqueKnowledge][:displayedKnowledgeAmount]
        formattedQueries = "- " + "\n- ".join(strippedQueries) if len(uniqueKnowledge) >= 1 else "N/A" # using "set()" to avoid duplicates
        
        # send
        await interaction.response.send_message(
            embed = discordHelpers.embeds.info(f"**You have taught the bot responses to the following __{len(strippedQueries)}__ queries:**\n```{formattedQueries}```").set_footer(text = f"Showing {len(strippedQueries)}")
        )

# // start command
command()