# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Helpers
# // ---------------------------------------------------------------------

# // ---- Imports
from better_profanity import Profanity
import re

# // ---- Variables
filter = Profanity()
filter.load_censor_words()

# // ---- Functions
def isTextProfane(string: str) -> bool:
    return filter.contains_profanity(string) or string.find("https://") != -1 or string.find("http://") != -1

def censorProfaneText(string: str, linkCensorText: str = "[Censored Link]", generalCensorCharacter: str = "*") -> str:
    string = re.sub(
        pattern = "https?://\S+|www\.\S+|\S+\.\S+/\S+|\S+\?(\S+=\S+&?)*\S+", # remove links (source: chatgpt)
        repl = linkCensorText, 
        string = string, 
        flags = re.MULTILINE
    )

    return filter.censor(string, generalCensorCharacter)

def clamp(num: float|int, min: float|int, max: float|int):
    if num < min:
        return min
    
    if num > max:
        return max
    
    return num