from thinkWindow import ThinkWindow
import time

class MemoryWindow(ThinkWindow):
    def __init__(self,mind):
        ThinkWindow.__init__(self,mind)
        self.query = ""
        
    def cypher(self,name,query):
        self.__doCypher(name,query)
        #self.query = query
        #self.queryName = name
        #time.sleep(2)
        #TODO: check the time, cancle or resume the last and ....
    def findOrCreate(self, varname,condition):
        startQuery = " ur=node(0)"
        createQuery = ""
        whereQuery = " (1=1) "
        returnQuery = ""
        
        node = True
        varCnt = 0
        resultVars= []
        for c in condition:
            var = "var%d"%varCnt
            if node:
                name = c[0]
                prop = {}
                if len(c)>1:
                    prop = c[1]
                if name.startswith("!"):
                    resultVars.append(var)
                    name = name[1:]
                if name.startswith("?"):
                    pass
                elif name.startswith("$") or (name.startswith("`") and name.endswith("`")):
                    v = self.mind.workingMemory.getVar(name)
                    if len(v)>0:
                        ids = ""
                        for n in v:
                            if n is None:
                                continue
                            if len(ids)>0:
                                ids += ","
                            ids += str(n.id)
                        startQuery += ", %s=node(%s)"%(var,ids)
                    else:
                        self.mind.workingMemory.setVar(varname,[])
                        return
                        #startQuery += ", %s=node(-1)"%(var)
                else:
                    prop["name"] = name
                    
                if len(prop.keys())==0:
                    createQuery +="(%s)"%(var)
                else:
                    createQuery +="(%s{"%(var)
                    firstArg = True
                    for k,v in prop.items():
                        if not firstArg:
                                createQuery += "," 
                        else:
                            firstArg = False
                        if type(v) == type(" ") or type(v)==type(u" "):
                            createQuery += " %s: \"%s\" "%(k,v.replace("\"","\\\""))
                        else:
                            createQuery += " %s: %s "%(k,v)
                    createQuery += "})"
            else:
                if c[0]=="<":
                    createQuery += "<-"
                elif c[0]==">":
                    createQuery += "->"
                else:
                    createQuery += "-"
                    
                relationName = c[1][0]
                createQuery += "[%s"%var 
                if len(relationName)>0:
                    q = relationName
                    createQuery +=":%s"%q
                createQuery += "]" 
                if len(c[1])>1:
                    for k,v in c[1][1].items(): 
                        if type(v) == type(" ") or type(v) == type(u" "):
                            whereQuery += " and %s.%s! = \"%s\" "%(var,k,v.replace("\"","\\\""))
                        else:
                            whereQuery += " and %s.%s! = %s "%(var,k,v)
            
                if c[-1]=="<":
                    createQuery += "<-"
                elif c[-1]==">":
                    createQuery += "->"
                else:
                    createQuery += "-"
            varCnt += 1
            node = not node
        if len(resultVars)==0:
            returnQuery = "*"
        else:
            returnQuery += resultVars[0]
            for re in resultVars[1:]:
                returnQuery += ","+re
        query = "CYPHER 1.9 start %s \n WHERE %s \n CREATE UNIQUE %s \n RETURN distinct %s"%(startQuery,whereQuery,createQuery,returnQuery)
        self.cypher(varname,query)        

    def find(self,varname,findType,condition):
        expressionName = self.mind.workingMemory.getTmpVarname()
        expressionCnt = 0 
        
        resultVar = expressionName
        startQuery = ""
        matchQuery = ""
        whereQuery = " (1=1) "
        returnQuery = ""
        node = True
        varCnt = 0
        resultVars= []
        for c in condition:
            var = "var%d"%varCnt
            if node:
                name = c[0]
                if name.startswith("!"):
                    resultVars.append(var)
                    name = name[1:]
                if len(startQuery)>0:
                        startQuery += ","
                if name.startswith("?"):
                    startQuery += "%s=node(*)"%(var)
                elif name.startswith("$") or (name.startswith("`") and name.endswith("`")):
                    v = self.mind.workingMemory.getVar(name)
                    if len(v)>0:
                        ids = ""
                        for n in v:
                            if len(ids)>0:
                                ids += ","
                            ids += str(n.id)
                        startQuery += "%s=node(%s)"%(var,ids)
                    else:
                        startQuery += "%s=node(*)"%(var)
                else:
                    startQuery += "%s=node:name(name='%s')"%(var,name)
                    
                matchQuery +="(%s)"%(var)
                if len(c)>1:
                    for k,v in c[1].items(): 
                        if type(v) == type(""):
                            whereQuery += " and %s.%s! = \"%s\" "%(var,k,v.replace("\"","\\\""))
                        else:
                            whereQuery += " and %s.%s! = %s "%(var,k,v)
            else:
                if c[0]=="<":
                    matchQuery += "<-"
                elif c[0]==">":
                    matchQuery += "->"
                else:
                    matchQuery += "-"
                    
                relationName = c[1][0]
                matchQuery += "[%s"%var 
                if len(relationName)>0:
                    q = relationName
                    matchQuery +=":%s"%q
                matchQuery += "]" 
                if len(c[1])>1:
                    for k,v in c[1][1].items(): 
                        if type(v) == type(""):
                            whereQuery += " and %s.%s! = \"%s\" "%(var,k,v.replace("\"","\\\""))
                        else:
                            whereQuery += " and %s.%s! = %s "%(var,k,v)
            
                if c[-1]=="<":
                    matchQuery += "<-"
                elif c[-1]==">":
                    matchQuery += "->"
                else:
                    matchQuery += "-"
            varCnt += 1
            node = not node
        if len(resultVars)==0:
            returnQuery = "*"
        else:
            returnQuery += resultVars[0]
            for re in resultVars[1:]:
                returnQuery += ","+re
        query = "CYPHER 1.9 start %s \n MATCH %s \n WHERE %s \n RETURN distinct %s"%(startQuery,matchQuery,whereQuery,returnQuery)
        self.cypher(resultVar,query)
        #"when" "where" "who" "the" "someof" "all" "a" "some"
        var = self.mind.workingMemory.getVar(resultVar)
        result = []
        if findType=="all":
            result = var
        elif findType=="the":
            if len(var)>0:
                result = [var[0]]
        elif findType=="only":
            if len(var)==1:
                result = [var[0]]                            
        elif findType=="some":
            result = var
        elif findType=="when":#TODO very basic, should imporve
            result = []
            for node in var:
                for x in node.WHEN.outgoing:
                    result.append(x.end)
                for r in node.INSTANCEOF.incoming:
                    for x in r.start.WHEN.outgoing:
                        result.append(x.end)
        elif findType=="where":#TODO very basic, should imporve
            result = []
            for node in var:
                for x in node.WHERE.outgoing:
                    result.append(x.end)
                for r in node.INSTANCEOF.incoming:
                    for x in r.start.WHERE.outgoing:
                        result.append(x.end) 
        elif findType=="who":#TODO very basic, should imporve
            result = []
            for node in var:
                for x in node.WHO.outgoing:
                    result.append(x.end)
        elif findType=="someof":#TODO very basic, should imporve
            for node in var:
                for x in node.INSTANCEOF.incoming:
                    result.append(x.start)
        elif findType=="a":#TODO very basic, should imporve
            result = []
            for node in var:
                x = node.INSTANCEOF.incoming.single
                if x is not None:
                    result.append(x.start)
        if None in result:
            result.remove(None)
        self.mind.workingMemory.setVar(varname,result)        
                
    def __doCypher(self,name,query):
        self.mind.log("new query:"+name+","+query)
        try:
            result = self.mind.memory.cypher(query)
            self.mind.workingMemory.addMemoryResults(name,result)
        except Exception as e:
            self.mind.workingMemory.setVar(name,[])
            self.mind.log(e)
                
                

