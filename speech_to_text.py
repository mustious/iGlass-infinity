import speech_recognition as sr
import os

project_root_path = os.path.abspath(os.path.dirname(__file__))
beep_tone_path = os.path.join(project_root_path, ".tones/beep_ping.wav")
google_keys_path = os.environ.get("google_keys_path")

# checks whether the environment variable value is valid and path exists
google_json_path_exists = isinstance(google_keys_path, str) and os.path.exists(google_keys_path)

if google_json_path_exists:
    with open(google_keys_path) as key_json:
        google_key = key_json.read()


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
        adds a beep tone to signify iGlass is waiting for command
        """

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
        response = {"success": None,
                    "error": None}

        self.beep_sound()

        with self.mic as source:
            self.recognise.adjust_for_ambient_noise(source)  # reduces noise
            voice = self.recognise.listen(source)

        try:
            if google_json_path_exists:
                response_google_cloud = self.recognise.recognize_google_cloud(audio_data=voice, credentials_json=google_key)
                response["success"] = response_google_cloud
                return response

            response_google = self.recognise.recognize_google(audio_data=voice)
            response["success"] = response_google
            return response

        except sr.RequestError:
            # network related error
            response["fail"] = "Request error please try again"
            return response

        except sr.UnknownValueError:
            """
            occurs when there is silence in speech
            this returns a None value which is neglected by the Brain instance 
            """
            response["fail"] = "Unknown Value Error"
            return response
