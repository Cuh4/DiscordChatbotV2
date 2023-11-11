# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Events Init
# // ---------------------------------------------------------------------

# // Imports
from helpers.general import events as __events
from . import on_message
from . import on_report
from . import on_ready

# // Main
class events:
    on_message = __events.event("message_event").save()
    on_report = __events.event("on_report").save()
    on_ready = __events.event("on_ready").save()