import os
import sys
import time
import webbrowser
import threading
import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
from colorama import init, Fore, Style
from typing import Optional

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class JARVISAssistant:
    def __init__(self, api_key: str):
        """
        Initialize JARVIS with Gemini API, speech recognition, and text-to-speech
        """
        # Configure Gemini API
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            self.log_error(f"Gemini API Configuration Error: {e}")
            sys.exit(1)
        
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize Text-to-Speech
        self.engine = pyttsx3.init()
        self.configure_tts()

    def configure_tts(self):
        """
        Configure text-to-speech settings
        """
        # Adjust speech rate and volume
        self.engine.setProperty('rate', 170)  # Speaking rate
        self.engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
        
        # Optional: Set voice (platform-dependent)
        voices = self.engine.getProperty('voices')
        # Choose a male or female voice (varies by system)
        self.engine.setProperty('voice', voices[0].id)  # First available voice

    def speak(self, text: str):
        """
        Convert text to speech
        """
        try:
            print(Fore.CYAN + f"JARVIS: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.log_error(f"Speech Error: {e}")

    def listen(self) -> Optional[str]:
        """
        Listen and convert speech to text
        """
        with self.microphone as source:
            print(Fore.GREEN + "Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                print(Fore.YELLOW + f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print(Fore.RED + "Sorry, I couldn't understand audio.")
                return None
            except sr.RequestError:
                print(Fore.RED + "Speech recognition service error.")
                return None
            except Exception as e:
                print(Fore.RED + f"Listening error: {e}")
                return None

    def generate_response(self, prompt: str) -> str:
        """
        Generate response using Gemini API
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {e}"

    def process_command(self, command: str) -> str:
        """
        Process user commands with specialized handling
        """
        # Greetings
        if command in ['hi', 'hello', 'hey']:
            return "Hello! I'm JARVIS, your virtual assistant. How can I help you today?"
        
        # System commands
        if 'open browser' in command:
            webbrowser.open('https://www.google.com')
            return "Opening web browser."
        
        # Time and date
        if 'time' in command:
            return time.strftime("The current time is %H:%M:%S")
        
        # Default to Gemini's response generation
        return self.generate_response(command)

    def interactive_mode(self):
        """
        Interactive mode with speech and text input
        """
        self.speak("JARVIS activated. How can I assist you?")
        
        while True:
            print("\n" + Fore.GREEN + "Choose interaction mode:")
            print(Fore.CYAN + "1. Voice Input")
            print(Fore.CYAN + "2. Text Input")
            print(Fore.CYAN + "3. Exit")
            
            choice = input(Fore.YELLOW + "Enter your choice (1/2/3): ")
            
            if choice == '1':
                voice_input = self.listen()
                if voice_input:
                    response = self.process_command(voice_input)
                    self.speak(response)
            
            elif choice == '2':
                text_input = input(Fore.YELLOW + "Enter your command: ")
                response = self.process_command(text_input)
                print(Fore.CYAN + f"JARVIS: {response}")
            
            elif choice == '3':
                self.speak("Goodbye! JARVIS is shutting down.")
                break
            
            else:
                print(Fore.RED + "Invalid choice. Please try again.")

    @staticmethod
    def log_error(message: str):
        """
        Log errors with color
        """
        print(Fore.RED + message)

    @staticmethod
    def display_logo():
        """
        Display JARVIS ASCII logo
        """
        print(Fore.LIGHTBLUE_EX + """     
     ____.  _____  ______________   ____.___  _________
    |    | /  _  \ \______   \   \ /   /|   |/   _____/
    |    |/  /_\  \ |       _/\   Y   / |   |\_____  \ 
/\__|    /    |    \|    |   \ \     /  |   |/        \ 
\________\____|__  /|____|_  /  \___/   |___/_______  /
                 \/        \/                       \/ 
Virtual Assistant JARVIS By akp
""")

def main():
    # Display logo
    JARVISAssistant.display_logo()
    
    # Gemini API Key
    API_KEY = "write your api key"
    
    # Initialize JARVIS
    jarvis = JARVISAssistant(API_KEY)
    
    # Start interactive mode
    jarvis.interactive_mode()

if __name__ == "__main__":
    main()
