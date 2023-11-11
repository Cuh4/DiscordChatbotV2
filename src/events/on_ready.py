
# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] On Ready
# // ---------------------------------------------------------------------

# // ---- Imports
import discord

from helpers import discord as discordHelpers
from helpers import general as helpers

from . import events

# // ---- Main
@events.on_ready.attach
async def callback(data: dict[str, any]):
    # // get needed vars
    # get discord stuffs
    client: discord.Client = helpers.globals.get("client")
    tree: discord.app_commands.CommandTree = data.get("tree")
    
    # // main
    # notify
    helpers.prettyprint.success(f"{discordHelpers.utils.formattedName(client.user)} has started.")
    
    # sync
    await tree.sync()