from time import sleep
import os
import requests
import webbrowser as wb
import pyttsx3 as pt
import speech_recognition as sr
import musicl_ibrary  # Ensure this module is correctly named
from openai import OpenAI

# Initialize components
engine = pt.init()
recognizer = sr.Recognizer()
newsapi = os.getenv("NEWS_API_KEY", "your_newsapi_key_here")

def speak(word):
    engine.setProperty('rate', 150)
    engine.say(word)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def choice():
    with sr.Microphone() as source:
        try:
            print("Speak")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            return command
        except (sr.UnknownValueError, sr.RequestError) as e:
            if isinstance(e, sr.UnknownValueError):
                print("Sorry, I did not understand that. Please try again.")
            else:
                print("Sorry, there was an issue with the speech recognition service.")
            return None

def process_command(c):
    if c is None:
        print("...")
        return
    else:
        c = c.lower()
        if "open" in c:
            if "google" in c:
                wb.open("https://www.google.com")
            elif "facebook" in c:
                wb.open("https://www.facebook.com")
            elif "youtube" in c:
                wb.open("https://www.youtube.com")
            elif "instagram" in c:
                wb.open("https://www.instagram.com")
        elif "play" in c:
            song = c.lower().split(" ")[1]
            if song in musicl_ibrary.music:
                link = musicl_ibrary.music[song]
                wb.open(link)
            else:
                print("No song found")
                speak("No song found")
                return
        elif "news" in c.lower():
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                for article in articles:
                    speak(article['title'])
                    print(article['title'])
        else:
            output = aiProcess(c)
            speak(output)

if __name__ == "__main__":
    while True:
        speak("Do you want to initialize Jarvis? (Yes or No)")
        user_choice = None
        while user_choice is None:
            user_choice = choice()

        if "no" in user_choice.lower():
            speak("Exiting the program...")
            break
        elif "yes" in user_choice.lower():
            speak("Initializing Jarvis...")
            while True:
                speak("Please give a command or say 'exit' to stop.")
                command = choice()
                if command is not None and "exit" in command.lower():
                    speak("Exiting Jarvis...")
                    break
                else:
                    process_command(command)
                    print("...")
                    sleep(5)
