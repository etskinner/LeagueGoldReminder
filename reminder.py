import requests
import time
import math
import pyttsx3
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# set ssl context
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# set up text-to-speech
engine = pyttsx3.init()


def say(text):
    engine.say(text)
    engine.runAndWait()


say("Text-to-speech started")

# set up gold thresholds
last_threshold = 0
thresholds = range(10000, 0, -500)
reminder_active = False

# print thresholds config
print("Thresholds:", end="")
for threshold in thresholds:
    print(", " + str(threshold), end="")
print("")

# set up status announcements
status = "Disconnected"

# main loop
while True:
    try:

        # get current gold
        r = requests.get(
            "https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False
        )

        if r.status_code == 200:
            if status != "Connected":
                status = "Connected"
                say(status)
            data = r.json()
            current_gold = math.floor(data["currentGold"])
            # print(current_gold)

            # if gold is less than the last threshold, reset
            if current_gold < last_threshold:
                print(
                    "Gold went lower than last threshold: "
                    + str(threshold)
                    + " -> "
                    + str(current_gold)
                )
                last_threshold = 0
                reminder_active = False

            # if a reminder is due, play it
            try:
                reminder_frequency = 20000 / (current_gold + 1)
                if (
                    reminder_active
                    and time.time() - last_reminder_time > reminder_frequency
                ):
                    say(last_threshold)
                    last_reminder_time = time.time()
            except NameError:
                pass

            # check for gold passed threshold
            for threshold in thresholds:
                if current_gold >= threshold:
                    if threshold > last_threshold:
                        print("Gold went over threshold: " + str(threshold))
                        engine.say(threshold)
                        engine.runAndWait()
                        last_reminder_time = time.time()
                        reminder_active = True
                        last_threshold = threshold
                        break

        # if disconnected, say so
        else:
            if status != "Disconnected":
                status = "Disconnected"
                say(status)

        # # print info about next reminder
        # if "last_reminder_time" in locals():
        #     print("Time since last reminder: "+str(math.floor(time.time() - last_reminder_time)))
        #     print("Time until next reminder: "+str(math.floor(last_reminder_time + reminder_frequency - time.time())))

        # wait a bit to prevent DOSing
        time.sleep(1)

    # if disconnected, say so
    except requests.exceptions.ConnectionError:
        if status != "Disconnected":
            status = "Disconnected"
            say(status)
