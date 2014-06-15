with(Motor.prototype){
    actions = [
            //action    senderEvent     senderAction
            [/^$/,      /.*/,       /sleepToggle/,  function(motor){ motor.update() }],
            [/say/,     /.*/,       /.*/,   function(motor,action, senderEvent, senderAction, data){ motor.say(data) }],
			[/log/,     /.*/,       /.*/,   function(motor,action, senderEvent, senderAction, data){ motor.log(data) }],
        ];

    initView = function(){
    	var self = this;
        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/assistant.css" media="screen" />');
        $('body').append('<div id="assistant_container" class="tooltip"><img id="assistant_ico" src="'+static_server_address+'/images/assistant.ico" width="17px"/></div>');
        this.face = $('#assistant_container');

        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/tooltipster.css" media="screen" />');
        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/tooltipster-light.css" media="screen" />');
        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/tooltipster-noir.css" media="screen" />');
        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/tooltipster-punk.css" media="screen" />');
        $("body").prepend('<link rel="stylesheet" type="text/css" href="'+static_server_address+'styles/tooltipster-shadow.css" media="screen" />');
        $.getScript(static_server_address+"/scripts/jquery.tooltipster.min.js",function(){
            self.face.tooltipster({
                animation: 'fade',
                delay: 200,
                timer: 5000,
                theme: 'tooltipster-shadow',
                contentAsHTML: true,
                });
            self.update();
        })
    };

    update = function (){
        if(!this.body.enabled){
            this.face.removeClass('enabled');
            this.say('Zzzzz, Zzzzz,....<br/><font size=-3>click on me to wakeup</font>');
        }else{
            this.face.addClass('enabled');
            this.say('Hello, I see and listen...<br/><font size=-3>click on me to sleep</font>');
        }
    };

	log = function(msg){
		console.log(msg);
	};
    say = function(msg){
        this.face.tooltipster('content',msg);
        this.face.tooltipster('show');
    };
}