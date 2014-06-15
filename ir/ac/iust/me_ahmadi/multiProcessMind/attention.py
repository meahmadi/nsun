import threading
import time
class Attention(threading.Thread):
    def __init__(self,mind):
        threading.Thread.__init__(self)
        self.mind = mind
        self.attentionQueue = {}
        self.completed = False
    def attend(self,var,importance=0.05):
        currentT = self.mind.clock()
        for k,l in self.attentionQueue.items():
            for time,v in l.items():
                if var in v:
                    l[time].remove(v)
                if len(l[time])==0:
                    del l[time] 
        if importance not in self.attentionQueue.keys():
            self.attentionQueue[importance] = {}
        if currentT not in self.attentionQueue[importance].keys():
            self.attentionQueue[importance][currentT] = []
        self.attentionQueue[importance][currentT].append(var)    
    def updateQueue(self):
        for i,l in self.attentionQueue.items():
            now = self.mind.clock()
            for time,items in l.items():
                if (now - time) / i > 100:
                    self.mind.log("object is out of attention time:"+str(items))
                    del self.attentionQueue[i][item] 
            if len(l)==0:
                del self.attentionQueue[i]
    def run(self):
        while not self.completed:
            self.updateQueue()
            keys = sorted(self.attentionQueue.keys())
            if len(keys)>0:
                self.mind.tick()# progress of mind is goes...
                times = sorted(self.attentionQueue[keys[-1]].keys())
                vars = self.attentionQueue[keys[-1]].pop(times[-1],[])# attention to the newest item received
                for var in vars:
                    if type(var) == type([]):
                        for v in var:
                            self.mind.log("attention "+str(type(v)))
                    else:
                        self.mind.log("attention "+str(type(var)))
            time.sleep(0.1) 