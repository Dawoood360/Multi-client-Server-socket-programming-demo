import socket
import struct
import os
from _thread import *
import threading
import time

 
lock = threading.Lock()
class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
        port = 80
        self.sock.bind(('', port))
        print("socket binded to %s" % (port))
        self.sock.listen(5)
        print("socket is listening")
    def clientThread(self,c):
        msg2=None
        startTime=None
        while True:
                packetLength = c.recv(5).decode("utf-8")
                if packetLength =="" :
                    # lock.release()
                    c.close()
                    break
                    # if  msg2=="1.0":
                    #     c.close()
                    #     break
                    # elif msg2=="1.1":
                    #     if startTime==None:
                    #         startTime=time.time()
                    #     else:
                    #         currentTime=time.time()
                    #         if currentTime-startTime>=1000:
                    #             c.close()
                    #             break
                    #     continue
                packet = c.recv(int(packetLength)) 
                msg = struct.unpack(str(len(packet))+'s', packet)
                msg = msg[0].decode("utf-8")
                msg2=msg.split(" ")[2].split("/")[1]
                print(msg2)
                self.respondState(msg,c)
    def receiveState(self):
        while True:
            try:
                self.c, addr = self.sock.accept()
                # lock.acquire()
                print('Connected to :', addr[0], ':', addr[1])
                start_new_thread(self.clientThread, (self.c,))
            except KeyboardInterrupt:
                self.c.close()

    def respondState(self, msg,c):
        data = msg.split(' ')
        if data[0] == 'GET':
            self.getMethod(data,c)
            # print('Get')
        if data[0] == 'POST':
           self.postMethod(data,c)

    def getMethod(self, Msgdata,c):
        
        filename = Msgdata[1]
        print(filename)
        try:
            with open("database"+filename,"rb") as f:
                f.seek(0, os.SEEK_END)
                fileSize = f.tell()
                f.seek(0, os.SEEK_SET)
                acceptMsg = 200  # Message Accepted
                packet = struct.pack(
                    '8s i 9s i', b'HTTP/1.0', acceptMsg, b'OK       ', fileSize)
                c.send(packet)
                data=f.read()
                c.send(data)
                return
        except:
            msg = 404
            packet = struct.pack('8s i 9s i', b'HTTP/1.0',
                                 msg, b'NOT FOUND', 0)

            c.send(packet)
            return

    def postMethod(self, MsgData,c):
        print(MsgData)
        filename = MsgData[1]
        pay=MsgData[len(MsgData)-1]
        print(pay)
        payloadSize = int(pay)
        
        try:
            
            f= open("database"+filename, 'wb')
            
            while payloadSize != 0:
               
                if payloadSize > 1000:
                    data = self.c.recv(1000)
                    payloadSize -= 1000

                elif payloadSize > 100:
                    data = self.c.recv(100)
                    payloadSize -= 100
                elif payloadSize > 10:
                    data = self.c.recv(10)
                    payloadSize -= 10
                else:
                    data = self.c.recv(payloadSize)
                    payloadSize = 0
                f.write(data)
            f.close()
            msg = 200
            packet = struct.pack(
                '8s i 9s', b'HTTP/1.0', msg, b'OK       ')
            c.send(packet)
            
        except:
            msg = 404
            packet = struct.pack('8s i 9s', b'HTTP/1.0', msg, b'NOT FOUND')
            c.send(packet)
            return


server = Server()
server.receiveState()
