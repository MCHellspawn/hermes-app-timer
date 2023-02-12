import re

def text_between(a, b, text):
    return min(re.findall(re.escape(a)+"(.*?)"+re.escape(b),text), key=len)

input = "remaining time on the potatoes timer"

sentences = [["remaining time on the","timer"],["how much time is on the","timer"]]
extractedTimerName = None

extractedTimerName = text_between(sentences[0][0],sentences[0][1], input).strip()

print(extractedTimerName)
