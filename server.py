import socket
import struct
import os


class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
        port = 85
        self.sock.bind(('', port))
        print("socket binded to %s" % (port))
        self.sock.listen(5)
        print("socket is listening")

    def receiveState(self):
        try:
            self.c, addr = self.sock.accept()
            while True:
                packet = self.c.recv(200)
                if not packet:
                    self.c.close()
                    break
                msg = struct.unpack(str(len(packet))+'s', packet)
                msg = msg[0].decode("utf-8")
                self.respondState(msg)
        except KeyboardInterrupt:
            self.c.close()

    def respondState(self, msg):
        data = msg.split(' ')
        if data[0] == 'GET':
            self.getMethod(data)
            # print('Get')
        if data[0] == 'POST':
            for d in data:
                print(d)
            self.postMethod(data)

    def getMethod(self, Msgdata):
        filename = Msgdata[1]
        tokens = filename.split('/')
        filename = tokens[1]
        print(filename)
        try:
            with open(filename) as f:
                lines = f.readlines()
                f.seek(0, os.SEEK_END)
                fileSize = f.tell()
                acceptMsg = 200  # Message Accepted
                packet = struct.pack(
                    '8s i 9s i', b'HTTP/1.0', acceptMsg, b'OK       ', fileSize)
                self.c.send(packet)
                for line in lines:
                    print(line)
                    stringSize = len(line)
                    packet = struct.pack(
                        str(stringSize)+'s', line.encode("utf-8"))
                    self.c.send(packet)
                return
        except:
            msg = 404
            packet = struct.pack('8s i 9s i', b'HTTP/1.0',
                                 msg, b'NOT FOUND', 0)
            self.c.send(packet)
            return

    def postMethod(self, MsgData):
        filename = MsgData[1]
        tokens = filename.split('/')
        filename = 'f'+tokens[1]
        payloadSize = int(MsgData[4])
        try:
            f= open(filename, 'a')
            print('FILE OPENED')
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
                f.write(data.decode('utf-8'))
            f.close()
            msg = 200
            packet = struct.pack(
                '8s i 9s', b'HTTP/1.0', msg, b'OK       ')
            self.c.send(packet)
        except:
            msg = 404
            packet = struct.pack('8s i 9s', b'HTTP/1.0', msg, b'NOT FOUND')
            self.c.send(packet)
            return


server = Server()
server.receiveState()
