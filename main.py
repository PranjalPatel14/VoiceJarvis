import speech_recognition as sr
import webbrowser
import pyttsx3
import pyaudio
import musicLibrary
import requests
from dotenv import load_dotenv
import os

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
weather_api_key = os.getenv("weather-api")
news_api_key = os.getenv("news-api")

# Function to speak a text string
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process commands
def processCommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song in your library.")
    elif "news" in c.lower():
        if news_api_key:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, I couldn't fetch the news at the moment.")
        else:
            speak("News API key is missing.")
    elif "weather"or"temperature" in c.lower():
        city = c.lower().split(" ")[-1]
        weather(city)
    else:
        speak("Sorry, I didn't get that.")

def weather(city):
    if weather_api_key:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric")
        if r.status_code == 200:
            data = r.json()
            weather = data.get('weather', [])
            for w in weather:
                speak(f"The weather in {city} is {w['description']}")
                speak(f"The temperature is {data['main']['temp']} Feherenheit")
        else:
            speak("Sorry, I couldn' fetch the weather at the moment.")
    
if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        ## Listen to the word jarvis
        r = sr.Recognizer()
        
        print("Recognizing....")
        # recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Ya")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source, timeout=2, phrase_time_limit=5)
                command = r.recognize_google(audio)

                processCommand(command)
        except Exception as e:
            print("Error; {0}" .format(e))