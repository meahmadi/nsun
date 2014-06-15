with(Brain.prototype){
    connections = [//[senderRegex   signalRegex [ [reciever,action] ] ]
            [/face\..*/, /sleepToggle/, [
                    ['brain',   ''],
                    ['sensor',  ''],
                    ['motor',   '']]],

            [/.*\.seen/,        /.*/,       [['brain',  'see']]],
            [/.*\.unseen/,      /.*/,       [['brain',  'unsee']]],

            [/.*\.toAdd/,       /.*/,       [['brain',  'see']]],
            [/.*\.notToAdd/,       /.*/,    [['brain',  'unsee']]],

            [/.*\.focused/,     /.*/,       [['mind',   'attention']]],
            [/.*\.edit/,        /.*/,       [['mind',   'change']]],
            [/.*\.add/,         /.*/,       [['mind',   'add']]],

            [/mind/,            /say/,      [['motor',  'say']]],
			[/mind/,            /log/,      [['motor',  'log']]],
        ];

    actions = [//action    senderEvent     senderAction function(me action, senderEvent, senderAction, data)
            //action    senderEvent     senderAction
            [/^$/,      /.*/,       /sleepToggle/,  function(self){ 
                                                        self.body.enabled = !self.body.enabled;
                                                    }],
            [/see/,     /.*/,       /.*/,           function(self,action, senderEvent, senderAction, data){
                                                        clearTimeout(self.attentionTimeout);
                                                        self.attentionTimeout = setTimeout(function(){
                                                            self.body.mind.call(action,senderEvent,senderAction,data);
                                                        },1000)
                                                    }],
            [/unsee/,   /.*/,       /.*/,           function(self,action, senderEvent, senderAction, data){
                                                        clearTimeout(self.attentionTimeout);
                                                    }],                                             
        ];
}