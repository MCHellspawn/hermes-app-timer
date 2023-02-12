"""Skill to set a timer."""
import logging
import re
from advtimerjob import AdvTimerJob
from advtimerjobs import AdvTimerJobs
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("TimerApp")

app = HermesApp("TimerApp")
timerList = AdvTimerJobs()

def text_between(a, b, text):
    return min(re.findall(re.escape(a)+"(.*?)"+re.escape(b),text), key=len)

@app.on_intent("AdvTimerStart")
async def adv_timer_start(intent: NluIntent):
    """Advanced Timer Start"""
    _LOGGER.info(f"Intent: {intent.id} | Started: AdvTimerStart")
    global timerList
    
    nameslot = next((slot for slot in intent.slots if slot.slot_name == 'name'), None)
    if nameslot == None:
        _LOGGER.info(f"Intent: {intent.id} | Name slot equals none")
        defTimer = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
        if defTimer == None: 
            timer = AdvTimerJob(timerList, intent, "Timer")
            _LOGGER.debug(f"Intent: {intent.id} | Timer : {timer}")
            _LOGGER.info(f"Intent: {intent.id} | Timer created: {timer.getName()}")
        else:
            _LOGGER.info(f"Intent: {intent.id} | Failed: AdvTimerStart [default timer exists]")
            app.notify(f"a default timer already exists", intent.site_id)
            return EndSession()
    elif len(nameslot.value['value']) == 0:
        _LOGGER.info(f"Intent: {intent.id} | Name slot exists but name is blank")
        extractedTimerName = intent.raw_input.replace("start a new timer for ", "")[:intent.raw_input.replace("start a new timer for", "").find(" for")].strip().lower()
        if len(extractedTimerName) > 0:
            timer = AdvTimerJob(timerList, intent, extractedTimerName)
            _LOGGER.debug(f"Intent: {intent.id} | Timer : {timer}")
            _LOGGER.info(f"Intent: {intent.id} | Timer created: {timer.getName()}")
        else:
            defTimer = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
            if defTimer == None: 
                timer = AdvTimerJob(timerList, intent, "Timer")
                _LOGGER.debug(f"Intent: {intent.id} | Timer : {timer}")
                _LOGGER.info(f"Intent: {intent.id} | Timer created: {timer.getName()}")
            else:
                _LOGGER.info(f"Intent: {intent.id} | Failed: AdvTimerStart [default timer exists]")
                app.notify(f"a default timer already exists", intent.site_id)
                return EndSession()
    else:
        _LOGGER.info(f"Intent: {intent.id} | Name: {str(nameslot.value['value'])} ({str(nameslot.raw_value)})")
        timer = AdvTimerJob(timerList, intent, nameslot.value['value'])
        _LOGGER.debug(f"Intent: {intent.id} | Timer : {timer}")
        _LOGGER.info(f"Intent: {intent.id} | Timer created: {timer.getName()}")

    timerList.addTimer(timer)
    timer.start(app)
    app.notify(timer.getTextStartResponse(), intent.site_id)

    _LOGGER.info(f"Intent: {intent.id} | Completed: AdvTimerStart")
    return EndSession()

@app.on_intent("AdvTimerStop")
async def adv_timer_stop(intent: NluIntent):
    """Advanced Timer Stop"""
    _LOGGER.info(f"Intent: {intent.id} | Started: AdvTimerStop")
    global timerList
   
    nameslot = next((slot for slot in intent.slots if slot.slot_name == 'name'), None)
    if nameslot == None:
        _LOGGER.info(f"Intent: {intent.id} | Name slot equals none")
        defTimer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
        if defTimer == None: 
            sentence = "I couldn't find a default timer"
            _LOGGER.info(f"Intent: {intent.id} | Timer stop failed: AdvTimerStop [no default timer exists]")
        else:
            sentence = defTimer.stop()
            _LOGGER.info(f"Intent: {intent.id} | Timer stopped: {defTimer.getName()}")
            timerList.cleanupTimerList()
            _LOGGER.info(f"Intent: {intent.id} | Timer list cleanup completed")
    elif len(nameslot.value['value']) == 0:
        _LOGGER.info(f"Intent: {intent.id} | Name slot exists but name is blank")
        extractedTimerName = intent.raw_input.replace("stop the timer for ", "")
        if len(extractedTimerName) > 0:
            # We extracted a timer name from the raw text.
            timer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == extractedTimerName), None)
            if timer == None:
                sentence = f"I couldn't find a timer for {extractedTimerName}"
                _LOGGER.info(f"Intent: {intent.id} | Timer stop failed: AdvTimerStop [no timer exists] | Name: {extractedTimerName}")
            else:
                sentence = timer.stop()
                _LOGGER.info(f"Intent: {intent.id} | Timer stopped: {timer.getName()}")
                timerList.cleanupTimerList()
                _LOGGER.info(f"Intent: {intent.id} | Timer list cleanup completed")
        else:
            # We did not extract a timer name from the raw text.
            defTimer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
            if defTimer == None: 
                sentence = "I couldn't find a default timer"
                _LOGGER.info(f"Intent: {intent.id} | Timer stop failed: AdvTimerStop [no default timer exists]")
            else:
                sentence = defTimer.stop()
                _LOGGER.info(f"Intent: {intent.id} | Timer stopped: {defTimer.getName()}")
                timerList.cleanupTimerList()
                _LOGGER.info(f"Intent: {intent.id} | Timer list cleanup completed")
    else:
        # Name slot sent with intent
        _LOGGER.info(f"Intent: {intent.id} | Name: {str(nameslot.value['value'])} ({str(nameslot.raw_value)})")
        timer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == str(nameslot.value['value'])), None)
        if timer == None:
            sentence = f"I couldn't find a timer for {str(nameslot.value['value'])}"
            _LOGGER.info(f"Intent: {intent.id} | Timer stop failed: AdvTimerStop [no timer exists] | Name: {str(nameslot.value['value'])}")
        else:
            sentence = timer.stop()
            _LOGGER.info(f"Intent: {intent.id} | Timer stopped: {timer.getName()}")
            timerList.cleanupTimerList()
            _LOGGER.info(f"Intent: {intent.id} | Timer list cleanup completed")

    _LOGGER.info(f"Intent: {intent.id} | Response: {sentence}")
    app.notify(sentence, intent.site_id)
    _LOGGER.info(f"Intent: {intent.id} | Completed: AdvTimerStop")
    return EndSession(sentence)

