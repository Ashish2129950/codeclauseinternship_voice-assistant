import tkinter as tk
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import pywhatkit as kit
import os
import time
import threading

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    if "hello" in command:
        return "Hello! How can I assist you?"
    elif "how are you" in command:
        return "I'm doing well, thank you for asking."
    elif "goodbye" in command:
        return "Goodbye! Have a great day."
    else:
        try:
            result = wikipedia.summary(command, sentences=2)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return "Multiple results found. Please specify."
        except wikipedia.exceptions.PageError as e:
            return "No matching page found."

def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    button_listen.config(text="Listening...", bg="#FFA500")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        assistant_response_label.config(text=command)
        response = process_command(command)
        assistant_response_label.config(text=response)
        speak(response)
    except sr.UnknownValueError:
        assistant_response_label.config(text="Could not understand audio")
    except sr.RequestError as e:
        assistant_response_label.config(text="Error: {0}".format(e))
    finally:
        button_listen.config(text="Listen", bg="#4CAF50")

def open_browser():
    webbrowser.open("https://www.google.com")

def play_song():
    kit.playonyt("Hit Hindi songs")

def close_notepad():
    os.system("taskkill /f /im notepad.exe")

def open_notepad():
    os.system("start notepad.exe")

def open_cmd():
    os.system("start cmd")

def close_cmd():
    os.system("taskkill /f /im cmd.exe")

def get_ip_address():
    ip = get('https://api.ipify.org').text
    return f"Your IP address is {ip}"

def get_time():
    current_time = time.strftime("%I:%M %p")
    return f"The current time is {current_time}"

def restart_system():
    os.system("shutdown /r /t 5")

def shutdown_system():
    os.system("shutdown /s /t 5")

def sleep_system():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def switch_window():
    pyautogui.keyDown("alt")
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.keyUp("alt")

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def main():
    while True:
        mic_input = mic().lower()
        if "hello" in mic_input or "hi" in mic_input:
            speak("Hello! How can I assist you?")
        elif "open browser" in mic_input:
            open_browser()
        elif "play song" in mic_input:
            play_song()
        elif "close notepad" in mic_input:
            close_notepad()
        elif "open notepad" in mic_input:
            open_notepad()
        elif "open command prompt" in mic_input:
            open_cmd()
        elif "close command prompt" in mic_input:
            close_cmd()
        elif "ip address" in mic_input:
            speak(get_ip_address())
        elif "time" in mic_input:
            speak(get_time())
        elif "restart system" in mic_input:
            restart_system()
        elif "shutdown system" in mic_input:
            shutdown_system()
        elif "sleep system" in mic_input:
            sleep_system()
        elif "switch window" in mic_input:
            switch_window()
        elif "open youtube" in mic_input:
            open_youtube()
        else:
            speak("Sorry, I didn't understand that.")

def mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=4, phrase_time_limit=5)
    try:
        print("Recognizing...")
        mic_input = r.recognize_google(audio, language='en-in')
        print("User said:", mic_input)
        return mic_input
    except Exception as e:
        print("Say that again please...")
        return "none"

def listen_button_click():
    threading.Thread(target=recognize_speech).start()

# Create the main window
window = tk.Tk()
window.title("Voice Assistant")

# Button styling
button_style = {"background": "#4CAF50", "foreground": "white", "font": ("Times New Roman", 14), "bd": 3}

# Create buttons
button_listen = tk.Button(window, text="Listen", command=listen_button_click, **button_style)
button_listen.pack(pady=10, side="top", anchor="center")

button_browser = tk.Button(window, text="Open Browser", command=open_browser, **button_style)
button_browser.pack(pady=10, side="top", anchor="center")

button_song = tk.Button(window, text="Play Song", command=play_song, **button_style)
button_song.pack(pady=10, side="top", anchor="center")

button_close = tk.Button(window, text="Close", command=window.destroy, **button_style)
button_close.pack(pady=10, side="top", anchor="center")

# Create label for displaying assistant response
assistant_response_label = tk.Label(window, text="", wraplength=400, font=("Times New Roman", 14))
assistant_response_label.pack(pady=10, side="top", anchor="center")

# Run the application
window.mainloop()
