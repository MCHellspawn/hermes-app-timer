"""Skill to tell set a timer."""
import threading
import time
import logging
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("TimerApp")

app = HermesApp("TimerApp")

t = None

class TimerJob(object):
    answer  = u"your timer has ended"
    intent = None
    timer = None
    start_time = None
    time_range = 0

    def __init__(self, intent): 
        self.intent = intent

    def buildSentence(self):
        seconds = self.getSeconds()[1]
        minutes = self.getMinutes()[1]
        hours = self.getHours()[1]

        s = len(seconds)>1
        m = len(minutes)>1
        h = len(hours)>1

        if(seconds == "one"):
            seconds = "one second"
        else:
            seconds = seconds + " seconds"
        if(minutes == "one"):
            minutes = "one minute"
        else:
            minutes = minutes + " minutes"
        if(hours == "one"):
            hours = "one hour"
        else:
            hours = hours + " hours"
        
        sentence = ""

        if s and (not m) and (not h):
            sentence =  "Timer set for " + seconds

        elif s and m and (not h):
            sentence =  "Timer set for " + minutes + " and " + seconds

        elif (not s) and m and (not h):
            sentence =  "Timer set for " + minutes
            
        elif not m and (not s):
            sentence =  "Timer set for " + hours

        elif (not m) and s and h:
            sentence =  "Timer set for " + hours + " and " + seconds
            
        elif (not s) and m and h:
            sentence =  "Timer set for " + hours + " and " + minutes

        elif s and m and h:
            sentence =  "Timer set for " + hours + " and " + minutes + " and " + seconds
        
        _LOGGER.info(sentence)
        app.notify(sentence, self.intent.site_id)
        self.timer = None
        self.start_time = 0

    def notify(self):
        #print(self.answer)
        app.notify(self.answer, self.intent.site_id)
 
    def getSeconds(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'seconds':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def getMinutes(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'minutes':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def getHours(self):
        for slot in self.intent.slots:
            if slot.slot_name == 'hours':
                return [slot.value['value'], slot.raw_value]
        return [0, ""]

    def start(self):
        seconds = self.getSeconds()[0]
        minutes = self.getMinutes()[0]
        hours   = self.getHours()[0]
        self.time_range = seconds + minutes * 60 + hours * 3600
        _LOGGER.info("start Timer: " + str(self.time_range))
        timer = threading.Timer(self.time_range, self.notify)
        self.buildSentence()
        self.start_time = time.time()
        self.timer = timer
        timer.start()
    
    def stop(self):
        global t
        self.timer.cancel()
        self.timer = None
        self.start_time = 0
        self.time_range = 0
        t = None
        _LOGGER.info("Stop timer")
        return "The timer has been stopped"

    def timeRemaining(self):
        if self.timer == None:
            return "No timer set"
        timePassed = time.time() - self.start_time
        timeDiff = self.time_range - int(timePassed)
        m, s = divmod(timeDiff, 60)
        h, m = divmod(m, 60)
        if(h > 0):
            sentence = "There are " + str(int(h)) + " hours, " + str(int(m)) + " minutes and " + str(int(s)) + " seconds remaining on the timer"
        elif(m > 0):
            sentence = "There are " + str(int(m)) + " minutes and " + str(int(s)) + " seconds  remaining on the timer"
        elif(s > 0):
            sentence = "There are " + str(int(s)) + " seconds remaining on the timer"
        _LOGGER.info(sentence)
        return sentence

@app.on_intent("TimerStart")
async def timer(intent: NluIntent):
    global t
    if t != None:
        app.notify("Existing timer has been stopped", intent.site_id)
        t.stop()
    t = TimerJob(intent)
    t.start()

    """Timer"""
    return EndSession()

@app.on_intent("TimerTimeRemaining")
async def timer(intent: NluIntent):
    """Time remaining"""
    global t
    if t == None:
        return EndSession("No timer set")
    else:
        return EndSession(t.timeRemaining())

@app.on_intent("TimerStop")
async def timer(intent: NluIntent):
    """stop Timer"""
    global t
    if t == None:
        return EndSession("No timer set")
    else:
        return EndSession(t.stop())

if __name__ == "__main__":
    t = None
    app.run()
