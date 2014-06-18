import os

os.environ['NEO4J_PYTHON_JVMARGS'] = '-Xms128M -Xmx512M'
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-6-openjdk-amd64'

from neo4j import GraphDatabase


class Memory(object):
    def __init__(self,mind,dbpath="data"):
        self.mind = mind
        self.dbpath = dbpath
        
        self.mind.log("Starting Graph Database at "+dbpath)
        self.db = GraphDatabase(dbpath)
        self.root = None
        memorySize = len(self.db.nodes) 
        self.log("starting with "+str(memorySize)+" nodes in memory")
        self.vars = {}
        self.initialGraph(memorySize<=1)
    def __del__(self):
        self.shutdown()
    def shutdown(self):
        self.log("shutting down Graph Database...")
        self.db.shutdown()        
    def log(self,something):
        self.mind.log(something)
    def error(self,errorType,command):
        self.mind.error(errorType,command)
    def initialTime(self,create=False):
        if create:
            self.log("create time graph...")
            with self.db.transaction:
                self.timeIndex = self.db.node.indexes.create('abstractTime')
                self.eventIndex = self.db.node.indexes.create('events')
                
                self.vars["timeroot"] = self.createNode("TIME_ROOT")
                self.vars["root"].TIMERELATION(self.vars["timeroot"])
                self.vars["timeroot"].TIMERELATION(self.createNode("JALALI_CALENDAR"),cal_type="J")
                self.vars["timeroot"].TIMERELATION(self.createNode("HIJRI_CALENDAR"),cal_type="H")
                self.vars["timeroot"].TIMERELATION(self.createNode("GREGORY_CALENDAR"),cal_type="G")
        else:
            self.log("initial time...")
            with self.db.transaction:
                self.vars["timeroot"] = self.vars["root"].TIMERELATION.single.end
                self.timeIndex = self.db.node.indexes.get('abstractTime')
                self.eventIndex = self.db.nodes.indexes.get('events')
    def initialPlace(self,create=False):
        if create:
            self.log("create place graph ...")
            with self.db.transaction:
                self.placeIndex = self.db.node.indexes.create('abstractPlace')
                
                self.vars["placeroot"] = self.createNode(name="PLACE_ROOT")
                self.vars["root"].PLACERELATION(self.vars["placeroot"])
        else:
            self.log("initial place ...")
            with self.db.transaction:
                self.vars["placeroot"] = self.vars["root"].PLACERELATION.single.end
                self.placeIndex = self.db.node.indexes.get('abstractPlace')
    def initialObjects(self,create=False):
        if create:
            with self.db.transaction:
                self.vars["objectroot"] = self.createNode("OBJECT_ROOT")
                self.vars["root"].OBJECTRELATION(self.vars["objectroot"])
                
                self.vars["actionroot"] = self.createNode("ACTION_ROOT")
                self.vars["objectroot"].ACTIONRELATION(self.vars["actionroot"])
                self.vars["eventroot"]  = self.createNode("EVENT_ROOT")
                self.vars["objectroot"].EVENTRELATION(self.vars["eventroot"])
            
                self.vars["me"] = self.createNode('me')
                self.vars["me"].ISA(self.vars["objectroot"],type="me")
            
                self.vars["master"] = self.createNode('master')
                self.vars["master"].ISA(self.vars["objectroot"],type="master")
        else:
            self.vars["objectroot"] = self.vars["root"].OBJECTRELATION.single.end
            self.vars["actionroot"] = self.vars["objectroot"].ACTIONRELATION.single.end
            self.vars["eventroot"] = self.vars["objectroot"].EVENTRELATION.single.end
            self.vars["me"] = [rel for rel in self.vars["objectroot"].ISA.incoming if rel["type"]=="me" ][0].start
            self.vars["master"] = [rel for rel in self.vars["objectroot"].ISA.incoming if rel["type"]=="master" ][0].start
    def initialGraph(self,create=False):
        if create:
            self.log("create Graph ...")
            with self.db.transaction:
                self.vars["root"] = self.db.node[0]
                self.vars["root"]['name'] = 'ROOT'
                            
                self.nameIndex = self.db.node.indexes.create('name')
                self.indexName(self.vars["root"])
                self.messageIndex = self.db.node.indexes.create('message',type='fulltext')

        else:
            self.log("initial graph...")
            with self.db.transaction:
                self.vars["root"] = self.db.node[0]
                self.nameIndex = self.db.node.indexes.get('name')
                self.messageIndex = self.db.node.indexes.get('message')
        self.initialTime(create)
        self.initialPlace(create)
        self.initialObjects(create)        

    def getNodes(self,str):
        if str.startswith("`") and str.endswith("`"):
            result = []
            for id in str[1:-1].split(","):
                result.append(self.db.node[int(id)])
            if len(result)==1:
                return result[0]
            if len(result)>1:
                return result
        return str        
    def cypher(self,query):
        return self.db.query(query)
    def findNodeById(self,id):
        return self.db.nodes[id]
    
    def indexName(self,obj):
        try:
            del self.nameIndex['name'][obj['name']][obj]
        except: pass
        self.nameIndex['name'][obj['name']] = obj    
                

        
    def createNode(self,name=None):
        with self.db.transaction:
            if name == None:
                node = self.db.node()
            else:
                node = self.db.node(name=name)
                self.indexName(node)            
        return node
    def createNodeOFType(self, typename=None, prop={}):
        with self.mind.memory.db.transaction:
            name = None
            if "name" in prop.keys():
                name = prop["name"]
            node = self.createNode(name)
            self.setNodeProperties(node,prop)
            if typename is not None:
                typevar = self.objectType(typename)
                node.IS(typevar)
        return node
    
    def setNodeProperties(self,node,prop):
        with self.db.transaction:
            for k,v in prop.items():
                node[k] = v
                if k=="name":
                    self.indexName(node)
    def setRelationProperties(self,rel,prop):
        with self.db.transaction:
            for k,v in prop.items():
                rel[k] = v
    def createRelation(self,type,prop,src,target):
        with self.db.transaction:
            rel = src.relationships.create(type,target)
            self.setRelationProperties(rel, prop)

    def isTypeOf(self,node,type):
        return node is not None and node.hasProperty("type") and node["type"]==type
    
    def getProperty(self,node,name,default=None):
        if node is None or not node.hasProperty(name):
            return default
        else:
            return node[name]

    def typeOfObject(self,node):
        if node is None:
            return []
        result = []
        for v in node.IS.outgoing:
            if v.end.id != self.vars["objectroot"].id:
                result.append(v.end)
        return result
    def objectType(self,typename):
        with self.db.transaction:
            if typename==None:
                return self.vars["objectroot"]
            else:
                resultVarname = self.mind.workingMemory.getTmpVarname()
                query = """CYPHER 1.9 start root=node(0),t=node:name(name='%s') 
                            MATCH (root)-[:OBJECTRELATION]->()<-[:IS]-(t)  
                            RETURN t"""%(typename)
                self.mind.memoryWindow.cypher(resultVarname,query)
                resultVar = self.mind.workingMemory.getVar(resultVarname)
                if len(resultVar)==0 or resultVar[0] is None:
                    typevar = self.createNode(typename)
                    typevar.IS(self.mind.workingMemory.getVar("objectroot")[0])
                else:
                    typevar = resultVar[0]
        return typevar
    def actionType(self,subject,actionname):
        with self.db.transaction:
            resultVarname = self.mind.workingMemory.getTmpVarname()
            if len(subject)==0:
                query = """CYPHER 1.9 start root=node(0),t=node:name(name='%s') 
                            MATCH (root)-[:OBJECTRELATION]->()-[:ACTIONRELATION]->()<-[r:IS]-(t)
                            WHERE has(r.type) and r.type="objective"  
                            RETURN t"""%(actionname)
                self.mind.memoryWindow.cypher(resultVarname,query)
                resultvar = self.mind.workingMemory.getVar(resultVarname)
                if resultvar is None or len(resultvar)==0 or resultvar[0] is None:
                    actionvar = self.createNode(actionname)
                    actionvar.IS(self.vars["actionroot"],type="objective")
                else:
                    actionvar = resultvar[0]
                return [actionvar]
            else:
                for sbj in subject:
                    sbjtype = self.typeOfObject(sbj)
                    print sbjtype
                    if len(sbjtype) == 0:
                        sbjtype = [sbj]
                    actionvars = []
                    for st in sbjtype:
                        query = """CYPHER 1.9 start root=node(0),t=node:name(name='%s') 
                                    MATCH (root)-[:OBJECTRELATION]->()-[:ACTIONRELATION]->()<-[r:IS]-(w)-[:WHO]->(t)
                                    WHERE has(r.type) and r.type="subjective"  
                                    RETURN w"""%(self.getProperty(st, "name", "---"))
                        self.mind.memoryWindow.cypher(resultVarname,query)
                        resultvar = self.mind.workingMemory.getVar(resultVarname)
                        if resultvar is None or len(resultvar)==0 or resultvar[0] is None:
                            actionvar = self.createNode(self.getProperty(st, "name", "---"))
                            actionvar.IS(self.vars["actionroot"],type="subjective")
                            actionvar.WHO(st)
                        else:
                            actionvar = resultvar[0]
                        created = False
                        for ins in actionvar.IS.incoming:
                            if self.getProperty(ins, "name") == actionname:
                                created = True
                                actionvars.append(ins)
                        if not created:
                            ins = self.createNode(actionname)
                            ins.IS(actionvar)
                            actionvars.append(ins)
                    return actionvars
                        
                            
    
