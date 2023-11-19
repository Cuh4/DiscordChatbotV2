# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Chatbot
# // ---------------------------------------------------------------------

# // ---- Imports
import random
import difflib

from . import knowledgeBase
from . import helpers

# // ---- Main
# // chatbot class
# main class that should be used for responding to queries, etc
class chatbot:
    def __init__(self, name: str, knowledgePath: str = "", confidence: float = 0.4, allowProfanity: bool = True, customKnowledgeBase: "knowledgeBase" = None):
        # chatbot name
        self.name = helpers.capitalizeName(name)
        
        # knowledge
        self.knowledgeBase = customKnowledgeBase or knowledgeBase(self.name, knowledgePath)
        
        # properties
        self.confidence = helpers.clamp(confidence, 0, 1)
        self.profanityAllowed = allowProfanity
        
    # // helpers
    def __getQuery(self, query: str, *, overrideConfidence: int|float = None) -> tuple[str, float|int]|tuple[None, None]:
        # find a response for this query
        confidence = overrideConfidence or self.confidence
        matches = difflib.get_close_matches(query, self.knowledgeBase.getAllQueries(), 6, confidence)

        if len(matches) > 0:
            match = matches[0]
            return match, difflib.SequenceMatcher(None, query, match).ratio() # note: might want to use "quick_ratio" since "ratio" is apparently computationally expensive
        
        # since we found nothing, let's try again with a lower confidence
        if overrideConfidence and overrideConfidence <= self.confidence / 6: # took too many tries (or confidence is 0), so lets just give up
            return None, None
        
        newConfidence = confidence / 1.25 # lower confidence slightly
        query, responseConfidence = self.__getQuery(query = query, overrideConfidence = newConfidence)
    
        return query, responseConfidence
        
    # // methods
    def respond(self, query: str):
        # simplify
        query = helpers.simplifyText(query)
        
        # get the remembered query
        knownQuery, responseConfidence = self.__getQuery(query)

        # doesn't exist, so return
        if knownQuery is None:
            return chatbotResponse(
                self,
                isSuccessful = False,
                reasonForFailure = "no_query"
            )
        
        # get knowledge for the query
        knowledge = self.knowledgeBase.getKnowledgeWithQuery(knownQuery)
 
        # no responses found, so return here
        if len(knowledge) <= 1:
            return chatbotResponse(
                self,
                isSuccessful = False,
                reasonForFailure = "no_kowledge"
            )
            
        # get a "random piece of knowledge"
        chosenKnowledge = random.choice(knowledge)
            
        # check for profanity
        if helpers.isTextProfane(chosenKnowledge.getResponse()) and not self.profanityAllowed:
            return chatbotResponse(
                self,
                isSuccessful = False,
                reasonForFailure = "profanity"
            )
        
        # return the answer
        return chatbotResponse(
            self,
            chosenKnowledge,
            responseConfidence,
            True
        )
        
# // chatbot response class
# represents a response to a query
class chatbotResponse:
    def __init__(self, parent: "chatbot", knowledge: "knowledgeBase" = None, responseConfidence: float|int = 0, isSuccessful: bool = True, reasonForFailure: str = ""):
        self.__chatbot = parent
        
        self.__response = knowledge.getResponse()
        self.__responseConfidence = responseConfidence
        
        self.__source = knowledge.getSource()
        self.__data = knowledge.getData()
        self.__query = knowledge.getQuery()
        
        self.__success = isSuccessful
        self.__failureReason = reasonForFailure

    def getChatbot(self):
        return self.__chatbot

    def getData(self):
        return self.__data
    
    def getSource(self):
        return self.__source
    
    def getQuery(self):
        return self.__query
        
    def getResponse(self):
        return self.__response
    
    def getResponseConfidence(self):
        return self.__responseConfidence
    
    def isSuccessful(self):
        return self.__success
    
    def getFailureReason(self):
        return self.__failureReason