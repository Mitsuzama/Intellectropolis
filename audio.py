import speech_recognition as sr
import pyttsx3


def speechToText(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["success"] = False
        response["error"] = "Unable to recognize speech"
    return response


def textToSpeech(myText):
    engine.say(myText)
    engine.runAndWait()


if __name__ == '__main__':
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    action = 'Listening'
    print(action)
    textToSpeech(action)
    quitFlag = True
    while (quitFlag):
        text = speechToText(recognizer, microphone)
        if not text["success"] and text["error"] == "API unavailable":
            print("ERROR: {}\nclose program".format(text["error"]))
            break

        while not text["success"]:
            print("I didn't catch that. What did you say?\n")
            text = speechToText(recognizer, microphone)

        if (text["transcription"].lower() == "exit"):
            quitFlag = False

        print(text["transcription"].lower())
        textToSpeech(text["transcription"].lower())
