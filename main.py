#Bluetooth
import pygatt

#Kivy and GUI
import kivy 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

#Speech recognition
import speech_recognition as sr
from threading import Thread
from queue import Queue


# Record Audio
r = sr.Recognizer()
mic = sr.Microphone()
audio_queue = Queue()

#Bluetooth adapter
adapter = pygatt.GATTToolBackend()

#Recognized message
msg = None

def recognize_worker():
    global msg
    while True:
        # this runs in a background thread
        audio = audio_queue.get()  # retrieve the next audio processing job from the main thread
        if audio is None: return  # stop processing if the main thread is done

        try:
            msg = r.recognize_google(audio)
        except:
            msg = "Cannot recognize!"

        audio_queue.task_done()  # mark the audio processing job as completed in the queue

def record(*args):
    # start a new thread to recognize audio, while this thread focuses on listening
    with sr.Microphone() as source:
        try:
            audio = r.listen(source, timeout=5)
            audio_queue.put(audio)
        except:
            pass

class VoiceApp(App):
    IDLE_STATE = "idle"
    RECORD_STATE = "record"
    RECOGNIZE_STATE = "recognize"

    def build(self):
        mainlayout = BoxLayout(orientation="horizontal")
        layout = BoxLayout(orientation="vertical")

        #Important vars
        self.state = self.IDLE_STATE

        #Action button
        self.stateText = Label(text="Idle")
        btn = Button(text="Click to start recording.")
        btn.bind(state=self.on_click)

        #Main layout preparation
        mainlayout.add_widget(Label(text=""))
        mainlayout.add_widget(layout)
        mainlayout.add_widget(Label(text=""))

        #Sublayout preparation
        layout.add_widget(self.stateText)
        layout.add_widget(btn)
        layout.add_widget(Label(text=""))

        Clock.schedule_interval(self.think, 1/60)

        return mainlayout

    def on_click(self, btn, state):
        if(state == "down" and self.state == self.IDLE_STATE):
            self.state = self.RECORD_STATE
            self.stateText.text = "Recording..."

    def on_start(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        self.recognize_thread = Thread(target=recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()

    def on_stop(self):
        audio_queue.join()  # block until all current audio processing jobs are done
        audio_queue.put(None)  # tell the recognize_thread to stop
        self.recognize_thread.join()  # wait for the recognize_thread to actually stop

    def think(self, dt):
        global msg

        #If recording
        if(self.state == self.RECORD_STATE):
            record()
            self.stateText.text = "Recognizing..."
            self.state = self.RECOGNIZE_STATE
        
        elif(msg != None):
            self.state = self.IDLE_STATE
            self.stateText.text = msg
            msg = None


if __name__ == '__main__':
    VoiceApp().run()