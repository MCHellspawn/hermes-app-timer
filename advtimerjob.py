import threading
import time
from typing import Optional
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import HermesApp

class AdvTimerJob(object):
    intent = None
    name = None    
    secondsSlot = None
    minutesSlot = None
    hoursSlot = None
    secondsExist = False
    minutesExist = False
    hoursExist = False
    seconds = 0
    minutes = 0
    hours = 0
    textSeconds = None
    textMinutes = None
    textHours = None
    textTime = None
    textStartResponse = None
    textCompleteResponse = None
    textFailResponse = None
    expired = False
    timer = None
    start_time = None
    time_range = 0

    def __init__(self, parent, intent: NluIntent, name: Optional[str] = None): 
        self.parent = parent
        self.intent = intent
        if name is None:
            self.name = "Timer" #default timer name
        else:
            self.name = name
        self.secondsSlot = next((slot for slot in intent.slots if slot.slot_name == 'seconds'), None)
        if self.secondsSlot is not None:
            self.secondsExist = True
            self.seconds = self.secondsSlot.value['value']
        self.minutesSlot = next((slot for slot in intent.slots if slot.slot_name == 'minutes'), None)
        if self.minutesSlot is not None:
            self.minutesExist = True
            self.minutes = self.minutesSlot.value['value']
        self.hoursSlot = next((slot for slot in intent.slots if slot.slot_name == 'hours'), None)
        if self.hoursSlot is not None:
            self.hoursExist = True
            self.hours = self.hoursSlot.value['value']
        self.time_range = self.seconds + self.minutes * 60 + self.hours * 3600
        self.initText()
        
    def initText(self):
        if self.secondsExist:
            if self.secondsSlot.raw_value == "one":
                self.textSeconds = "one second"
            else:
                self.textSeconds = self.secondsSlot.raw_value + " seconds"
        if self.minutesExist:
            if (self.minutesSlot.raw_value == "one"):
                self.textMinutes = "one minute"
            else:
                self.textMinutes = self.minutesSlot.raw_value + " minutes"
        if self.hoursExist:
            if (self.hoursSlot.raw_value == "one"):
                self.textHours = "one hour"
            else:
                self.textHours = self.hoursSlot.raw_value + " hours"

        if self.secondsExist and (not self.minutesExist) and (not self.hoursExist):
            self.textTime = f"{self.textSeconds}"
        elif self.secondsExist and self.minutesExist and (not self.hoursExist):
            self.textTime = f"{self.textMinutes} and {self.textSeconds}"
        elif (not self.secondsExist) and self.minutesExist and (not self.hoursExist):
            self.textTime = f"{self.textMinutes}"
        elif not self.minutesExist and (not self.secondsExist):
            self.textTime = f"{self.textHours}"
        elif (not self.minutesExist) and self.secondsExist and self.hoursExist:
            self.textTime = f"{self.textHours} and {self.textSeconds}"
        elif (not self.secondsExist) and self.minutesExist and self.hoursExist:
            self.textTime = f"{self.textHours} and {self.textMinutes}"
        elif self.secondsExist and self.minutesExist and self.hoursExist:
            self.textTime = f"{self.textHours} and {self.textMinutes} and {self.textSeconds}"

        if self.name != "Timer":
            self.textStartResponse =  f"Timer for {self.name} set for {self.textTime}"
            self.textCompleteResponse = f"Timer for {self.name} has completed"
        else:
            self.textStartResponse =  f"Timer set for {self.textTime}"
            self.textCompleteResponse = f"The timer has completed"

    def buildText(self, seconds:int = None, minutes:int = None, hours:int = None):
        s = False
        m = False
        h = False
        
        if seconds is None:
            s = True
        if minutes is None:
            m = True
        if hours is None:
            h = True

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

        if s and (not m) and (not h):
            self.textTime = f"{seconds}"
        elif s and m and (not h):
            self.textTime = f"{minutes} and {seconds}"
        elif (not s) and m and (not h):
            self.textTime = f"{minutes}"
        elif not m and (not s):
            self.textTime = f"{hours}"
        elif (not m) and s and h:
            self.textTime = f"{hours} and {seconds}"
        elif (not s) and m and h:
            self.textTime = f"{hours} and {minutes}"
        elif s and m and h:
            self.textTime = f"{hours} and {minutes} and {seconds}"

        if self.name != "Timer":
            self.textStartResponse =  f"Timer for {self.name} set for {self.textTime}"
        else:
            self.textStartResponse =  f"Timer set for {self.textTime}"
  
    def notify(self, app:HermesApp):
        if self.name != "Timer":
            response = f"the {self.name} timer has ended"
        else:
            response = f"the timer has ended"
        self.expired = True
        app.notify(response, self.intent.site_id)
        self.parent.cleanupTimerList()
 
    def getSeconds(self):
        return self.seconds

    def getMinutes(self):
        return self.minutes

    def getHours(self):
        return self.hours

    def getTimeRemaining(self):
        if self.timer == None:
            return f"The {self.name} timer is no set"
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
        return sentence

    def getName(self):
        return self.name
    
    def setName(self, name: str):
        self.name = name
        return self.name

    def setTextTime(self, text: str):
        self.textTime = text
        return self.textTime
    
    def getTextTime(self):
        return self.textTime

    def setTextStartResponse(self, text: str):
        self.textStartResponse = text
        return self.textStartResponse
    
    def getTextStartResponse(self):
        return self.textStartResponse

    def setTextCompleteResponse(self, text: str):
        self.textCompleteResponse = text
        return self.textTimtextCompleteResponsee
    
    def getTextCompleteResponse(self):
        return self.textTextCompleteResponseme
 
    def setTextFailResponse(self, text: str):
        self.textTime = text
        return self.textTime
    
    def getTextFailResponse(self):
        return self.textTime

    def start(self, app:HermesApp):
        timer = threading.Timer(self.time_range, self.notify,[app])
        self.start_time = time.time()
        self.timer = timer
        timer.start()
    
    def stop(self):
        """
        Stops the timer. Sets start_time to 0, time
        _range = 0, and expried = true.

        returns str = sentence to return to the end user confirming timer stop
        """
        self.timer.cancel()
        self.timer = None
        self.start_time = 0
        self.time_range = 0
        self.expired = True
        if self.name == "Timer":
            return "The timer has been stopped"
        else:
            return f"The {self.name} timer has been stopped"
        
