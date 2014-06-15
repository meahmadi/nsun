import uuid

class WorkingMemory(object):
    def __init__(self,mind):
        self.mind = mind
        self.data = {}
        self.alias = {}
        for k,v in self.mind.memory.vars.items():
            self.data[k] = [v]
    
    def addMemoryResults(self,name,result):
        rs = []
        for k in result.keys():
            isList = False
            for row in result[k]:
                isList = True
                if row not in rs:
                    rs.append(row)
            if not isList:
                row = result[k].single
                if row not in rs:
                    rs.append(row)
        self.setVar(name, rs)
    def removeAlias(self,name):
        if name in self.alias:
            del self.alias[name]
    def setAlias(self,name,ref):
        self.alias[name] = ref
        if not(self.ifTempVar(name)):
            self.mind.attention.attend(ref)
    def getAliasRef(self,name):
        rname = name
        while rname in self.alias:
            rname = self.alias[rname]
        return rname
    def setVar(self,name,value):
        self.removeAlias(name)
        self.data[name] = value
        if not(self.ifTempVar(name)):
            self.mind.attention.attend(value)
    def getVar(self,name):
        if name == "root":
            return [self.mind.memory.findNodeById(0)]
        if name == "time":
            return [self.mind.currentWindow.currentTimeObj()]
        if name == "place":
            return [self.mind.currentWindow.currentPlace()]
        if name == "event":
            return [self.mind.currentWindow.currentEvent()]
        if name.startswith("`") and name.endswith("`"):
            try:
                id = int(name[1:-1].strip())
                return [self.mind.memory.findNodeById(id)]
            except:
                return []
        nname = name
        if nname.startswith("$"):            
            nname = nname [1:]
        rname = self.getAliasRef(nname)
        if rname in self.data.keys():
            return self.data[rname]
        else:
            return []
    def copyVar(self,src,target):
        self.setVar(target, self.getVar(src))
    def getVarProperties(self,var,prop):
        result = []
        if var is not None:
            for v in var:
                result.append(self.mind.memory.getProperty(v,prop))
        return result 
    def getTmpVarname(self):
        return "_tmp_"+str(uuid.uuid4())
    def ifTempVar(self,name):
        return name.startswith("_tmp_")    
    def gc(self):
        toDelete = []
        for k,v in self.data.items():
            if k.startswith("_tmp_") and k not in self.alias.values():
                toDelete.append(k)
        for k in toDelete:
            del self.data[k]
    def andVars(self,v1,v2):
        result = []
        for v in v1:
            if v in v2:
                result.append(v)
        return result
    def orVars(self,v1,v2):
        result = v1[:]
        for v in v2:
            if v not in result:
                result.append(v)
        return result
    def notVars(self,v1,v2):
        result = v1[:]
        for v in v2:
            if v in result:
                result.remove(v)
        return result
    def partOfVar(self,v,index):
        result = []
        if v is not None and len(v) > index:
            result = v[index]
        return result
    def isVarEmpty(self,var):
        if var is not None and len(var)>0:
            for x in var:
                if x is not None:
                    return True
        return False    
    def createRelation(self,relname,relprop,v1,v2):
        for v11 in v1:
            for v22 in v2:
                if v11 is not None and v22 is not None:
                    self.mind.memory.createRelation(relname,relprop,v11,v22)
    def setRelationProperties(self,var1,var2,relname,prop):
        for v1 in var1:
            for v2 in var2:
                if v1 is None or v2 is None:
                    continue
                setted = False
                if relname in [str(x.type) for x in v1.relationships.outgoing]:
                    for rel in getattr(v1,relname).outgoing:
                        if v2 == rel.end:
                            setted = True
                            self.mind.memory.setRelationProperties(rel, prop)
                if not setted:
                    self.mind.memory.createRelation(relname,prop,v1,v2)

    def setVarProperties(self,var,prop):
        for v in var:
            if v is not None:
                self.mind.memory.setNodeProperties(v,prop)            