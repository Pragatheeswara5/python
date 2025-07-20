import speech_recognition as sr
import threading
import webbrowser
import pyttsx3

stop_listening_flag=False
final_text=[]

def speak(text):
    try:
        engine=pyttsx3.init()
        voices=engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(text)
        engine.runAndWait()
    except:
        print("Something went wrong....!")

def stop_by_keyboard():
    global stop_listening_flag
    input("Press enter at any time stop recording...\n")
    stop_listening_flag=True

def callback(recognizer, audio):
    global stop_listening_flag
    try:
        text=recognizer.recognize_google(audio)
        print("You said: ", text)
        final_text.append(text)

    except sr.UnknownValueError:
        print("Could not understand your audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

def main():
    global stop_listening_flag

    recognizer=sr.Recognizer()
    mic=sr.Microphone()

    keyboard_thread=threading.Thread(target=stop_by_keyboard)

    keyboard_thread.start()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening in real time... Speak now")

    stop_listen_func=recognizer.listen_in_background(mic, callback)

    while not stop_listening_flag:
        pass

    stop_listen_func(wait_for_stop=False)

    print("\nFinal Transcription:")
    print(" ".join(final_text))

    if 'youtube' in final_text[0].lower():
        speak("Opening YouTube....")
        webbrowser.open("https://www.youtube.com/")

if __name__ == "__main__":
    main()