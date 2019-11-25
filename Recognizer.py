from queue import Queue

#Speech recognition
import speech_recognition as sr
from threading import Thread

class Recognizer():
    def __init__(self, *_):
        #Record Audio
        self.r = sr.Recognizer()

        try:
            self.mic = sr.Microphone()
        except:
            self.mic = None # No default microphone

        self.audio_queue = Queue()

        #Recognized message
        self.msg = None

        #Listening
        self.stop_listening = None

    def start(self):
        self.recognize_thread = Thread(target=self.recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()

    def stop(self):
        if(self.stop_listening != None):
            self.stop_listening(wait_for_stop=False)
        
        self.audio_queue.join()  # block until all current audio processing jobs are done
        self.audio_queue.put(None)  # tell the recognize_thread to stop
        self.recognize_thread.join()  # wait for the recognize_thread to actually stop

    def recognize_worker(self):
        while True:
            #Background thread
            audio = self.audio_queue.get()  # retrieve the next audio processing job from the main thread
            if audio is None: return  # stop processing if the main thread is done

            try:
                self.msg = "Recognizing..."
                self.msg = self.r.recognize_google(audio)
            except:
                self.msg = "Cannot recognize!"

            self.audio_queue.task_done()  # mark the audio processing job as completed in the queue

    def callback(self, recognizer, audio):
        self.audio_queue.put(audio)

    def record(self, *_):
        if(self.mic == None): return;

        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, duration=0.5)
        
        self.stop_listening = self.r.listen_in_background(self.mic, self.callback)

    def stopRecord(self):
        self.stop_listening(wait_for_stop=False)