

#Kivy and GUI
import kivy 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget

#Speech recognition
import speech_recognition as sr
from threading import Thread

#Kolem
from functools import partial
from queue import Queue


# Record Audio
r = sr.Recognizer()
mic = sr.Microphone()
audio_queue = Queue()

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

def callback(recognizer, audio):
    audio_queue.put(audio)

def record(*args):
    global stop_listening
    stop_listening = r.listen_in_background(mic, callback)

class VoiceApp(App):
    #States
    IDLE_STATE = "idle"
    RECORD_STATE = "record"
    RECOGNIZE_STATE = "recognize"

    COMMANDS = {
        "up":["straight","forward"],
        "down":["backward","back","backoff","reverse"],
        "left":["left"],
        "right":["right"],
        "dance":["dance"],
        "fight":["fight", "exterminate"],
        "hi":["hi","hello","greetings","greed","morning"],
        "top":["top","high","highest","third","upper"],
        "mid":["middle","mid","center","second"],
        "low":["low", "lowest", "bottom", "ground", "sit", "first"]
    }

    def build(self):
        #Keyboard init
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        #Init layout
        mainlayout = BoxLayout(orientation="horizontal")
        layout = BoxLayout(orientation="vertical")

        #Important vars
        self.lastAction = None
        self.state = self.IDLE_STATE
        self.position = 0 #0 - Low, 1 - Mid, 2 - High 
        self.step = 0 #0 - Small, 1 - Large

        #Record button
        self.stateText = Label(text="Idle")
        recBtn = ToggleButton(text="Click to start recording.")
        recBtn.bind(state=self.on_click_rec)

        #Stop
        stopBtn = Button(text="Stop")
        stopBtn.bind(on_press=partial(self.takeAction, "stop"))

        #Main layout preparation
        mainlayout.add_widget(Label(text=""))
        mainlayout.add_widget(layout)
        mainlayout.add_widget(Label(text=""))

        #Sublayout preparation
        layout.add_widget(self.stateText)
        layout.add_widget(recBtn)
        layout.add_widget(stopBtn)

        Clock.schedule_interval(self.think, 1/60)

        return mainlayout

    def on_click_rec(self, btn, state):
        global stop_listening

        if(state == "down" and self.state == self.IDLE_STATE):
            self.state = self.RECORD_STATE
            record()
        elif(state == "up"):
            stop_listening(wait_for_stop=False)

    #When window created
    def on_start(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        self.recognize_thread = Thread(target=recognize_worker)
        self.recognize_thread.daemon = True
        self.recognize_thread.start()

        #Import after kivy
        from BLE import BLECom
        self.BLE = BLECom()

    #When exiting
    def on_stop(self):
        global stop_listening
        stop_listening(wait_for_stop=False)
        audio_queue.join()  # block until all current audio processing jobs are done
        audio_queue.put(None)  # tell the recognize_thread to stop
        self.recognize_thread.join()  # wait for the recognize_thread to actually stop

        self.BLE.endThread()
        self.BLE.th.join()

    #Send appropriate command to bluetooth
    def checkCommand(self, msg):
        #For each word check commands, each command can be triggered by some word --> 3 loops
        for word in msg.split(" "):
            for cmd in self.COMMANDS:
                for dt in self.COMMANDS[cmd]:
                    #If trigger word matches command --> take action
                    if(dt == word):
                        self.takeAction(cmd)
 
    #Take action
    def takeAction(self, action, *_):
        #Reapeted action protection
        if(self.lastAction == action):
            return
        self.lastAction = action

        #Position change
        if(action == "top" or action == "numpad9"):
            self.BLE.sendCmd(34,1)
            self.position = 2
        elif(action == "mid" or action == "numpad6"):
            self.BLE.sendCmd(25,1)
            self.position = 1
        elif(action == "low" or action == "numpad3"):
            self.BLE.sendCmd(0,1)
            self.position = 0

        #Stop any movement
        elif(action == "stop" or action == "r"):
            if(self.position == 2):
                self.BLE.sendCmd(34,1)
            elif(self.position == 1):
                self.BLE.sendCmd(25,1)
            elif(self.position == 0):
                self.BLE.sendCmd(0,1)    
    
        #Go forward
        elif(action == "forward" or action == "up"):
            if(self.position == 2):
                self.BLE.sendCmd(35,0)
            elif(self.position == 1):
                self.BLE.sendCmd(26,0)
            elif(self.position == 0):
                self.BLE.sendCmd(1,0) 

        #Go backward
        elif(action == "backward" or action == "down"):
            if(self.position == 2):
                self.BLE.sendCmd(36,0)
            elif(self.position == 1):
                self.BLE.sendCmd(27,0)
            elif(self.position == 0):
                self.BLE.sendCmd(2,0)  

        #Go left
        elif(action == "left"):
            if(self.position == 2):
                self.BLE.sendCmd(37,0)
            elif(self.position == 1):
                self.BLE.sendCmd(28,0)
            elif(self.position == 0):
                self.BLE.sendCmd(3,0) 

        #Go right
        elif(action == "right"):
            if(self.position == 2):
                self.BLE.sendCmd(38,0)
            elif(self.position == 1):
                self.BLE.sendCmd(29,0)
            elif(self.position == 0):
                self.BLE.sendCmd(4,0) 

        #Slide
        elif(action == "q"):
            self.BLE.sendCmd(7, 0)
        elif(action == "e"):
            self.BLE.sendCmd(8, 0)

        #Special
        elif(action == "dance" or action == "d"):
            self.BLE.sendCmd(9,1) 
        elif(action == "hi" or action == "h"):
            self.BLE.sendCmd(12,1)
        elif(action == "fight" or action == "f"):
            self.BLE.sendCmd(10,1)  
        elif(action == "kick" or action == "k"):
            self.BLE.sendCmd(11,1)  
        elif(action == "pack" or action == "p"):
            self.BLE.sendCmd(100,1)

    #Kivy loop
    def think(self, dt):
        global msg

        #If recording
        if(msg != None):
            self.state = self.IDLE_STATE
            self.stateText.text = msg

            #Check for command
            self.checkCommand(msg)

            msg = None

    #Keyboard interface
    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode[1], 'have been pressed')
        self.takeAction(keycode[1])
        
        return True


if __name__ == '__main__':
    VoiceApp().run()