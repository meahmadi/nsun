NOP=    function(src,event){}
D3ID=   function(src,event){return d3.select(src)[0][0].__data__.id}
D3DATA=   function(src,event){return d3.select(src)[0][0].__data__.data();}

with (Sensor.prototype){
    selectorAlias= {// selectorName: [selector, event]
            'face.shake':       ['#assistant_ico',          'click'],

            'point.seen':       ['image[class~="point"]',   'mouseenter.assistantSensor'],
            'point.unseen':     ['image[class~="point"]',   'mouseleave.assistantSensor'],
            'point.edit':       ['image[class~="point"]',   'dblclicked.assistantSensor'],
            'point.focused':    ['image[class~="point"]',   'click.assistantSensor'],

            'meeting.seen':       ['image[class~="meeting"]',   'mouseenter.assistantSensor'],
            'meeting.unseen':     ['image[class~="meeting"]',   'mouseleave.assistantSensor'],
            'meeting.edit':       ['image[class~="meeting"]',   'dblclicked.assistantSensor'],
            'meeting.focused':    ['image[class~="meeting"]',   'click.assistantSensor'],

            'brace.seen':       ['path[class~="brace"]',   'mouseenter.assistantSensor'],
            'brace.unseen':     ['path[class~="brace"]',   'mouseleave.assistantSensor'],
            'brace.edit':       ['path[class~="brace"]',   'dblclicked.assistantSensor'],
            'brace.focused':    ['path[class~="brace"]',   'click.assistantSensor'],            

            'arrow.seen':       ['path[class~="arrow"]',   'mouseenter.assistantSensor'],
            'arrow.unseen':     ['path[class~="arrow"]',   'mouseleave.assistantSensor'],
            'arrow.edit':       ['path[class~="arrow"]',   'dblclicked.assistantSensor'],
            'arrow.focused':    ['path[class~="arrow"]',   'click.assistantSensor'],                        

            'line.add':        ['#add-taskToRoot-btn',           'click.assistantSensor'],
            'line.add':        ['#ribbon-segment-addSegmentTask','click.assistantSensor'],
            'point.add':       ['#ribbon-addTaskDoc',            'click.assistantSensor'],
            'meeting.add':     ['#ribbon-addMetting',            'click.assistantSensor'],
            'brace.add':       ['#ribbon-add-addBrace',          'click.assistantSensor'],
            'arrow.add':       ['#add-arrowParent-btn',          'click.assistantSensor'],

            'line.toAdd':        ['#add-taskToRoot-btn',           'mouseenter.assistantSensor'],
            'line.toAdd':        ['#ribbon-segment-addSegmentTask','mouseenter.assistantSensor'],
            'point.toAdd':       ['#ribbon-addTaskDoc',            'mouseenter.assistantSensor'],
            'meeting.toAdd':     ['#ribbon-addMetting',            'mouseenter.assistantSensor'],
            'brace.toAdd':       ['#ribbon-add-addBrace',          'mouseenter.assistantSensor'],
            'arrow.toAdd':       ['#add-arrowParent-btn',          'mouseenter.assistantSensor'],

            'line.notToAdd':        ['#add-taskToRoot-btn',           'mouseleave.assistantSensor'],
            'line.notToAdd':        ['#ribbon-segment-addSegmentTask','mouseleave.assistantSensor'],
            'point.notToAdd':       ['#ribbon-addTaskDoc',            'mouseleave.assistantSensor'],
            'meeting.notToAdd':     ['#ribbon-addMetting',            'mouseleave.assistantSensor'],
            'brace.notToAdd':       ['#ribbon-add-addBrace',          'mouseleave.assistantSensor'],
            'arrow.notToAdd':       ['#add-arrowParent-btn',          'mouseleave.assistantSensor'],            
        };
    sens = [
            //selectorName      signalName      convertor   duringSleep fromBody
            ['face.shake',      'sleepToggle',  NOP,    true,    true],

            ['point.seen',      'pointSeen',    D3DATA,   false,    true],
            ['point.unseen',    'pointUnSeen',  D3DATA,   false,    true],
            ['point.edit',      'pointEdit',    D3DATA,   false,    true],
            ['point.focused',   'pointFocused', D3DATA,   false,    true],
            ['point.toAdd',     'pointToAdd',   NOP,      false,    false],            
            ['point.notToAdd',  'pointToAdd',   NOP,      false,    false],
            ['point.add',       'pointAdded',   NOP,      false,    false],

            ['meeting.seen',      'meetingSeen',    D3DATA,   false,    true],
            ['meeting.unseen',    'meetingUnSeen',  D3DATA,   false,    true],
            ['meeting.edit',      'meetingEdit',    D3DATA,   false,    true],
            ['meeting.focused',   'meetingFocused', D3DATA,   false,    true],            
            ['meeting.toAdd',     'meetingToAdd',   NOP,      false,    false],
            ['meeting.notToAdd',  'meetingToAdd',   NOP,      false,    false],
            ['meeting.add',       'meetingAdded',   NOP,      false,    false],

            ['brace.seen',      'braceSeen',    D3DATA,   false,    true],
            ['brace.unseen',    'braceUnSeen',  D3DATA,   false,    true],
            ['brace.edit',      'braceEdit',    D3DATA,   false,    true],
            ['brace.focused',   'braceFocused', D3DATA,   false,    true],
            ['brace.toAdd',     'braceToAdd',   NOP,      false,    false],
            ['brace.notToAdd',  'braceToAdd',   NOP,      false,    false],
            ['brace.add',       'braceAdded',   NOP,      false,    false],

            ['arrow.seen',      'arrowSeen',    D3DATA,   false,    true],
            ['arrow.unseen',    'arrowUnSeen',  D3DATA,   false,    true],
            ['arrow.edit',      'arrowEdit',    D3DATA,   false,    true],
            ['arrow.focused',   'arrowFocused', D3DATA,   false,    true],
            ['arrow.toAdd',     'arrowToAdd',   NOP,      false,    false],
            ['arrow.notToAdd',  'arrowToAdd',   NOP,      false,    false],
            ['arrow.add',       'arrowAdded',   NOP,      false,    false],

            ['line.toAdd',      'lineToAdd',    NOP,    false,    false],
            ['line.notToAdd',   'lineToAdd',    NOP,    false,    false],
            ['line.add',        'lineAdded',    NOP,    false,    false],

        ];
        
    actions = [
            //action    senderEvent     senderAction
            [/^$/,      /.*/,       /sleepToggle/,  function(sensor){
                                                        if(sensor.body.enabled) 
                                                            sensor.enable(); 
                                                        else sensor.disable();}]
        ];
}