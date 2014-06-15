import web
import traceback
import webbrowser
from web.contrib import template

import os
import json
from datetime import datetime
		
#from ir.idehgostar.modir.assistant.mind import Mind
from ir.ac.iust.me_ahmadi.multiProcessMind.mind import Mind


render = template.render_genshi(['./templates/'])

urls = (
	'/(.*)', 'Assistant'
)

class MyApplication(web.application):
    def run(self, port=12010, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

app = MyApplication(urls, globals())

outbuffer = []
history = []
def getMindOutput(action,args):
	Assistant.outbuffer.append([action,args])
def flushOutput():
	t = []
	t = Assistant.outbuffer
	Assistant.outbuffer = []
	Assistant.history += t
	return t
		
	
Mind.singleton(getMindOutput)	
	
class Assistant:
	outbuffer = []
	history = []
	def __init__(self):
		pass
	def GET(self,name):
		print "GET "+name
		if not name: 
			return render.index(root="static");
	def OPTIONS(self,args):
		web.header('Access-Control-Allow-Origin', '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		web.header('Access-Control-Allow-Headers','Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')		
	def POST(self,action):
		if not action:
			return '';
		web.header('Access-Control-Allow-Origin',      '*')
		web.header('Access-Control-Allow-Credentials', 'true')
		web.header('Access-Control-Allow-Headers','Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
		data = web.data()

		data_dict = {}
		try:
			data_dict = json.loads(data)	
		except Exception, e:
			print "error parsing json:"+ str(e)
			pass
		
		if action=="message":
			mind = Mind.singleton(getMindOutput)
			try:
				for line in data_dict["body"].splitlines():
					print line
					mind.listen(line)
			except Exception as e:
				print "Error:"+str(e)				
			results = []
			for output in flushOutput():
				results.append({'data': output[1],'action':output[0]})
			return json.dumps(results)
		if action=="update":
			results = []
			for output in flushOutput():
				results.append({'data': output[1],'action':output[0]})
			return json.dumps(results) 			
		else:
			return "[]"


if __name__ == "__main__":
	print "See: localhost:12010 in browser"
	webbrowser.get().open('http://localhost:12010/')
	app.run(port=12010)
