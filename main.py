import keyboard
import pyaudio
import wave
import speech_recognition as sr   
import requests
import pyttsx3 
import openai
import os

# Define your ChatGPT API endpoint and API token

# API_ENDPOINT = "gpt-3.5-turbo"
API_TOKEN = ""
openai.api_key = API_TOKEN


# Initialize the text-to-speech engine
engine = pyttsx3.init()


# A function to handle key strokes
# def key_watcher(key):
#     if key.name == "space":
#         start_recording()

#     elif key.name == "esc":
#         stop_recording()

# def key_watcher(key):
#     if key == 1:
#         start_recording()      

    # elif key == "esc":
    #     stop_recording()



# A function to record voice using PyAudio
def start_recording():
    CHUNK = 1024
    FORAMT = pyaudio.paInt16
    CHANNELS = 1 
    RATE = 44100
    RECORD_SECONDS = 90

    p = pyaudio.PyAudio()
    stream = p.open(format=FORAMT,
                    channels=CHANNELS,
                    rate = RATE,
                    input = True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)

    print("recording....")
    
    
    # Collecting Voice frames
    frames=[]
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

        # if keyboard.is_pressed("esc"):
        #     stop_recording()
        #     return
        # Nothing more than 30 seconds
        if len(frames) > int(RATE / CHUNK * RECORD_SECONDS):
            break
        

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Thinking \n")

    # Compress all the frames into a single byte
    audio_data = b''.join(frames)
    audio = sr.AudioData(audio_data, sample_rate=RATE, sample_width=2)
    text = recognize_speech(audio) 
    response = get_chatgpt_response(text) 

    speak(response) 


def recognize_speech(audio_data):
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio_data, language="en-US")
        print(f"Recognized text: {text}")
        return text

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return ""

    except sr.RequestError as e:
        print(f"Error: {e}")
        return ""

# Retrieves the ChatGPT response
def get_chatgpt_response(text, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": text}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7, # how random your answers should be
    )
    print(response.choices[0].message["content"])
    return response.choices[0].message["content"]


# def stop_recording():
#     print("Recording stopped.")


# Define a function to speak text aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()


# key_watcher(1)
while(not keyboard.is_pressed == "esc"):
    start_recording()    
    if(keyboard.is_pressed == "enter"):    
        continue 
    if(keyboard.is_pressed == "esc"):    
        break 




# keyboard.wait("esc") 
# keyboard.unhook_all()
