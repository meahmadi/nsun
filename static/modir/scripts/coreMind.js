function Mind(){}

Mind.prototype = {
    mindServerAddress : "http://localhost:12010/",

	init : function(body){
		this.body = body;
	},

	call : function(action, senderEvent, senderAction, data){
		console.log("MIND: call action "+action+" from "+senderEvent+","+senderAction+":"+data);
	},

	decision : function(data){
		console.log("MIND: decision recieved "+data)
	},
	
    sendMind : function(_type,_data){
        var self = this;
        //console.log("sending data to mind...:"+_type +" : "+_data);
        $.ajax({
            type : "POST",
            async : true,
            url : self.mindServerAddress +  _type,
            dataType : "json",
            data : JSON.stringify(_data),
            crossDomain: true,
            success: function(data){
            	self.decision(data);
            }
        });
    },	
}
