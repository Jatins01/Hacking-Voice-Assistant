import pyttsx3
import speech_recognition as sr
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am HackSpeak. Please tell me how may I help you")

import speech_recognition as sr

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 300  
        r.pause_threshold = 1.2   
        r.dynamic_energy_threshold = True
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please say it again.")
        return "None"
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition.")
        return "None"

    return query
