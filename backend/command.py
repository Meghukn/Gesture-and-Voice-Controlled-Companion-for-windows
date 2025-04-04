import datetime
import os
import sys
import time
import cv2
import pyautogui
import pyttsx3
import requests
import speech_recognition as sr
import eel
import wikipedia
from googletrans import Translator
from backend import hand

translator = Translator()  # Initialize the translator

# Expose the function so it can be called from JavaScript
@eel.expose
def start_hand_gesture_recognition():
    hand.start_hand_gesture_recognition()  # Call the function from hand.py

# Initialize global language variable (default to English)
selected_language = 'en'  # Default language is English

# Expose function to set language
@eel.expose
def setLanguage(language):
    global selected_language
    selected_language = language
    print(f"Language set to: {selected_language}")
    eel.setLanguage(language)  # Trigger JavaScript function to change placeholder


def speak(text):
    """
    Converts text to speech in the selected language.
    """
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')

    if selected_language == 'kn':  # Kannada
        # Check if Kannada voice is available
        for voice in voices:
            if 'Kannada' in voice.name:  # Select Kannada voice if available
                engine.setProperty('voice', voice.id)
                break
        else:
            print("Kannada voice not found. Using default voice.")
            engine.setProperty('voice', voices[1].id)  # Fall back to default voice (English)
        
        text = translate_to_kannada(text)  # Translate English to Kannada if necessary
    
    else:  # Default to English
        engine.setProperty('voice', voices[1].id)
    
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)  # Display message in the frontend
    engine.say(text)  # Speak the text
    eel.receiverText(text)  # Send the text to be displayed in the chat history
    engine.runAndWait()

def takecommand():
    """
    Captures voice input and returns it as text. Translates Kannada to English if needed.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        # Check the selected language
        if selected_language == 'kn':  # Kannada recognition
            query = r.recognize_google(audio, language='kn-IN')
            print(f"User said (Kannada detected): {query}")
        else:  # Default to English recognition
            query = r.recognize_google(audio, language='en-IN')
            print(f"User said (English detected): {query}")
        
        eel.DisplayMessage(query)

        # If the recognized query is in Kannada, translate it to English
        if selected_language == 'kn':
            print("Detected Kannada. Translating to English...")
            query = translator.translate(query, src='kn', dest='en').text
            print(f"Translated to English: {query}")
        
        query = clean_translated_query(query)
        eel.DisplayMessage(query)

    except sr.UnknownValueError:
        print("Could not understand the audio.")
        eel.DisplayMessage("Could not understand the audio.")
        return ""

    except sr.RequestError as e:
        print(f"Error with speech recognition service: {e}")
        eel.DisplayMessage("There was an issue with the recognition service.")
        return ""

    except Exception as e:
        print(f"Error: {e}")
        eel.DisplayMessage("An error occurred.")
        return ""

    return query.lower()

def clean_translated_query(query):
    """
    Cleans the translated query by removing filler words or unnecessary articles like 'the'.
    """
    fillers = ['the', 'a', 'this', 'that', 'to', 'of']
    words = query.split()
    filtered_words = [word for word in words if word.lower() not in fillers]
    return ' '.join(filtered_words)

def translate_to_english(query):
    """
    Translates a given Kannada query to English only if it's in Kannada.
    Otherwise, returns the query as-is.
    """
    try:
        # Detect language first
        detection = translator.detect(query)
        if detection.lang == 'en':  # If it's already in English
            print("Detected English. No translation required.")
            return query.lower()
        elif detection.lang == 'kn':  # If it's Kannada
            print("Detected Kannada. Translating to English...")
            translated_text = translator.translate(query, src='kn', dest='en').text
            print(f"Translated to English: {translated_text}")
            return clean_translated_query(translated_text).lower()
    except Exception as e:
        print("Translation error:", e)
    return query

def translate_to_kannada(text):
    """
    Translates a given English text to Kannada.
    """
    try:
        translated_text = translator.translate(text, src='en', dest='kn').text
        return translated_text
    except Exception as e:
        print("Error in translating to Kannada:", e)
        return text  # If translation fails, return original text

@eel.expose
def allCommands(message=1):
    """
    Processes user commands and performs the requested action.
    """
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        query = translate_to_english(query)  # Translate Kannada to English if necessary

        if "open" in query:
            from backend.features import openCommand
            openCommand(query)
        elif 'on youtube' in query:
            from backend.features import PlayYoutube
            PlayYoutube(query)
            speak("Playing on YouTube.")
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif "shut down system" in query:
            os.system("shutdown /s /t 5")

        elif "restart system" in query:
            os.system("shutdown /r /t 5")

        elif "lock system" in query:
            os.system("rundll32.exe user32.dll,LockWorkStation")

        elif "camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(1)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "go to sleep" in query:
            speak(' alright then, I am switching off')
            sys.exit()

        elif "ip address" in query:
            speak("Checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                speak("your ip address is")
                speak(ipAdd)
            except Exception as e:
                speak("network is weak, please try again some time later")

        elif "increase volume" in query or "volume up" in query:
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")
            pyautogui.press("volumeup")

        elif "volume down" in query or "decrease volume" in query:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        elif "mute" in query:
            pyautogui.press("volumemute")
        elif 'what is' in query or 'where is' in query or 'who is' in query:
            speak("Searching...")
            if 'what is' in query:
                query = query.replace("what is", "")
            elif 'where is' in query:
                query = query.replace("where is", "")
            elif 'who is' in query:
                query = query.replace("who is", "")
            
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There are multiple results, please be more specific.")
                print("DisambiguationError:", e)
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("The request timed out. Please try again later.")
            except wikipedia.exceptions.ConnectionError:
                speak("There is a problem with the connection. Please check your internet.")
            except Exception as e:
                speak("Sorry, I couldn't find an answer to that.")
                print("Error:", e)
        else:
            speak("I'm not sure how to handle that.")
    except Exception as e:
        print("Error:", e)
        
    eel.ShowHood()