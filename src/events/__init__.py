# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Events Init
# // ---------------------------------------------------------------------

# // Imports
from helpers.general import events as __events
from . import on_message
from . import report_response
from . import on_ready

# // Main
class events:
    on_message = __events.event("message_event").save()
    report_response = __events.event("report_response").save()
    on_ready = __events.event("on_ready").save()