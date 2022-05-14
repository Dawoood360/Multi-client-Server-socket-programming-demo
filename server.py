from pickle import TRUE
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
        self.msgs=[]
    def clientThread(self,c):
        msg2=None
        startTime=None
        timeoutenabled = False
        while True:
                packetLength = c.recv(5).decode("utf-8")
                if packetLength =="" :
                    # print('HI')
                    # lock.release()
                    if  msg2=="1.0":
                        print('connection Closed')
                        c.close()
                        break
                    elif msg2=="1.1":
                        # print('1.1')
                        if not timeoutenabled:
                            print('timeout set')
                            startTime=time.time()
                            timeoutenabled = TRUE
                            for msg in self.msgs:
                                self.respondState(msg,c)
                        elif time.time()-startTime >5:
                            print('connection Closed')
                            c.close()
                            break

                else:
                    packet = c.recv(int(packetLength)) 
                    msg = struct.unpack(str(len(packet))+'s', packet)
                    msg = msg[0].decode("utf-8")
                    msg2=msg.split(" \n")[0].split(' ')[2].split('\n')[0].split('/')[1]
                if msg2=="1.0":
                    self.respondState(msg,c)
                elif msg2=="1.1":
                    self.msgs.append(msg)
        
            
        

                
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
