# // ---------------------------------------------------------------------
# // ------- [Discord Chatbot v2] PyChatbot Knowledge
# // ---------------------------------------------------------------------

# // ---- Imports
import time
import json
import os
import sqlite3

from . import helpers

# // ---- Main
# // knowledgebase class
# responsible for storing responses to queries
class knowledgeBase:
    def __init__(self, name: str, knowledgePath: str):
        # properties
        self.name = name

        self.databaseName = helpers.pathSafeName(name) + ".db"
        self.databasePath = knowledgePath
        self.fullPath = os.path.abspath(os.path.join(self.databasePath, self.databaseName))

        # connect to db
        self.database = sqlite3.connect(self.fullPath)
        self.createDatabaseSchema()
        
    # // helpers
    def __getCursor(self):
        return self.database.cursor()
    
    def __commit(self):
        return self.database.commit()
    
    def __fetchAllOfColumn(self, columnIndex: int, allData: list):
        return [data[columnIndex] for data in allData]
    
    def __toKnowledge(self, data: list):
        return knowledge(self, data[0], data[1], data[2], data[3], json.loads(data[4]), data[5]) # id, query, response, source, custom data, timestamp
        
    # // methods
    def createDatabaseSchema(self):
        cursor = self.__getCursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS KnowledgeBase (
            id INTEGER PRIMARY KEY,
            query TEXT,
            response TEXT,
            source TEXT,
            data TEXT,
            timestamp REAL
        )""") # data is a json dict
        
        self.__commit()

    def getAllQueries(self) -> list[str]:
        cursor = self.__getCursor()
        allData = cursor.execute("SELECT query FROM KnowledgeBase")
        queries = self.__fetchAllOfColumn(0, allData)

        return queries
    
    def getKnowledgeWithSource(self, source: str) -> list["knowledge"]:
        # execute sql stuffs
        cursor = self.__getCursor()
        __savedKnowledge = cursor.execute("SELECT * FROM KnowledgeBase WHERE source = ?", [source]).fetchall()
        
        # return
        return [self.__toKnowledge(__knowledge) for __knowledge in __savedKnowledge]

    def getKnowledgeWithQuery(self, query: str) -> list["knowledge"]:
        # execute sql stuffs
        cursor = self.__getCursor()
        __savedKnowledge = cursor.execute("SELECT * FROM KnowledgeBase WHERE query = ?", [query]).fetchall()
        
        # return
        return [self.__toKnowledge(__knowledge) for __knowledge in __savedKnowledge]
    
    def getKnowledgeWithID(self, id: int):
        # execute sql stuffs
        cursor = self.__getCursor()
        __knowledge = cursor.execute("SELECT * FROM KnowledgeBase WHERE id = ?", [id]).fetchone()
        
        # return
        return self.__toKnowledge(__knowledge)
    
    def unlearn(self, id: int):
        self.__getCursor().execute("DELETE FROM KnowledgeBase WHERE id = ?", [id])
        self.__commit()
        
    def learn(self, query: str, response: str, source: str, *, data: dict[str, any] = {}):
        # save query and responses
        cursor = self.__getCursor()
        cursor.execute("INSERT OR IGNORE INTO KnowledgeBase (query, response, source, data, timestamp) VALUES (?, ?, ?, ?, ?)", [query, response, source, json.dumps(data), time.time()])
        
        self.__commit()
      
# // knowledge class
# represents knowledge on a specific query
# it's pretty much data from a sqlite db plopped into a class
class knowledge:
    def __init__(self, knowledgeBase: "knowledgeBase", id: int, query: str, response: str, source: str, data: dict[str, any], timestamp: float):
        self.__knowledgeBase = knowledgeBase

        self.__id = id
        self.__response = response
        self.__source = source
        self.__data = data
        self.__query = query
        self.__timestamp = timestamp

    def getKnowledgeBase(self):
        return self.__knowledgeBase
        
    def getID(self):
        return self.__id
        
    def getResponse(self):
        return self.__response
        
    def getSource(self):
        return self.__source
    
    def getData(self):
        return self.__data
    
    def getQuery(self):
        return self.__query
    
    def getTimestamp(self):
        return self.__timestamp
    
    def unlearn(self):
        return self.getKnowledgeBase().unlearn(self.getID())