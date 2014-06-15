
find the root1 (ROOT)
create t1 root1 and root
is t1

create now {year:1393, month:3, day:13}
find the jalalical (JALALI_CALENDAR)
connect now ISA jalalical
find all times ($timeroot->?<ISA-!?)
create t1 times and now
is t1

create meisam {name:"meisam ahmadi"}
connect meisam IS me

create birth {name:"birth_event",type:"birth"}
connect birth ISA eventroot

create my_birth {type:"birth"}
connect my_birth PERSON meisam
connect my_birth ISA birth
connect my_birth WHEN now

what
cypher all "start a=node(*) match (a)-[r]->() return a,r"

create nemo Fish{name:"nemo"}
create samenemo Fish

FindOrCreate nemotype $objectroot<IS-!DALGHAKMAHI
connect nemo IS nemotype

set nemo{color:"red"}
set ERTEBAT(nemo,meisam){somevale:10}

event "nahar"

event my_birth
time now

FindOrCreate myHome $objectroot<IS-PLACEROOT<IS-!MyHome
place myHome

see me
see (nemo with{pos:"in hand of"} meisam)

then +3h
action nemo gone
action meisam says {msg:"where is nemo?"}



