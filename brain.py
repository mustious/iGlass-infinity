import gpiozero
import time
import threading
import multiprocessing

import iglass_vision
from bot import DialogflowBot
from speak_out import SpeakOut
from speech_to_text import SpeechRecognizer

button = gpiozero.Button(17)  # respeaker 2-mics button

iglass_project_id = "musty-1563232769915"
iglass_bot = DialogflowBot(iglass_project_id)

speaker = SpeakOut()
speech_recognizer = SpeechRecognizer()

iglass_vision_keywords = ["OCR", "object-recognition"]  # keywords to trigger Cloud Vision API


def time_counter(secs=3):
    time.sleep(secs)


def button_counter():
    global button_count
    global stop_threads

    while True:
        if stop_threads:
            break
        button_state = button.value
        print(button_state)
        if button_state == 1:
            button_count += 1
        time.sleep(0.3)


for _ in range(1):
    stop_threads = False

    button_count = 0
    time_thread = threading.Thread(target=time_counter, args=(3,))
    counter_thread = threading.Thread(target=button_counter)

    threads = [time_thread, counter_thread]

    time_thread.start()
    counter_thread.start()

    time.sleep(3)
    if not time_thread.is_alive():
        stop_threads = True

    if button_count == 0:
        # no action if no button press
        continue
    elif button_count == 1:
        # activate voice recognition on one button press

        recognizer_response = speech_recognizer.listen()
        if recognizer_response["success"]:
            input_sentence = recognizer_response["success"]
        else:
            break
        if input_sentence in ["exit", "X"]:
            break
        print(f"You: {input_sentence}")
        bot_response = iglass_bot.chat_response(input_sentence)

        if bot_response in iglass_vision_keywords:
            pass
        print(f"iGlassBot: {bot_response}")
        speaker.speak(bot_response)

    elif button_count == 2:
        # perform OCR on two button presses
        ocr_result = iglass_vision.iglass_vision_response("OCR")
        speaker.speak(ocr_result)


