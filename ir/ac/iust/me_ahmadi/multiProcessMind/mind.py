from __future__ import print_function
import traceback
import sys
import os

from language import Language
from attention import Attention

from memory import Memory
from workingMemory import WorkingMemory

from thinkWindow import ThinkWindow
from memoryWindow import MemoryWindow
from bodyWindow import BodyWindow



class Mind(object):
    __instance = None
    def __init__(self,verbose=True,dbpath="../agentdata"):
        self.__lastError = None
        self.output = print
        self.__clock = 0
        self.verbose = verbose    
        self.windows = []

        self.attention = Attention(self)
        self.language = Language(self)

        self.bodyWindow = BodyWindow.create(self)
        
        self.memory = Memory(self,dbpath)
        self.workingMemory = WorkingMemory(self)
        
        self.currentWindow = self.bodyWindow
        
        #TODO: a memory window!!!
        self.memoryWindow = MemoryWindow.create(self)
        self.attention.start()
        
    def shutdown(self):
        self.memory.shutdown()
        self.attention.completed = True
        for window in self.windows:
            window.completed = True
            print("stopped")

    def tick(self):
        self.__clock += 1
    def clock(self):
        return self.__clock

    @classmethod
    def singleton(cls,output):
        if cls.__instance == None:
            cls.__instance = Mind()
        cls.__instance.setBodyOutput(output)
        return cls.__instance        
    def __del__(self):
        self.shutdown()
    def version(self):
        return "Cognitive Agent Language For Mind Version 0.1\nTime + Space + Intelligence is at your service...."
    def prompt(self):
        return ">>>>"    
    def say(self,message):
#        self.log(message)
        self.output("log",message)
    def log(self,message):
        if self.verbose:
            print(message)
    def error(self,errorType,command):
        traceback.print_exc()
        self.__lastError = str(errorType)+":"+str(command)
        self.log("ERROR: "+self.__lastError) 
        return False
    def lastError(self):
        return self.__lastError
    def hasError(self):
        return (self.__lastError is not None)
    def clearError(self):
        self.__lastError = None

    def setBodyOutput(self,bodyOutput):
        self.output = bodyOutput
    def listen(self,message):
        return self.language.interpret(message)

            
   
    
