
import socket			
import struct
import sys
def initiateConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 80	
    try:		
        s.connect(('127.0.0.1', port))
        return s
    except:
        print("Connection failed")
        sys.exit(0)		

def makePacket(fileName,Method):
    msg=Method+" /"+fileName+" HTTP/1.0 \nHost: reqbin.com"
    stringSize=len(msg)
    packet=struct.pack(str(stringSize)+'s',msg.encode("utf-8"))
    return packet

clientSocket=initiateConnection()
fileName=input("Please enter the file u wish to get")
packet=makePacket(fileName,"GET")

clientSocket.send(packet)
clientSocket.close()	
	
