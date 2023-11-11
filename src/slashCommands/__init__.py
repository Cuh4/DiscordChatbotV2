# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Slash Commands Init
# // ---------------------------------------------------------------------

# // Imports
import inspect

from .teach import command
from .restart import command
from .unlearn import command

# // Main
# starts all slash commands
def start():
    for func in dir():
        # not a function, so ignore
        if not inspect.isfunction(func):
            continue
        
        # not a slash command handler function, so ignore
        if func.__name__ != "command":
            continue
        
        # call function
        func()