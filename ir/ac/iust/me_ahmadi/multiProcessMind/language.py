import pyparsing as pp
import sys
import traceback
import random
import re
import copy
from mdatetime import MDateTime


class Basket(object):
    pass

class Language(object):
    def __init__(self,mind):
        self.mind = mind
        self.initialParser()
    def log(self,something):
        self.mind.log(something)
    def error(self,errorType,command):
        self.mind.error(errorType,command)        
    def interpret(self,raw_command):
        try:
            self.log("interpret:"+raw_command)
            if len(raw_command.strip())==0:
                return True
            result = self.expression.parseString(raw_command,parseAll=True)
            return True
        except pp.ParseException as x:
            self.error("Line {e.lineno}, column {e.col}:{e.parserElement}{e.msg}\n'{e.line}'".format(e=x),str(x))
            return False
        except:
            self.error(sys.exc_info()[0],raw_command)
            traceback.print_exc()
            return False        

    def simpleDictToStr(self,d):
        r = "{"
        first = True
        for k,v in d.items():
            if not first:
                r += ", "
            r += str(k) + ":"
            if type(v) == type(str):
                r += "'%s'"%v
            else:
                r += str(v)
            first = False
        r += "}"
        return r
    def neo4jToStr(self,results,var=None):#TODO buffy
        rr =""
        if results is None:
            rr = "NONE"
        else:
            if type(results) == type([]):
                for r in results:
                    rr += self.nodeToStr(r, var) + "\n"
            else:
                rr = str(results)
        return rr.strip()
    def nodeToStr(self,node,var=None):
        dir(node)
        if node is None:
            return "None"
        if var is None:
            d = {}
            d["outgoing"] = []
            for rel in node.relationships.outgoing:
                d["outgoing"].append((rel.end.id,str(rel.type),rel.to_dict()))
            d["incoming"] = []
            for rel in node.relationships.incoming:
                d["incoming"].append((rel.start.id,str(rel.type),rel.to_dict()))
            for k,v in node.to_dict().items():
                d[k] = v
            d["id"] = node.id
            return str(d)
        else:
            var = var[1:]
            if node.hasProperty(var):
                return str(node[var])
            else:
                return ""


    def parseQuotedString(self,s,loc,tokens):
        return tokens[0][1:-1]
    def parseNumber(self,s,loc,tokens):
        return float(tokens[0])
    def parseDict(self,s,loc,tokens):
        result = {}
        for nv in tokens[0]:
            val = nv[1]
            if type(val)== type(str):
                 val = val.strip("\"")
            result[nv[0]] = val
        return result
    def parseObjectId(self,s,loc,tokens):
        return [self.db.node[int(tokens[0][0])]]
    def parseVarToId(self,s,loc,tokens):
        if not(tokens[0][0].startswith("`") and tokens[0][0].endswith("`")):
            result = []
            var = self.mind.workingMemory.getVar(tokens[0][0])
            if var is None:
                return result
            for v in var:
                result.append("`%d`"%v.id)
            return result
        return tokens[0]
    def parseComment(self,s,loc,tokens):
        return None
    def parseVarProp(self,s,loc,tokens):
        var = self.mind.workingMemory.getVar(tokens[0][0])
        return self.mind.workingMemory.getVarProperties(var,tokens[0][1])
    def parseNewNodeFromProperties(self,s,loc,tokens):
        var = self.mind.workingMemory.getTmpVarname()

        if len(tokens)>1:
            typename = tokens[0]
            prop = tokens[1]
        else:
            typename = None
            prop = tokens[0]
        
        node = self.mind.memory.createNodeOFType(typename,prop)
        self.mind.workingMemory.setVar(var,[node])
        return var
    def parseVarOper(self,s,loc,tokens):
        var = self.mind.workingMemory.getTmpVarname()
        v1 = self.mind.workingMemory.getVar(tokens[0])
        v2 = self.mind.workingMemory.getVar(tokens[2])
        result = []
        if tokens[1].upper() == "AND":
            result = self.mind.workingMemory.andVars(v1,v2)
        if tokens[1].upper() == "OR":
            result = self.mind.workingMemory.orVars(v1,v2)
        if tokens[1].upper() == "NOT":
            result = self.mind.workingMemory.notVars(v1,v2)
        self.mind.workingMemory.setVar(var,result)
        return var
    def parseVarArray(self,s,loc,tokens):
        var = self.mind.workingMemory.getTmpVarname()
        v1 = self.mind.workingMemory.getVar(tokens[0])
        result = self.mind.workingMemory(v1,tokens[1])
        self.mind.workingMemory.setVar(var,result)
        return var 
    def parseExpression(self,s,loc,tokens):
        self.log(tokens)
    def sayingAction(self,s,loc,tokens):
        self.log("saying:")
        self.log(str(s)+str(loc)+str(tokens))
    def exitAction(self,s,loc,tokens):
        self.mind.shutdown()
        exit()
    def parseAction(self,s,loc,tokens):
        self.log(str(s)+str(loc)+str(tokens))
    def parseIsExpression(self,s,loc,tokens):
        varname = tokens[1]
        var = self.mind.workingMemory.getVar(varname)
        if self.mind.workingMemory.isVarEmpty(var):
            self.mind.say("YES")
        else:
            self.mind.say("NO")
    def parseCypherExpression(self,s,loc,tokens):
        var = tokens[1]
        query = tokens[2]
        self.mind.memoryWindow.cypher(var,query)
    def parseWhatExpression(self,s,loc,tokens):
        results = []
        if len(tokens)==1:
            seen = []
            for k1,v1 in self.mind.workingMemory.alias.items():
                for k2,v2 in self.mind.workingMemory.data.items():
                    if v1==k2:
                       results.append("%s=%s"%(k1,self.neo4jToStr(v2)))
                       seen.append(k2)
                       break
            for k,v in self.mind.workingMemory.data.items():
                if k not in seen and not k.startswith("_tmp_"):
                    results.append("%s=%s"%(k,self.neo4jToStr(v)))
        else:
            var = self.mind.workingMemory.getVar(tokens[1])
            if len(tokens)>2:
                results.append(self.neo4jToStr(var,tokens[-1]))
            else:
                results.append(self.neo4jToStr(var))
        self.mind.say("\n".join(results))
    def parseCreateOrFindExpression(self,s,loc,tokens):
        self.mind.memoryWindow.findOrCreate(tokens[1],tokens[2])
    def parseFindExpression(self,s,loc,tokens):
        findType = tokens[1].lower()
        varname = tokens[2]
        condition = tokens[3]
        self.mind.memoryWindow.find(varname,findType,condition)
    def parseCreateExpression(self,s,loc,tokens):
        self.mind.workingMemory.copyVar(tokens[2],tokens[1])
    def parseConnectExpression(self,s,loc,tokens):
        v1 = self.mind.workingMemory.getVar(tokens[1])
        rel = tokens[2]
        v2 = self.mind.workingMemory.getVar(tokens[3])
        
        relname = rel[0]
        if len(rel)>1:
             relprop = rel[1]
        else:
            relprop = {}
        self.mind.workingMemory.createRelation(relname,relprop,v1,v2)
    def parseSetRelExpression(self,s,loc,tokens):
        var1 = self.mind.workingMemory.getVar(tokens[1])
        var2 = self.mind.workingMemory.getVar(tokens[2])
        prop = tokens[3]
        relname = tokens[0]
        self.mind.workingMemory.setRelationProperties(var1,var2,relname,prop)
    def parseSetVarExpression(self,s,loc,tokens):
        var = self.mind.workingMemory.getVar(tokens[0])
        self.mind.workingMemory.setVarProperties(var,tokens[1])
    def parseTimeDefference(self,s,loc,tokens):
        number = tokens[0]
        type = tokens[1][0]
        current = self.mind.bodyWindow.currentTime()
        if type=="M" or type.lower() in ["month"]:
            current = current.addDelta(month = number)
        elif type=="m" or type.lower() in ["minute"]:
            current = current.addDelta(minute = number)
        elif type.lower in ["millisecond","ms"]:
            current = current.addDeltea(msecond = number)
        elif type.lower in ["second","s"]:
            current = current.addDeltea(second = number)
        elif type.lower in ["hour","h"]:
            current = current.addDeltea(hour = number)
        elif type.lower in ["day","d"]:
            current = current.addDeltea(day = number)
        elif type.lower in ["week","w"]:
            current = current.addDeltea(day = number*7)
        elif type.lower in ["month","M"]:
            current = current.addDeltea(month = number)
        elif type.lower in ["year","y"]:
            current = current.addDeltea(year = number)
        self.mind.bodyWindow.setTime(time=current)    
    def parseTimeExact(self,s,loc,tokens):
        #TODO support jalali and hijri
        if len(tokens)==0:
            return
        if tokens[0] == "now":
            t = MDateTime()
            self.mind.bodyWindow.setTime(time=t)
        if tokens[0].lower().startswith("g"):
            dt = MDateTime.create(tokens[1][0],tokens[1][1],tokens[1][2],tokens[1][3],tokens[1][4],tokens[1][5],tokens[1][6])
            self.mind.bodyWindow.setTime(time=dt)
    def parseEventName(self,s,loc,tokens):
        if s.strip().endswith("\""):
            name = tokens[1]
            node = self.mind.memory.createNode(name)
            prop = {"name":name,"type":"Event"}
            self.mind.memory.setNodeProperties(node,prop)
            self.mind.bodyWindow.setEvent(node)
        else:
            varname = tokens[1]
            var = self.mind.workingMemory.getVar(varname)
            created = False
            if var is not None:
                for v in var:
                    if v is not None:
                        prop = {"Type":"Event"}
                        self.mind.memory.setNodeProperties(v,prop)
                        self.mind.bodyWindow.setEvent(v)
                        created = True
            if not created:
                self.mind.error("event var doesn't exists",s)            
    def parsePlaceName(self,s,loc,tokens):
        if s.strip().endswith("\""):
            name = tokens[1]
            node = self.mind.memory.createNode(name)
            prop = {"name":name,"type":"Place"}
            self.mind.memory.setNodeProperties(node,prop)
            self.mind.bodyWindow.setPlace(node)
        else:
            varname = tokens[1]
            var = self.mind.workingMemory.getVar(varname)
            created = False
            if var is not None:
                for v in var:
                    if v is not None:
                        if not v.hasProperty("type"):
                            prop = {"type":"Place"}
                            self.mind.memory.setNodeProperties(v,prop)
                        self.mind.bodyWindow.setPlace(v)
                        created = True
            if not created:
                self.mind.error("event var doesn't exists",s)            
    def parseSpatialExpression(self,s,loc,tokens):
        place = self.mind.bodyWindow.currentPlace()

        op = tokens[1]
        prop = {} if len(tokens)<4 else tokens[-2]
        prop["type"] = op
        
        vars1 = self.mind.workingMemory.getVar(tokens[0][0])
        vars2 = self.mind.workingMemory.getVar(tokens[-1][0])
        with self.mind.memory.db.transaction:
            for var1 in vars1:
                for var2 in vars2:
                    vars = []
                    for var in [var1,var2]:
                        v = self.mind.bodyWindow.instanceOf(var)
                        vars.append(v)
            
                    rel = vars[0].relationships.create("WHERE",vars[1])
                    self.mind.memory.setRelationProperties(rel,prop)
        return [tokens[0][0]]
    def parseSeeExpression(self,s,loc,tokens):
        with self.mind.memory.db.transaction:
            event = self.mind.bodyWindow.currentEvent()
            focusIndex = self.mind.memory.getProperty(event,"focusCount",0)
            for varname in tokens[1:]:
                vars = self.mind.workingMemory.getVar(varname)
                for v in vars:
                    ins = self.mind.bodyWindow.instanceOf(v)
                    event.FOCUS(ins,index=focusIndex)
                    focusIndex += 1
                    event["focusCount"] = focusIndex
    def parseActionExpression(self,s,loc,tokens):
        with self.mind.memory.db.transaction:
            prop = {}
            subject = []
            if type(tokens[-1]) == type({}):
                prop = tokens[-1]
            if len(tokens)==4:
                subject = self.mind.workingMemory.getVar(tokens[1])
                actionname = tokens[2]
            elif len(tokens)==3:
                if type(tokens[-1]) == type({}):
                    actionname = tokens[1]
                else:
                    actionname = tokens[2] 
                    subject = self.mind.workingMemory.getVar(tokens[1])
            elif len(tokens)==2:
                actionname = tokens[1]
            actiontype = self.mind.memory.actionType(subject,actionname)
            for action in actiontype:
                actionvar = self.mind.bodyWindow.instanceOf(action,new = True)
                actionvar.WHEN(self.mind.bodyWindow.currentTimeObj())
                actionvar.EVENT(self.mind.bodyWindow.currentEvent())
                for sbj in subject:
                    actionvar.WHO(sbj)
                self.mind.memory.setNodeProperties(actionvar,prop)
    def parseSearchExpression(self,s,loc,tokens):
        print "search expression:",s.strip(),loc,tokens
            
    def initialParser(self):
        ss = Basket()
        ss.dash            = pp.Literal( "-" )
        ss.lparen          = pp.Literal( "(" )
        ss.rparen          = pp.Literal( ")" )
        ss.dblQ            = pp.Literal("\"")
        ss.singleQ         = pp.Literal("'") 
        ss.dash            = pp.Literal("-")
        ss.dpoint          = pp.Literal(":")
        ss.minuse          = pp.Literal("+")
        ss.plus            = pp.Literal("-")
        ss.dot             = pp.Literal(".")
        ss.comma           = pp.Literal(",")
        ss.semicolon       = pp.Literal(";")
        ss.dollar          = pp.Literal("$")
        ss.space           = pp.Literal(" ")
        ss.question        = pp.Literal("?")
        ss.tajob           = pp.Literal("!")
        ss.lbrkt           = pp.Literal("[")
        ss.rbrkt           = pp.Literal("]")
        ss.dblquestion     = pp.Literal("??")
        ss.equals          = pp.Literal("=")
        ss.A               = pp.Literal("A") | pp.Literal("a")
        ss.NONE            = pp.Literal("NONE")
        ss.bg              = pp.Literal(">")
        ss.lt              = pp.Literal("<")
        ss.AND             = pp.CaselessLiteral("and")
        ss.OR              = pp.CaselessLiteral("or")
        ss.NOT              = pp.CaselessLiteral("not")
        
        ss.caps            = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ss.capsUnderline   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        ss.lowers          = ss.caps.lower()
        ss.integer         = pp.Word(pp.nums)
        ss.timeint         = pp.Combine(pp.Optional(ss.plus | ss.minuse) + ss.integer).setParseAction(self.parseNumber) | ss.question
        
        ss.stringPhrase    = pp.quotedString.setParseAction(self.parseQuotedString)
        ss.number          = pp.Combine(pp.Optional(ss.plus | ss.minuse) + ss.integer + pp.Optional( ss.dot + ss.integer )).setParseAction(self.parseNumber)
        ss.comment         = pp.javaStyleComment.setParseAction(self.parseComment) 
        
        ss.typeName        = pp.Combine(pp.Word(ss.caps,exact=1) + pp.Word(pp.alphas))#("TypeName")#TODO action
        ss.objectName      = pp.Combine(pp.Word(ss.lowers,exact=1) + pp.Optional(pp.Word(pp.alphas)))#("ObjectName")#TODO action
        ss.objectid        = pp.Combine(pp.Literal("`")+ ss.integer + pp.Literal("`"))#.setParseAction(self.parseObjectId)#("ObjectId")
        ss.var             = pp.Combine(pp.Optional(ss.dollar)+pp.Word(pp.alphas+ "_",exact=1) + pp.Optional(pp.Word(pp.alphas + pp.nums + "_"))) | ss.objectid#("VariableName")#TODO action
        
        
        ss.constValue      =  ss.number | ss.stringPhrase | ss.NONE | pp.Group(pp.Suppress(ss.dollar) + ss.var + pp.Suppress(ss.dot) + ss.var).setParseAction(self.parseVarProp) | pp.Group(ss.var).setParseAction(self.parseVarToId) #pp.Word(pp.alphas) |
        ss.nameValue       = pp.Group(pp.Word(pp.alphas) + pp.Suppress(pp.Literal(":")) + ss.constValue)
        ss.dTimeValue      = ss.number +\
                                (pp.CaselessLiteral("millisecond") | pp.CaselessLiteral("ms") |\
                                 pp.CaselessLiteral("second") | pp.CaselessLiteral("s") |\
                                 pp.CaselessLiteral("minute") | pp.Literal("m") |\
                                 pp.CaselessLiteral("hour")   | pp.CaselessLiteral("h") |\
                                 pp.CaselessLiteral("day")    | pp.CaselessLiteral("d") |\
                                 pp.CaselessLiteral("week")   | pp.CaselessLiteral("w") |\
                                 pp.CaselessLiteral("month")  | pp.Literal("M") |\
                                 pp.CaselessLiteral("year")   | pp.CaselessLiteral("y"))
        ss.timeValue       = (pp.CaselessLiteral("Jalali") | pp.CaselessLiteral("J") |\
                                   pp.CaselessLiteral("Hijri") | pp.CaselessLiteral("H") |\
                                   pp.CaselessLiteral("Gregorian") | pp.CaselessLiteral("g") )\
                                   +(ss.timeint + pp.Suppress(ss.dash) + ss.timeint + pp.Suppress(ss.dash) + ss.timeint  \
                                      + ss.timeint + pp.Suppress(ss.dpoint) + ss.timeint + pp.Suppress(ss.dpoint) + ss.timeint + pp.Suppress(ss.dpoint) + ss.timeint ) 
        ss.properties      = pp.Group( pp.Suppress(pp.Literal("{")) + ss.nameValue + pp.ZeroOrMore(pp.Suppress(ss.comma) + ss.nameValue) + pp.Suppress(pp.Literal("}"))).setParseAction(self.parseDict)
        
        
        ss.nameSelectorBase= pp.Group(pp.Combine(pp.Optional(ss.tajob) + (ss.question |  pp.Optional(ss.var))) + pp.Optional(ss.properties))
        ss.nameSelector    = ss.nameSelectorBase + pp.ZeroOrMore(pp.Group((ss.dash|ss.lt|ss.bg) + pp.Optional(ss.nameSelectorBase) + (ss.dash|ss.lt|ss.bg)) + ss.nameSelectorBase)
        
        ss.operator        = pp.Word(pp.alphas) + pp.Optional(ss.properties)
        
        ss.findCondition = pp.Group(pp.Suppress("(") + ss.nameSelector + pp.Suppress(")")) + pp.Optional(pp.CaselessLiteral("as") + ss.var)
        ss.findExpression = pp.CaselessLiteral("find") + \
                    ( pp.CaselessLiteral("when") | pp.CaselessLiteral("where") | pp.CaselessLiteral("who") | pp.CaselessLiteral("the") | pp.CaselessLiteral("only") | pp.CaselessLiteral("someof") | pp.CaselessLiteral("all") | pp.CaselessLiteral("a") | pp.CaselessLiteral("some") )("findType") +\
                    ss.var +\
                    ss.findCondition #+ pp.ZeroOrMore( ss.comma  + ss.findCondition )
                    
        ss.searchExpression = pp.CaselessLiteral("search") + \
                                ss.var + \
                                ss.var + \
                                pp.Group(pp.OneOrMore(ss.var)) + \
                                ss.properties
        
        ss.placeExpression = pp.CaselessLiteral("place") + (ss.var | ss.stringPhrase)
        
        ss.spatialOperation = pp.Forward()
        ss.spatialOperation <<  pp.Suppress("(") + pp.Group(ss.var |  ss.spatialOperation ) + ss.operator + pp.Group(ss.var |  ss.spatialOperation ) + pp.Suppress(")") 
        ss.seeExpression =  pp.CaselessLiteral("see") + ( pp.OneOrMore(ss.var | ss.spatialOperation.setParseAction(self.parseSpatialExpression)))
        
        ss.eventExpression = pp.CaselessLiteral("event") +  (ss.var | ss.stringPhrase)
         
        ss.timeNow = pp.CaselessLiteral("now")
        ss.timeExpression = pp.CaselessLiteral("time") + (ss.timeNow | ss.timeValue | pp.Empty()).setParseAction(self.parseTimeExact) +\
                                                           pp.ZeroOrMore(ss.dTimeValue.setParseAction(self.parseTimeDefference))
        
        ss.actionExpression = pp.CaselessLiteral("action") + ss.var + pp.Optional(ss.var) + pp.Optional( ss.properties )
         
        #TODO: then khali
        ss.thenExpression = pp.CaselessLiteral("then") + pp.OneOrMore(ss.dTimeValue.setParseAction(self.parseTimeDefference))
        
        ss.cypherExpression = pp.CaselessLiteral("cypher") + ss.var + ss.stringPhrase
        
        ss.whatExpression = pp.CaselessLiteral("what") +\
                             pp.Optional(ss.var +\
                                         pp.Optional(pp.Suppress(pp.Literal("["))+ss.integer+pp.Suppress(pp.Literal("]"))) +\
                                         pp.Optional(pp.Combine(ss.dot+ss.var)))
        ss.isExpression   = pp.CaselessLiteral("is") + ss.var
        ss.createExpression = pp.CaselessLiteral("create") + ss.var +\
                                 (  (pp.Optional(ss.var) + ss.properties).setParseAction(self.parseNewNodeFromProperties) |\
                                    (ss.var + (ss.AND | ss.OR | ss.NOT) + ss.var).setParseAction(self.parseVarOper) |\
                                    (ss.var + pp.Suppress(ss.lbrkt) + ss.integer + pp.Suppress(ss.rbrkt)).setParseAction(self.parseVarArray) |\
                                    (ss.var))
        ss.createOrFindExpression = (pp.CaselessLiteral("findOrCreate")|pp.CaselessLiteral("createOrFind")) + ss.var + pp.Group(ss.nameSelector)
        
        ss.connectExpression = pp.CaselessLiteral("connect") + ss.var + pp.Group(ss.var + pp.Optional(ss.properties)) + ss.var
        ss.setExpression = pp.CaselessLiteral("set") + ((ss.var + ss.properties).setParseAction(self.parseSetVarExpression)|\
                                                        (ss.var + pp.Suppress(ss.lparen) + ss.var + pp.Suppress(ss.comma) + ss.var + pp.Suppress(ss.rparen) + ss.properties).setParseAction(self.parseSetRelExpression))
        
        ss.expressions = ss.findExpression.setParseAction(self.parseFindExpression) |\
                         ss.cypherExpression.setParseAction(self.parseCypherExpression) |\
                         ss.whatExpression.setParseAction(self.parseWhatExpression) |\
                         ss.isExpression.setParseAction(self.parseIsExpression) |\
                         ss.createExpression.setParseAction(self.parseCreateExpression) |\
                         ss.createOrFindExpression.setParseAction(self.parseCreateOrFindExpression) |\
                         ss.connectExpression.setParseAction(self.parseConnectExpression) |\
                         ss.setExpression |\
                         ss.eventExpression.setParseAction(self.parseEventName) |\
                         ss.placeExpression.setParseAction(self.parsePlaceName) |\
                         ss.timeExpression |\
                         ss.thenExpression |\
                         ss.searchExpression.setParseAction(self.parseSearchExpression) |\
                         ss.actionExpression.setParseAction(self.parseActionExpression) |\
                         ss.seeExpression.setParseAction(self.parseSeeExpression)
        ss.saying = ss.var + pp.Literal(":") + (ss.findExpression | ss.placeExpression | ss.timeExpression | ss.thenExpression | ss.actionExpression | ss.seeExpression)
        ss.exit = pp.CaselessLiteral("exit")
        ss.line = ss.saying.setParseAction(self.sayingAction) | ss.expressions | ss.exit.setParseAction(self.exitAction)
        self.expression = ss.line
        #phase 1: find what is cypher create connect set findOrCreate
        #phase 2: event place time see
        #phase 3: action then
        #phase 4: saying  search
        
#    def settimeCommand(self,args):
#        #TODO: time +/- time
#        if len(args)==1:
#            #TODO: another argument types
#            if self.argType(args[0]) == ArgType.TimeObject:
#                self.setTime(args[0])
#        return True
#    def setplaceCommand(self,args):
#        if len(args)==1:
#            if self.argType(args[0]) == ArgType.PlaceObject:
#                self.mind.setPlace(args[0])
#        return True
#    def addEventCommand(self,args):
#        return True
#    def addRelationCommand(self,args):
#        return True
#    def declareEventCommand(self,args):
#        return True
#    def commentCommand(self,args):
#        return True
#    def exitCommand(self,args):
#        return False
#            