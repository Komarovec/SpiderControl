import asyncio
from threading import Thread
from bleak import discover, BleakClient
from queue import Queue
import time

class BLECom():
    def __init__(self, callback, *args):
        self.changeStateCallback = callback
        self.connection = False
        self.address = "A8:10:87:47:3D:C0"
        self.DATA_IO = "0000ffe1-0000-1000-8000-00805f9b34fb"
        self.startThread()
        self.exit = False # Exits thread next loop

    #Join thread when exiting
    def endThread(self, *args):
        self.exit = True
        self.msg_queue.put(None)

    #Starts thread
    def startThread(self, *args):
        self.exit = False
        self.msg_queue = Queue()
        self.th = Thread(target=self.startBluetooth)
        self.th.start()

    #Send msg
    def sendMsg(self, msg):
        self.msg_queue.put(msg)

    #Sends adds command number to hex-string and send to BLE class
    def sendCmd(self, cmd, rep):
        self.sendMsg([0x55, 0x55, 0x05, 0x06, cmd, rep, 0x00])

    #Threaded workload sends and receives bytes via BLE
    async def run(self, address, uuid, loop):
        #Connecting loop
        while True:
            try:
                async with BleakClient(address, loop=loop) as client:
                    self.changeStateCallback(self.connection)
                    #Sending loop
                    while True:
                        self.connection = await client.is_connected()
                        if(not self.connection):
                            break

                        #Check if queue is empty
                        if(self.msg_queue.empty()):
                            msg = None
                        else:
                            msg = self.msg_queue.get()
                            #If none then end thread
                            if(msg == None or self.exit):
                                return

                        if(msg != None):
                            await client.write_gatt_char(uuid, bytearray(msg))
                            self.msg_queue.task_done()

                self.changeStateCallback(self.connection) #Callback connection changed
            except:
                #End thread on exit
                if(self.exit):
                    return

    #Called in new thread!!
    def startBluetooth(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.run(self.address, self.DATA_IO, loop))
