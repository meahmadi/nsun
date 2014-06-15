findorcreate quranbook $objectroot<IS-!QuranBook
findorcreate concept $objectroot<IS-QuranConcept

findorcreate sure $quranbook<IS-Sure<IS-!Yousof{number:12}
findorcreate aye $quranbook<IS-Aye<IS-!?{sure:$sure, aye:1}

connect aye WHERE{type:"in"} sure

place aye

create word Word{text:"الم"}
see (word in aye)
findorcreate horofmoghata $quranbook<IS-!QuranHoroofMoqata
connect word IS HoroofMoqata

then +1s
create ebarat Ebarat{text:"تلک آیات الکتاب المبین"}
see ((ebarat after word) in aye)
findorcreate ketab_concept $concept<IS-!Ketab{text:"کتاب"}
findorcreate alketabalmobin_concept $concept<IS-!AlKetabAlMobin{text:"الکتاب المبین"}
connect alketabalmobin_concept CONCEPTUAL_IS ketab_concept
findorcreate aye_concept $concept<IS-Aye{text:"آیه"}

findorcreate ayatalketabalmobin $aye_concept{text:"آیات الکتاب المبین"}
connect ayatalketabalmobin CONCEPTUAL_FOR alketabalmobin_concept
connect ebarat CONTAINS ayatalketabalmobin
see ayatalketabalmobin

findorcreate aye $quranbook<IS-Aye<IS-!?{sure:$sure, aye:2}
connect aye WHERE{type:"in"} sure

place aye

findorcreate God $concept<IS-!{text:"الله"}
findorcreate Enna $concept<IS-!{text:"انا"}
findorcreate AhlBeit $concept <IS-!{text:"اهل بیت"}

connect Enna CONCEPTUAL_IS God
connect Enna CONCEPTUAL_IS AhlBeit

findorcreate Quran $concept<IS-!Quran{text:"قرآن"}
findorcreate QuranArabi $Quran<IS-!QuranArabi{text:"قرآنا عربیا"}
findorcreate mokhatab $concept<IS-!Mokhatab
see Enna
see QuranArabi
action Enna nazel{target:$QuranArabi}
then +1s
action mokhatab taghol{probability:1}
