import os
import time
import random
import speak_out

good_night_greetings = ["Have a good rest", "Sleep well Champ!"]
good_day_greetings = ["Have a great day"]

project_root_path = os.path.dirname(os.path.abspath(__file__))
goodbye_tone_path = ".tones/goodbye.wav"
full_goodbye_tone_path = os.path.join(project_root_path, goodbye_tone_path)
print(full_goodbye_tone_path)
current_time = time.localtime().tm_hour

if current_time > 20 or current_time < 5:
    greeting = random.choice(good_night_greetings)
else:
    greeting = random.choice(good_day_greetings)

speaker = speak_out.SpeakOut()

try:
    speaker.speak("Good night")
    time.sleep(0.5)
    speaker.speak(greeting)

    if os.path.exists(full_goodbye_tone_path):
        os.system(f"aplay {full_goodbye_tone_path}")
    else:
        pass

except:
    print("path does not exist")

#os.system("sudo shutdown down")
