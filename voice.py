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

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for background noise... Please wait")
        r.adjust_for_ambient_noise(source, duration=2)  # more reliable
        r.pause_threshold = 1.0
        print("Listening now... 🎤")

        try:
            # ⬆️ remove timeout restriction, only phrase_time_limit
            audio = r.listen(source, phrase_time_limit=25)
        except Exception as e:
            print("Listening error:", e)
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"✅ User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("❌ Couldn’t understand your voice.")
        return "None"
    except sr.RequestError:
        print("❌ Network issue, speech service down.")
        return "None"

