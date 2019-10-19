import asyncio
from threading import Thread
from bleak import discover, BleakClient
from queue import Queue
import time


class BLECom():
    def __init__(self, *args):
        self.address = "A8:10:87:47:3D:C0"
        self.DATA_IO = "0000ffe1-0000-1000-8000-00805f9b34fb"
        self.msg_queue = Queue()
        self.th = Thread(target=self.startBluetooth)
        self.th.start()

    #Join thread when exiting
    def endThread(self, *args):
        self.msg_queue.put(None)

    #Send msg
    def sendMsg(self, msg):
        self.msg_queue.put(msg)

    #Threaded workload send and receives bytes via BLE
    async def run(self, address, uuid, loop):
        try:
            async with BleakClient(address, loop=loop) as client:
                while True:
                    #Check if queue is empty
                    if(self.msg_queue.empty()):
                        msg = None
                    else:
                        msg = self.msg_queue.get()
                        #If none then end thread
                        if(msg == None):
                            break

                    if(msg != None):
                        await client.write_gatt_char(uuid, bytearray(msg))
                        self.msg_queue.task_done()
        except:
            print("Cannot connect")

    #Called in new thread!!
    def startBluetooth(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.run(self.address, self.DATA_IO, loop))
