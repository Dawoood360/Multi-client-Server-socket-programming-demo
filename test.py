try:
    with open("ss.png", "rb") as f:
        byte = f.read(1)
        while byte:
            # Do stuff with byte.
            byte = f.read(1)
            print(byte)
except IOError:
     print('Error While Opening the file!')  