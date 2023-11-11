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

# // Number
def clamp(number: float|int, min: float|int, max: float|int):
    if number < min:
        return min
    
    if number > max:
        return max
    
    return number