@app.on_intent("AdvTimerTimeRemaining")
async def adv_timer_timeremaining(intent: NluIntent):
    """Advanced Timer Time remaining"""
    _LOGGER.info(f"Intent: {intent.id} | Started: AdvTimerTimeRemaining")
    global timerList
    
    sentences = [["remaining time on the","timer"],["how much time is on the","timer"]]
    
    nameslot = next((slot for slot in intent.slots if slot.slot_name == 'name'), None)
    if nameslot == None:
        _LOGGER.info(f"Intent: {intent.id} | Name slot equals none")
        defTimer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
        if defTimer == None: 
            sentence = "I couldn't find a default timer"
            _LOGGER.info(f"Intent: {intent.id} | Timer time remaining failed: AdvTimerTimeRemaining [no default timer exists]")
        else:
            sentence = defTimer.getTimeRemaining()
            _LOGGER.info(f"Intent: {intent.id} | Timer retrieved time remaining: {defTimer.getName()}")
    elif len(nameslot.value['value']) == 0:
        _LOGGER.info(f"Intent: {intent.id} | Name slot exists but name is blank")
        extractedTimerName = text_between(sentences[0][0],sentences[0][1], intent.raw_input).strip()
        # extractedTimerName = intent.raw_input.replace("remaining time on the ", "").replace(" timer", "").strip().lower()
        if len(extractedTimerName) > 0:
            # We extracted a timer name from the raw text.
            timer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == extractedTimerName), None)
            if timer == None:
                sentence = f"I couldn't find a timer for {extractedTimerName}"
                _LOGGER.info(f"Intent: {intent.id} | Timer time remaining failed: AdvTimerTimeRemaining [no timer exists] | Name: {extractedTimerName}")
            else:
                sentence = timer.getTimeRemaining()
                _LOGGER.info(f"Intent: {intent.id} | Timer retrieved time remaining: {timer.getName()}")
        else:
            # We did not extract a timer name from the raw text.
            defTimer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == 'Timer'), None)
            if defTimer == None: 
                sentence = "I couldn't find a default timer"
                _LOGGER.info(f"Intent: {intent.id} | Timer time remaining failed: AdvTimerTimeRemaining [no default timer exists]")
            else:
                sentence = defTimer.getTimeRemaining()
                _LOGGER.info(f"Intent: {intent.id} | Timer retrieved time remaining: {defTimer.getName()}")
    else:
        # Name slot sent with intent
        _LOGGER.info(f"Intent: {intent.id} | Name: {str(nameslot.value['value'])} ({str(nameslot.raw_value)})")
        timer:AdvTimerJob = next((timer for timer in timerList.timers if timer.getName() == str(nameslot.value['value'])), None)
        if timer == None:
            sentence = f"I couldn't find a timer for {str(nameslot.value['value'])}"
            _LOGGER.info(f"Intent: {intent.id} | Timer time remaining failed: AdvTimerTimeRemaining [no timer exists] | Name: {str(nameslot.value['value'])}")
        else:
            sentence = timer.getTimeRemaining()
            _LOGGER.info(f"Intent: {intent.id} | Timer retrieved time remaining: {timer.getName()}")

    _LOGGER.info(f"Intent: {intent.id} | Response: {sentence}")
    app.notify(sentence, intent.site_id)
    _LOGGER.info(f"Intent: {intent.id} | Completed: AdvTimerTimeRemaining")
    return EndSession(sentence)

if __name__ == "__main__":
    _LOGGER.info("Starting Hermes App: AdvTimer")
    app.run()