

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
from kivy.properties import NumericProperty

#Function tools
from functools import partial

#Custom
from Recognizer import Recognizer

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
        #Recognizer object
        self.recog = Recognizer()

        #Keyboard init
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self.root, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        #Init layout
        mainlayout = BoxLayout(orientation="horizontal")
        layoutLeft = BoxLayout(orientation="vertical")
        layoutMid = BoxLayout(orientation="vertical")
        layoutRight = BoxLayout(orientation="vertical")

        #Control vars
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

        #Kivy properties
        self.queueSize = NumericProperty(0)

        #Taken action
        self.actionLabel = Label(text="Action: ")

        #Bluetooth connection
        self.bleLabel = Label(text="Not connected")

        #Audio queue to proces
        self.queueLabel = Label(text="To procces: "+str(self.queueSize))

        #Main layout preparation
        mainlayout.add_widget(layoutLeft)
        mainlayout.add_widget(layoutMid)
        mainlayout.add_widget(layoutRight)

        #Middle layout
        layoutMid.add_widget(self.stateText)
        layoutMid.add_widget(recBtn)
        layoutMid.add_widget(stopBtn)

        #Left layout
        layoutLeft.add_widget(self.actionLabel)
        layoutLeft.add_widget(self.bleLabel)
        layoutLeft.add_widget(self.queueLabel)

        Clock.schedule_interval(self.think, 1/60)

        return mainlayout

    def on_click_rec(self, btn, state):
        if(state == "down" and self.state == self.IDLE_STATE):
            self.state = self.RECORD_STATE
            self.recog.record()
        elif(state == "up"):
            self.recog.stopRecord()

    #When window created
    def on_start(self):
        # start a new thread to recognize audio, while this thread focuses on listening
        self.recog.start()

        #Import after kivy
        from BLE import BLECom
        self.BLE = BLECom()

    #When exiting
    def on_stop(self):
        self.recog.stop()

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
        msg = self.recog.msg

        #If recording
        if(msg != None):
            self.state = self.IDLE_STATE
            self.stateText.text = msg

            #Check for command
            self.checkCommand(msg)

            #Delete message after being sent
            self.recog.msg = None

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