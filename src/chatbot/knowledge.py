# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] Chatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
import json
import os

# // ---- Main
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
        
    def learn(self, query: str, answers: list[str]):
        # tags system
        for index, answer in enumerate(answers):
            for tagName, tag in self.tags.items():
                answer = answer.replace(tagName, tag)
                
            answers[index] = answer
        
        # update
        data = self.read()
        answersFromData = data.get(query, None)
        
        if answersFromData is not None: # if answers for this query already exist, then join these new answers up with them
            for answer in answers:
                if answer not in answersFromData: # prevent adding two of the same answer
                    answersFromData.append(answer)
        else: # if they don't exist, then create
            answersFromData = answers
            
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