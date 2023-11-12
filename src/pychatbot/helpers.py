# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Helpers
# // ---------------------------------------------------------------------

# // ---- Imports
from better_profanity import profanity as filter
import re

# // ---- Variables
filter.load_censor_words()

# // ---- Functions
def simplifyText(string: str):
    punctuation = [*",.?;:-'!\""]
    
    for i in punctuation:
        string = string.replace(i, "")
        
    return string.lower()

def isTextProfane(string: str) -> bool:
    return filter.contains_profanity(string) or string.find("https://") != -1 or string.find("http://") != -1

def censorProfaneText(string: str, linkCensorText: str = "[Censored Link]", generalCensorCharacter: str = "*") -> str:
    newString = re.sub(
        pattern = "https?://\S+|www\.\S+|\S+\.\S+/\S+|\S+\?(\S+=\S+&?)*\S+", # remove links (source: chatgpt)
        repl = linkCensorText, 
        string = string, 
        flags = re.MULTILINE
    )
    
    newString = filter.censor(newString, generalCensorCharacter)
    return newString

def clamp(num: float|int, min: float|int, max: float|int):
    if num < min:
        return min
    
    if num > max:
        return max
    
    return num