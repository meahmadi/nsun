function Motor(){}

Motor.prototype = {

    actions : [],//action    senderEvent     senderAction

    init : function(body) {
        this.body = body;
        var self = this;
        this.initView();
    },

    initView : function(){

    },

    call : function(action, senderEvent, senderAction, data){
        //console.log("MOTOR call action "+action+" from "+senderEvent+","+senderAction+":"+data);
        var self = this;
        $.each(self.actions, function(index,value){
            if(value[0].test(action) && value[1].test(senderEvent) && value[2].test(senderAction))
                value[3](self,action, senderEvent, senderAction, data);
        });     
    },

    update : function (){},
    say : function(msg){},
	log : function(msg){},
};
