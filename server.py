
import socket			
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		
print ("Socket successfully created")

port = 80			


s.bind(('', port))		
print ("socket binded to %s" %(port))


s.listen(5)	
print ("socket is listening")		


while True:


    c, addr = s.accept()	
    print ('Got connection from', addr )

    packet =c.recv(200)
    
    msg=struct.unpack(str(len(packet))+'s',packet)

    print(msg[0].decode("utf-8"))

    
    c.close()

    
    break
