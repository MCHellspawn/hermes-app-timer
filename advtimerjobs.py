import advtimerjob

class AdvTimerJobs(object):
    timers = []
    
    def __init__(self): 
        self.timers = []

    def addTimer(self, timer: advtimerjob.AdvTimerJob):
        self.timers.append(timer)

    def removeTimer(self, timer: advtimerjob.AdvTimerJob):
        timerCheck = next((timer for timer in self.timers if timer == timer), None)
        if timerCheck != None:
            self.timers.remove(timer)
            return True
        else:
            return False

    def removeTimerByName(self, name: str):
        timer = next((timer for timer in self.timers if timer.name == name), None)
        if timer != None:
            self.timers.remove(timer)
            return True
        else:
            return False

    def getTimerByName(self, name: str):
        timer = next((timer for timer in self.timers if timer.name == name), None)
        return timer

    def cleanupTimerList(self):
        for timer in self.timers:
            if timer.expired:
                self.timers.remove(timer)
