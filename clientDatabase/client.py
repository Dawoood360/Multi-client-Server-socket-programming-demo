import socket
import struct
import sys
import os

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 80
        try:
            self.s.connect(('127.0.0.1', port))
        except:
            print("Connection failed")
            sys.exit(0)

    def makeGetPacket(self, fileName):
        msg = "GET /"+fileName+" HTTP/1.0\nHost: reqbin.com"
        stringSize = len(msg)
        packet = struct.pack(str(stringSize)+'s', msg.encode("utf-8"))
        return packet
    
    def makePostPacket(self,fileName):
        with open(fileName) as f:
                lines = f.readlines()
                f.seek(0, os.SEEK_END)
                fileSize=f.tell()
                f.close()
        msg = "POST /"+fileName+" HTTP/1.0\nHost: reqbin.com\nContent-Length: "+str(fileSize)
        stringSize = len(msg)
        packet = struct.pack(str(stringSize)+'s', msg.encode("utf-8"))
        return packet

    def sendState(self):
        try:
            while True:
                method = input("Enter type of request POST or GET :")
                if method == 'GET':
                    fileName = input("Please enter the file u wish to get: ")
                    packet = self.makeGetPacket(fileName)
                    self.s.send(packet)
                    self.receiveState(method)
                elif method=='POST':
                    fileName = input("Please enter the file u wish to POST: ")
                    try:
                        packet = self.makePostPacket(fileName)
                    except :
                        print('File not Found')
                        continue
                    self.s.send(packet)
                    self.sendFile(fileName)
                    self.receiveState(method)
        except KeyboardInterrupt:
            self.s.close()
    def sendFile(self,fileName):
        with open(fileName) as f:
                lines = f.readlines()
                for line in lines:
                    # print(line)
                    stringSize = len(line)
                    packet = struct.pack(
                        str(stringSize)+'s', line.encode("utf-8"))
                    self.s.send(packet)
        return
    def receiveState(self,method):
        if method == 'GET':
            packet = self.s.recv(28)
            rawMsg = struct.unpack('8s i 9s i', packet)
            Responsemsg = rawMsg[1]
            header = rawMsg[0].decode('utf-8')+' '+str(rawMsg[1])+' '+rawMsg[2].decode('utf-8')
            print(header)
            if Responsemsg == 200:
                payloadSize = rawMsg[3]
                f = open("receivedFile.txt", 'a')
                while payloadSize != 0:
                    if payloadSize > 1000:
                        data = self.s.recv(1000)
                        payloadSize -= 1000

                    elif payloadSize > 100:
                        data = self.s.recv(100)
                        payloadSize -= 100
                    elif payloadSize > 10:
                        data = self.s.recv(10)
                        payloadSize -= 10
                    else:
                        data = self.s.recv(payloadSize)
                        payloadSize = 0
                    f.write(data.decode('utf-8'))
                    # print(data.decode('utf-8'))
           