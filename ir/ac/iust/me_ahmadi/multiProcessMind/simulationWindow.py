from thinkWindow import ThinkWindow
import time

class SimulationFrame(ThinkWindow):
    def __init__(self,mind):
        ThinkWindow.__init__(self,mind)
    def run(self):
        while not self.completed:
            time.sleep(1)
	