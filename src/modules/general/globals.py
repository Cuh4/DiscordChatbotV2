# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Globals Module
# // ---------------------------------------------------------------------

# // ---- Imports
import typing

# // ---- Variables
savedGlobals: dict[str, typing.Any] = {}

# // ---- Functions
def save(name: str, value: typing.Any):
    savedGlobals[name] = value
    
def get(name: str, *, default: typing.Any = None):
    return savedGlobals.get(name, default)