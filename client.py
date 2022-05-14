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

    def makePacket(self,request):
        packet = struct.pack(str(len(request))+'s', request.encode("utf-8"))
        return packet

    def sendState(self,request):
        
        self.method =request.split(" ")[0]
        self.fileName=request.split(" ")[1]
        
        if self.method == 'GET':
            try:
                f = open("clientDatabase"+self.fileName)
                print('File found in cache')
                
            except:
                packet = self.makePacket(request)
                lengthstr=str(len(packet))
                print(lengthstr)
                bytesReceived=len(lengthstr)
                print(bytesReceived)
                while bytesReceived<5:
                    lengthstr+=" "
                    bytesReceived+=1
                
                self.s.send(lengthstr.encode("utf-8"))
                self.s.send(packet)
        elif self.method=='POST':
            
            try:
                packet = self.makePacket(request)
            except :
                print('File not Found')
            print(packet)
            lengthstr=str(len(packet))
            print(lengthstr)
            bytesReceived=len(lengthstr)
            print(bytesReceived)
            while bytesReceived<5:
                lengthstr+=" "
                bytesReceived+=1
            
            self.s.send(lengthstr.encode("utf-8"))
            self.s.send(packet)
            self.sendFile(self.fileName)
            
        
        # self.s.close()
    def sendFile(self,fileName):
        with open("clientDatabase"+fileName,"rb") as f:
                fileData=f.read()
                self.s.send(fileData)
                    
                
        return
    def receiveState(self,method,fileName):
        
        if method == 'GET':
            
            packet = self.s.recv(28)
            rawMsg = struct.unpack('8s i 9s i', packet)
            Responsemsg = rawMsg[1]
            header = rawMsg[0].decode('utf-8')+' '+str(rawMsg[1])+' '+rawMsg[2].decode('utf-8')
            print(header)
            if Responsemsg == 200:
                payloadSize = rawMsg[3]
                print(payloadSize)
                f = open("clientDatabase"+fileName, 'wb')
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
                    
                    f.write(data)
                    # print(data.decode('utf-8'))

                f.close()
        elif method =='POST':
            packet = self.s.recv(24)
            rawMsg = struct.unpack('8s i 9s', packet)
            Responsemsg = rawMsg[1]
            header = rawMsg[0].decode('utf-8')+' '+str(rawMsg[1])+' '+rawMsg[2].decode('utf-8')
            print(header)
           
        return
def initConnection():
    try:
        request=""
        with open("requestcomp.txt") as f:
            lines=f.readlines()
            request+=lines[0]
            for i in range(1,len(lines)):
                if(lines[i].split(" ")[0]=="GET") or (lines[i].split(" ")[0]=="POST"):
                    client=Client()
                    client.sendState(request)
                    client.receiveState(client.method,client.fileName)
                    request=lines[i]
                elif(i==len(lines)-1):
                    
                    client=Client()
                    request+=lines[i]
                    client.sendState(request)
                    client.receiveState(client.method,client.fileName)
                else:
                    request+=lines[i]
                
    except:
        print("file not found")


initConnection()