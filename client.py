from socket import *
import threading

import select


print("client")
serverName = '127.0.0.1'
serverPort = 12001

# create the socket
s = socket(AF_INET, SOCK_STREAM)
s.connect((serverName, serverPort))
print("connected to:", serverName)

#------------------- need 2 threads for handling incoming and outgoing messages--

#       1: create out_buffer:
out_buffer = []

# for incoming data
def incoming():
    while 1:
        data = s.recv(1024)
        if data:
            print("\nReceived:", data.decode())
            data_string = data.decode()
            '''
            if ( "P1Cards:" in data_string ):
                data_string = data_string.replace("P1Cards:", "")
                print(data_string)
            elif ( "P2Cards:" in data_string ):
                data_string = data_string.replace("P2Cards:", "")
                print(data_string)
            '''
#Establish that we have joined
s.send("HELLO".encode())

# now for outgoing data

def outgoing():
    global out_buffer
    while 1:
        user_input=input("Your message: ")+"\n"
        if user_input:
            out_buffer += [user_input.encode()]
#       for i in wlist:
            s.send(out_buffer[0])
            out_buffer = []

thread_in = threading.Thread(target=incoming, args=())
thread_out = threading.Thread(target=outgoing, args=())
thread_in.start() # this causes the thread to run
thread_out.start()
thread_in.join()  # this waits until the thread has completed
thread_out.join()
