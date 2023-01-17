from urllib.error import URLError
import urllib.request
import json
import time
import ssl
import math
import pyttsx3
import time

# set ssl context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# set up text-to-speech
engine = pyttsx3.init()
engine.say("Text-to-speech started")
engine.runAndWait()

# set up gold thresholds
last_threshold = 0
thresholds = range(10000,0,-500)
reminder_active = False

# print thresholds config
print("Thresholds:", end="")
for threshold in thresholds:
    print(", "+str(threshold), end="")
print("")

# set up status announcements
status = "Disconnected"

# main loop
while True:
    try:
        # get current gold
        with urllib.request.urlopen('https://127.0.0.1:2999/liveclientdata/activeplayer', context=ctx) as f:
            if status != "Connected":
                status = "Connected"
                engine.say(status)
                engine.runAndWait()
            data = json.load(f)
            current_gold = math.floor(data["currentGold"])
            print(current_gold)

            # if gold is less than the last threshold, reset
            if current_gold < last_threshold:
                last_threshold = 0
                reminder_active = False
            
            # if a reminder is due, play it
            try:
                reminder_frequency = 20000/(current_gold+1)
                if reminder_active and time.time() - last_reminder_time > reminder_frequency:
                    engine.say(last_threshold)
                    engine.runAndWait()
                    last_reminder_time = time.time()
            except NameError:
                pass
            
            # check for gold passed threshold
            for threshold in thresholds:
                if current_gold >= threshold:
                    if threshold > last_threshold:
                            print("Gold went over threshold: "+str(threshold))
                            engine.say(threshold)
                            engine.runAndWait()
                            last_reminder_time = time.time()
                            reminder_active = True                            
                            last_threshold = threshold
                            break
        
        # print info about next reminder
        if "last_reminder_time" in locals():
            print("Time since last reminder: "+str(math.floor(time.time() - last_reminder_time)))
            print("Time until next reminder: "+str(math.floor(last_reminder_time + reminder_frequency - time.time()))
        
        time.sleep(1)

    # catch error if not in game
    except URLError as e:
        if status == "Connected":
            status = "Disconnected"
            engine.say(status)
            engine.runAndWait()        
        print("Unable to find game, reconnecting...")
        time.sleep(10)
    


