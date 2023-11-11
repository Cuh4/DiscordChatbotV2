# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Slash Commands Init
# // ---------------------------------------------------------------------

def start():
    # importing the commands will automatically start them
    # is this a good way to do things? probably not
    from .teach import command as _
    from .restart import command as _
    from .unlearn import command as _