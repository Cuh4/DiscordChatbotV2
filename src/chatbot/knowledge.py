# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
import json
import os

# // ---- Main
class answer:
    def __init__(self, text: str, source: str):
        self.text = text
        self.source = source
        
    def getText(self):
        return self.text
    
    def getSource(self):
        return self.source

class knowledge:
    def __init__(self, knowledgeFilePath: str):
        # properties
        self.path = knowledgeFilePath
        self.tags = {}
        
        # create knowledge file if it doesnt exist
        if not self.fileExists():
            self.save({})
            
        # keep data stored
        self.data = self.read()
        
    def __tagName(self, name: str):
        return f"[{name}]"
        
    def addTag(self, tagName: str, tag: str):
        self.tags[self.__tagName(tagName)] = tag
        
    def removeTag(self, tagName: str):
        self.tags.pop(self.__tagName(tagName))
        
    def getAllQueries(self):
        return list(self.data.keys())
    
    def getAnswersForQuery(self, query: str) -> list[dict[str, str]]:
        return self.data.get(query, [])
        
    def learn(self, query: str, answers: list[answer]):
        # tags system
        for index, __answer in enumerate(answers):
            for tagName, tag in self.tags.items():
                __answer.text = __answer.text.replace(tagName, tag)
                
            answers[index] = __answer
        
        # retrieve saved knowledge
        data = self.read()
        
        # get all answers for the specified query
        answersFromData = data.get(query, answers)
        
        # add the new answers if they aren't already added
        for __answer in answers:
            if __answer not in answersFromData: # prevent adding two of the same answer
                answersFromData.append(vars(__answer))
            
        data[query] = answersFromData # apply changes
        
        # save changes
        self.save(data)
        self.data = data
        
    def save(self, data: dict):
        with open(self.path, "w") as file:
            json.dump(
                obj = data,
                fp = file,
                indent = 6
            )
            
    def read(self) -> dict[str, list[str]]:
        with open(self.path, "r") as file:
            return json.load(
                fp = file
            )
            
    def fileExists(self):
        return os.path.exists(self.path)