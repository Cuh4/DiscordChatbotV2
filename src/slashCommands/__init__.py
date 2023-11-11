# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Slash Commands Init
# // ---------------------------------------------------------------------

# // Imports
import inspect

from .teach import command as teach
from .restart import command as restart
from .unlearn import command as unlearn

# // Variables
commands: list["function"] = []

# // Main
# register slash command
def register(func: "function"):
    global commands
    commands.append(func)

# starts all slash commands
def start():
    for command in commands:
        command()