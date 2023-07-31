import speech_recognition as sr
from PyQt5.QtCore import QThread


class VoiceCommandThread(QThread):

    def __init__(self):
        super().__init__()
        # self.callback = callback
        # self.recognizer = sr.Recognizer()
        # self.microphone = sr.Microphone()

    def run(self):
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                print("Asteapta comanda: ")
                ceva = r.listen(source)
            try:
                detected = r.recognize_google(ceva, language="ro-RO")
                print("Comanda: ", detected)
            except sr.UnknownValueError:
                print("Nu s-a putut detecta")
