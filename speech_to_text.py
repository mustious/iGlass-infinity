import speech_recognition as sr
import os

project_root_path = os.path.abspath(os.path.dirname(__file__))


class SpeechRecognizer:
    """
    This module triggers the microphone to accept speech then uses the google api to transcribe it
    if google api is not available it uses the wit.ai api

    :ivar recognise: instance of the Recognizer() class from the speech-recognition library
    :ivar mic: instance of the Microphone() class
    """

    def __init__(self):
        self.recognise = sr.Recognizer()
        self.mic = sr.Microphone()

    def beep_sound(self):
        """
        adds a beep tone to signify iGlass is waiting a command
        """

        beep_tone_path = os.path.join(project_root_path, ".tones/beep_ping.wav")
        try:
            if os.path.exists(beep_tone_path):
                os.system(f"aplay {beep_tone_path}")
        except:
            pass

    def listen(self):
        """
        triggers the mic, coverts audio to text

        :var response_google: text string from google cloud speech-to-text
        :return: response
        :rtype dict
        """
        response = {"successful": None,
                    "failure": None}

        self.beep_sound()

        with self.mic as source:
            self.recognise.adjust_for_ambient_noise(source)  # reduces noise
            voice = self.recognise.listen(source)

        try:
            response_google = self.recognise.recognize_google(audio_data=voice)
            response["successful"] = response_google
            return response

        except sr.RequestError:
            # network related error
            response["failure"] = "Request error please try again"
            return response

        except sr.UnknownValueError:
            """
            occurs when there is silence in speech
            this returns a None value which is neglected by the Brain instance 
            """
            # response["failure"] = "Unknown Value Error"
            return response
