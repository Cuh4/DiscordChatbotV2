# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Globals Module
# // ---------------------------------------------------------------------

# // ---- Variables
savedGlobals: dict[str, any] = {}

# // ---- Functions
def save(name: str, value: any):
    savedGlobals[name] = value
    
def get(name: str, *, default: any = None):
    return savedGlobals.get(name, default)