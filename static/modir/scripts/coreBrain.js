

function Brain(){}

Brain.prototype = {
    connections : [//[senderRegex   signalRegex [ [reciever,action] ] ]
    ],

    actions : [//action    senderEvent     senderAction function(me action, senderEvent, senderAction, data)
    ],

    init : function(body){
        this.body = body;
        this.attentionTimeout = 0;
    },


    signal : function(senderEvent,action,data){
        // console.log("BRAIN: Signal From "+senderEvent+","+action+":"+data);
        var self = this;
        $.each(self.connections, function(index,value){
            if(value[0].test(senderEvent) && value[1].test(action)){
                $.each(value[2], function(i,v){
                    self.body[v[0]].call(v[1],senderEvent,action,data);
                });
            }
        });
    },

    call : function(action, senderEvent, senderAction, data){
        // console.log("BRAIN: call action "+action+" from "+senderEvent+","+senderAction+":"+data);
        var self = this;
        $.each(self.actions, function(index,value){
            if(value[0].test(action) && value[1].test(senderEvent) && value[2].test(senderAction))
                value[3](self,action, senderEvent, senderAction, data);
        });
    },

};