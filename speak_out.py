import pyttsx3
import os

project_root_path = os.path.dirname(os.path.abspath(__file__))


class SpeakOut:
    """
    reads out the text passed to it using android pico2wave as default TTS and pytttsx3

    :param engine: creates an Engine instance from pyttsx3
    """

    def __init__(self, rate: int = 200, volume: float = 1.0, lang: str = "default"):
        """"
        create a new TTS instance

        :param rate: rate of speech of TTS
        :type rate: int
        :param volume: volume level of TTS in range 0.1 - 1.0
        :type volume: float
        :param lang: languge of TTS
        :type lang: str
        """
        self.engine = pyttsx3.init()
        self.lang = lang
        self.pyttsx3_volume = volume
        self.pyttsx3_rate = rate

    def speak(self, text: str):
        """
        reads out the text using pico2wave as default TTS

        :param text: string of text to played as sound
        :type text: str
        """
        try:
            output_voice_path = os.path.join(project_root_path, "voice.wav")
            if os.path.exists(output_voice_path):
                os.remove(output_voice_path)
            os.system(f"pico2wave -w {output_voice_path} -l en-GB '{text}'")
            os.system(f"aplay {output_voice_path}")

        except:
            # fallback to pyttsx3  pico2wave fails
            self.engine.say(text=text)
            self.set_pyttsx3_properties()  # sets the properties pyttsx3
            self.engine.runAndWait()

    def speak_pyttsx3(self, text: str):
        """
        reads out text using pyttsx3 module

        :param text: string of text to be played by pyttsx3
        :type text: str
        """
        self.set_pyttsx3_properties()
        self.engine.say(text)
        self.engine.runAndWait()

    def change_lang(self, new_lang: str):
        """
        changes the TTS language

        :param new_lang: new TTS language
        :type new_lang: str
        """
        self.lang = new_lang

    def change_pyttsx3_rate(self, new_rate: int):
        """
        changes the pyttsx3 speaking rate

        :param new_rate: new TTS rate
        :type new_rate: int
        """
        self.pyttsx3_rate = new_rate

    def change_pyttsx3_volume(self, new_volume: float):
        """
        changes the pyttsx3 volume

        :param new_volume: new pyttsx3 volume in range 0.1 - 1.0
        :type new_volume: float
        """
        self.pyttsx3_volume = new_volume

    def set_pyttsx3_properties(self):
        """
        sets the rate, volume, voice property after the pyttsx3.engine.Engine instance is created
        """
        self.engine.setProperty("rate", self.pyttsx3_rate)
        self.engine.setProperty("volume", self.pyttsx3_volume)
        self.engine.setProperty("voice", self.lang)

    def get_pyttsx3_langs(self):
        """
        gets the possible languages for pico2wave and pyttsx3 TTS

        :return: list_voices
        """
        list_voices = []
        voices = self.engine.getProperty("voices")
        for voice in voices:
            list_voices.append(voice.id)
        return list_voices
