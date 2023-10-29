# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Misc
# // ---------------------------------------------------------------------

# // ---- Main
# // String
def doesStringOnlyContainLetter(string: str, letters: str):
    return set(string) <= set(letters)

def truncateIfTooLong(string: str, maxLength: int, ending: str = "..."):
    if len(string) > maxLength:
        return string[: maxLength - len(ending)] + ending
    
    return string