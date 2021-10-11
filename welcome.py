import os
import time
import speak_out


project_root_path = os.path.dirname(os.path.abspath(__file__))
welcome_tone_path = ".tones/welcome_tone.wav"
full_tone_path = os.path.join(project_root_path, welcome_tone_path)

welcome_message = "Welcome to eye Glass"
greeting = "Good "
current_hour = time.localtime().tm_hour

if 5 <= current_hour < 12:
    greeting += "morning"
elif 12 <= current_hour < 17:
    greeting += "afternoon"
else:
    greeting += "evening"

welcome_message1 = "please press a button and say a command"
welcome_message2 = "To get help using this device, press a button and say help"

speaker = speak_out.SpeakOut()

try:
    if os.path.exists(full_tone_path):
        os.system(f"aplay {full_tone_path}")
    else:
        pass
    speaker.speak(welcome_message)
    time.sleep(1)
    speaker.speak(greeting)
    time.sleep(1)
    speaker.speak(welcome_message1)
    speaker.speak(welcome_message2)

except:
    print("path does not exist")
