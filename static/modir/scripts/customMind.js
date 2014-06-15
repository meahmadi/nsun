function getRandomVarName(){
	return "tv"+Math.floor(Math.random()*10000)+""+Date.now()
}
with (Mind.prototype){
	mindServerAddress = "http://localhost:12010/";
	call = function(action, senderEvent, senderAction, data){
		console.log("MIND call: "+action+" from "+senderEvent+","+senderAction+":"+data);
		msg = "";
		switch(action){
			case "see":
				if ( /.*ToAdd$/.test(senderAction)){

				}else if (/.*Seen$/.test(senderAction)){
					sourcetype = senderEvent.split(".")[0];
					msg += "time now\n";

					objtype = getRandomVarName();
					msg += "findOrCreate "+objtype+" $objectroot<IS-!"+sourcetype +"\n";
					objvar = getRandomVarName();
					msg += "findOrCreate "+objvar+" $"+objtype+"<IS-!?{objid:"+data.id+",title:\""+data.title+"\"}\n";

					place = [];
					placeVars = [];
					parentPlace = undefined;
					if (sourcetype=="point"){
						parentPlace = data.getTask();
					}

					taskvar = getRandomVarName();
					msg += "findOrCreate "+taskvar+" $objectroot<IS-!task \n";

					while((parentPlace!=undefined)&&(parentPlace instanceof Task)){
						console.log(parentPlace);
						place.push(parentPlace);

						placevar = getRandomVarName();
						msg += "findOrCreate "+placevar+" $"+taskvar+"<IS-!{objid:"+parentPlace.id+",title:\""+parentPlace.title+"\"} \n";
						placeVars.push(placevar);

						parentPlace = parentPlace.getParent();
					}
					if(place.length>0){
						msg += "place "+placeVars[0]+"\n";
						msg += "see ";
						for(var i=0;i<placeVars.length;i++){
							if(i<placeVars.length-1){
								msg += "(" + placeVars[i] + " in ";
							}else{
								msg += placeVars[i];
								for(var j=0; j<placeVars.length-1;j++)
									msg += ")";
								msg += "\n";
							}
						}
					}
					msg += "see " + objvar + "\n";
					console.log(msg);
				}
				break;
			case "change":
				console.log("change "+data.title);
				break;
			case "attention":
				console.log("attention on "+data.title);
				break;
			case "add":
				console.log("add "+ senderAction);
				break;
			default:
				console.log("another action:"+senderAction);
		}
		this.sendMind("message",{"body":msg});
	};

	decision = function(data){
		for(var i=0;i<data.length;i++){
			this.body.brain.signal('mind',data[i].action,data[i].data);
		}
	}
}