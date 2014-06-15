function Assistant(){}

Assistant.prototype = { 
    init : function (){
        this.enabled = false;
        self = this;

        $.getScript(static_server_address+"scripts/coreBrain.js",function(){
            $.getScript(static_server_address+"scripts/customBrain.js",function(){
                self.brain = new Brain();
                self.brain.init(self);
            });
        });

        $.getScript(static_server_address+"scripts/coreMind.js",function(){
            $.getScript(static_server_address+"scripts/customMind.js",function(){
                self.mind = new Mind();
                self.mind.init(self);
            });
        });

        $.getScript(static_server_address+"scripts/coreMotor.js",function(){
            $.getScript(static_server_address+"scripts/customMotor.js",function(){
                self.motor = new Motor();
                self.motor.init(self);
            });
        });

        $.getScript(static_server_address+"scripts/coreSensor.js",function(){
            $.getScript(static_server_address+"scripts/customsensor.js", function(){
                self.sensor = new Sensor();
                self.sensor.init(self);
            });
        });
    },

};

window.assistant = new Assistant();
window.assistant.init();
