# To automate Mouse and Keyboard controls
import pyautogui as pg
# google library to transform text to speech
from gtts import gTTS as gts
# to recognize the speech from the microphone / audio file
import speech_recognition as sr
# to play the sound converted using gTTS
import playsound as ps
import os  # To delete the generated audio files
import random  # For generating the random numbers for our generated file
import webbrowser  # For opening the web-browser
from time import ctime  # To get the current time

pg.FAILSAFE = False


class Assistant():
    def __init__(self, name):
        self.name = name
        self.recognizer = sr.Recognizer()

    def listen(self, ask=False):
        with sr.Microphone() as self.source:
            if ask:
                self.speak(ask)
            self.audio = self.recognizer.listen(self.source)
            voice_data = ''
            try:
                voice_data = self.recognizer.recognize_google(self.audio)
            except sr.UnknownValueError:
                self.speak('Sorry, I did not get that')
            except sr.RequestError:
                self.speak("Sorry, my speech service is down")
            return voice_data

    def speak(self, audio_string):
        self.tts = gts(text=audio_string, lang='en')
        self.r = random.randint(1, 10000000)
        self.audio_file = 'audio-' + str(self.r) + '.mp3'
        self.tts.save(self.audio_file)
        ps.playsound(self.audio_file)
        print(audio_string)
        os.remove(self.audio_file)

    def respond(self, voice_data):
        if 'what is your name' in voice_data:
            self.speak(f'My name is {self.name}')
        elif ('what time is it') in voice_data:
            self.speak(ctime())
        elif 'search' in voice_data:
            self.search = self.listen('What do you want to search for?')
            self.url = f"https://google.com/search?q={self.search}"
            webbrowser.get().open(self.url)
            self.speak(f'Here is what I found for {self.search}')
        elif 'find location' in voice_data:
            self.location = self.listen('What is the location?')
            self.url = f"https://google.nl/maps/place/{self.location}/&amp;"
            webbrowser.get().open(self.url)
            self.speak(f'Here is the location of {self.location}')
        elif 'shutdown' in voice_data:
            self.speak("Shutting down your PC")
            pg.click(x=0, y=1079)
            pg.click(x=22, y=1008)
            pg.click(x=27, y=927)
        elif 'weather' in voice_data:
            self.speak("Searching For Weather of Fateh Jang.")
            self.url = f"https://google.com/search?q=fateh jang weather"
            webbrowser.get().open(self.url)
            self.speak(f'Here is the weather for Fateh Jang')
        elif 'exit' in voice_data:
            self.speak('Good Bye')
            exit(0)


if __name__ == "__main__":
    assistant = Assistant("Rebbica")
    assistant.speak(
        f"Hello, my name is {assistant.name}. And I am designed by Wasif Ali")
    while True:
        assistant.speak("I am listening")
        voice_data = assistant.listen()
        assistant.respond(voice_data)
        # assistant.speak("Kindly wait for a few seconds.")
