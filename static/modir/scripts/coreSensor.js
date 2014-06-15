function Sensor(){}

Sensor.prototype = {

    selectorAlias: {// selectorName: [selector, event]
    },

    sens : [//[selectorName      signalName      convertor   duringSleep    fromBody]
    ],
    actions : [//action    senderEvent     senderAction, function(me action, senderEvent, senderAction, data)
    ],

    init : function(body){
        this.body = body;

        this.enable(true);
        if(this.body.enable)
            this.enable();
        else
            this.disable();
    },

    call : function(action, senderEvent, senderAction, data){
        //console.log("SENSOR: call action "+action+" from "+senderEvent+","+senderAction+":"+data);
        var self = this;
        $.each(self.actions, function(index,value){
            if(value[0].test(action) && value[1].test(senderEvent) && value[2].test(senderAction))
                value[3](self,action, senderEvent, senderAction, data);
        });     
    },

    enable : function(initial) {
        var initial = typeof initial == 'undefined' ? false : initial;
        var self = this;
        $.each(this.sens, function(index, value){
            var selectorName = value[0];
            var signalName = value[1];
            var convertor = value[2]
            var fromBody = value[4]
            var selector = self.selectorAlias[selectorName]
            if((initial && value[3]) || (!initial && !value[3]) ){
                // console.log("SENSOR: adding listener on "+selector[0]+":"+selector[1]+" fromBody?"+fromBody);
                if(fromBody){
                    $("body").on(selector[1],selector[0],function(e){
                        // console.log("SENSOR event: fromBody "+selectorName+":"+signalName);
                        self.body.brain.signal(selectorName,signalName,(convertor)(this,e));
                    });
                }else{
                    $(selector[0]).on(selector[1],function(e){
                        // console.log("SENSOR event:"+selectorName+":"+signalName);
                       self.body.brain.signal(selectorName,signalName,(convertor)(this,e)); 
                    });
                }
            }
        });
    },

    disable : function(){
        var self = this;
        $.each(this.sens, function(index, value){
            var selectorName = value[0];
            var signalName = value[1];
            var fromBody = value[4]
            var selector = self.selectorAlias[selectorName]
            if(!value[3]){
                if(fromBody)
                    $("body").off(selector[1],selector[0]);             
                else
                    $(selector[0]).off(selector[1]);             
            }
        });
    }
};
