import threading
import time
from mdatetime import MDateTime
from attention import Attention

class ThinkWindow(threading.Thread):
    def __init__(self,mind):
        threading.Thread.__init__(self)
        self.mind = mind
        self.mind.windows.append(self)
        self.attention = self.mind.attention#Attention(self.mind.attention)
        self.completed = False
        self.__current_time = None
        self.__current_event = None
        self.__current_place = None
        self.__times = {}
    def __del__(self):
        pass
    def log(self,something):
        self.mind.log(somthing)
    def error(self,errorType,command):
        self.mind.error(errorType,command)        
    @classmethod
    def create(cls,mind):
        result = cls(mind)
        result.start()
        return result
    def run(self):
        while not self.completed:
           time.sleep(1) 
           
    def setEvent(self,event=None):
        #if current -> set next
        with self.mind.memory.db.transaction:
            if event==None:
                self.__current_event = self.mind.memory.db.node(type="Event")
            else:
                self.__current_event = event
        return self.__current_event
    def createSubEvent(self):
        if self.__current_event is None:
            return setEvent()
        last = self.__current_event
        new = self.setEvent()
        last.SUB(new)
        for w in last.WHEN.outgoing:
            new.WHEN(w.end)
        for p in last.WHERE.outgoing:
            new.WHERE(p.end)
    def currentEvent(self):
        if self.__current_event is not None:
            return self.__current_event
        return self.setEvent()
 
    def nowtime(self):
        return MDateTime()
    def setTime(self,timeObj=None,time=None):
        with self.mind.memory.db.transaction:
            lastTime = self.__current_time
            if timeObj==None:
                t = self.nowtime() if time is None else time
                self.__current_time = self.mind.memory.db.node(type="Time",time=t.isoformat(),mseconds=t.mseconds())
                self.__times[self.__current_time] = t
            else:
                self.__current_time = timeObj
                if not timeObj in self.__times.keys():
                    self.__times[timeObj] = MDateTime.fromMSeconds(timeObj["mseconds"])
                self.__times[self.__current_time] = self.__times[timeObj]
            self.mind.memory.timeIndex['time'][self.__current_time["time"]] = self.__current_time                
            self.mind.memory.timeIndex['mseconds'][self.__current_time["mseconds"]] = self.__current_time
            if lastTime != None:
                lastTime.NEXT(self.__current_time)
            
            if len(self.currentEvent().WHEN.outgoing)>0:
                lastEvent = self.currentEvent()
                self.createSubEvent()
                for rel in self.currentEvent().WHEN:
                    rel.delete()
            self.currentEvent().WHEN(self.__current_time)
        return self.__current_time
    def currentTimeObj(self):
        if self.__current_time is None:
            return self.setTime()
        else:
            return self.__current_time
    def currentTime(self):
        return self.__times[self.currentTimeObj()]

    def setPlace(self,place=None):
        with self.mind.memory.db.transaction:
            lastPlace = self.__current_place
            if place==None:
                self.__current_place = self.mind.memory.db.node(type="PlaceInstance")
            elif place.hasProperty("type") and place["type"]=="PlaceInstance":
                self.__current_place = place
            else:            
                self.__current_place = self.mind.memory.db.node(type="PlaceInstance")
                self.__current_place.INSTANCEOF(place)
            if lastPlace is not None:
                lastPlace.NEXT(self.__current_place)
            if len(self.currentEvent().WHERE.outgoing)>0:
                lastEvent = self.currentEvent()
                self.createSubEvent()
                for rel in self.currentEvent().WHERE:
                    rel.delete()
            self.currentEvent().WHERE(self.__current_place)                
        return self.__current_place
    def currentPlace(self):
        if self.__current_place is None:
            return self.setPlace()
        else:
            return self.__current_place

    def instanceOf(self,node,new=False):
        with self.mind.memory.db.transaction:
            place = self.currentPlace()
            if new:
                v = self.mind.memory.createNode()
                v.INSTANCEOF(node)
                v["type"] = "ObjectInstance"
                v.WHERE(place,type="in")
            else:
                contains = [r.end for r in place.WHERE.incoming if self.mind.memory.getProperty(r,"type")=="in"]
                v = node 
                if not self.mind.memory.isTypeOf(node, "ObjectInstance"):
                    found = False
                    for object in contains:
                        if self.mind.memory.isTypeOf(object,"ObjectInstance"):
                            for r in [r.end for r in object.INSTANCEOF.outgoing ]:
                                if node == r:
                                    v = object
                                    found = True
                                    break
                        if found:break
                    if not found:
                        v = self.mind.memory.createNode()
                        v.INSTANCEOF(node)
                        v["type"] = "ObjectInstance"
                if v not in contains:
                    v.WHERE(place,type="in")
        return v
