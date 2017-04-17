#Each instance of this serves as a client

import sys
import random
import time
from socket import *
import threading
import select
from maingame import compare_hands
from pygame import mixer
from random import randint

deckBackImg = "./DECK/deck_back.png" #-- Default image

print("client")

#Lets get arguments for this..

serverName = sys.argv[1]
serverPort = int(sys.argv[2]) #Default 12001

# create the socket
s = socket(AF_INET, SOCK_STREAM)
s.connect((serverName, serverPort))
print("connected to:", serverName)

#------------------- need 2 threads for handling incoming and outgoing messages--

#       1: create out_buffer:
out_buffer = []

def setInitialCardFileNames():
	global winMessage
	winMessage = "No Game"

	global P1_Card1
	global P1_Card2
    
	global P2_Card1
	global P2_Card2

	global P3_Card1
	global P3_Card2
    
	global P4_Card1
	global P4_Card2
    
	global P5_Card1
	global P5_Card2
    
	global P6_Card1
	global P6_Card2

	global P7_Card1
	global P7_Card2
    
	global P8_Card1
	global P8_Card2
    
	global Flop_Card1
	global Flop_Card2
	global Flop_Card3
	global Flop_Card4
	global Flop_Card5

	P1_Card1 = deckBackImg
	P1_Card2 = deckBackImg
    
	P2_Card1 = deckBackImg
	P2_Card2 = deckBackImg
    
	P3_Card1 = deckBackImg
	P3_Card2 = deckBackImg
    
	P4_Card1 = deckBackImg
	P4_Card2 = deckBackImg
    
	P5_Card1 = deckBackImg
	P5_Card2 = deckBackImg
    
	P6_Card1 = deckBackImg
	P6_Card2 = deckBackImg 
    
	P7_Card1 = deckBackImg
	P7_Card2 = deckBackImg
    
	P8_Card1 = deckBackImg
	P8_Card2 = deckBackImg   

	Flop_Card1 = deckBackImg
	Flop_Card2 = deckBackImg
	Flop_Card3 = deckBackImg
	Flop_Card4 = deckBackImg
	Flop_Card5 = deckBackImg
	
	print("Set Initial Card File Names")

def generateFlop():
	print("Flop")
	Flop.append(Deck.pop(0))
	Flop.append(Deck.pop(0))
	Flop.append(Deck.pop(0))
def generateTurn():
	print("Turn")
	Flop.append(Deck.pop(0))
def generateRiver():
	print("River")
	Flop.append(Deck.pop(0))

def test():
	main()
	response = "PLAY"
	clientSocket.send(response.encode());
	sresp = clientSocket.recv((1024))
	print("server says: %s",sresp.decode())

clientSocket = socket(AF_INET,SOCK_STREAM)

def playerCheck():
    user_input = "CHECK"
    outgoing(user_input)

def playerFold():
    user_input = "FOLD"
    outgoing(user_input)

def playerRaise():
    user_input = "RAISE"
    outgoing(user_input)

def playerCall():
    user_input = "CALL"
    outgoing(user_input)    
    
betCounter = 0
def placeBet(): #TODO: Include bet amount.
    user_input = "BET"
    outgoing(user_input)

def establishConnection():
	clientSocket.connect((serverName,serverPort))
	response = "HELLO"
	clientSocket.send(response.encode());
	sresp = clientSocket.recv((1024))
	print("server says: %s",sresp.decode())

def closeConnection():
	print("Bye user")
	clientSocket.close()

def updateWindow(image_update):
	from holdem_main import updateGUI
	updateGUI(image_update)

def ChatUpdate(message):
	from holdem_main import ChatReceive
	ChatReceive(message)    
    
def main():
    print("Welcome")

#UDP Pinger
def UDP_Pinger():
    while 1:
    
        ##UDP BEGIN
        UDPclientSocket = socket(AF_INET, SOCK_DGRAM)
        UDPclientSocket.settimeout(1)
        message = "Ping: "
        addr = ("127.0.0.1", 12000)

        start = time.time()
        UDPclientSocket.sendto(message.encode(), addr)
        try:
            data, server = UDPclientSocket.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print ('%s %f' % (data, elapsed))
        except timeout:
            print ('REQUEST TIMED OUT')    
        ##UDP END
    
# for incoming data
def incoming():
    while 1:
    
        data = s.recv(1024)
        if data:
            print("\nReceived:", data.decode())
            data_string = data.decode()
            
            #Handle gameplay sounds
            if ( "Player Called" in data_string ):
                mixer.init()
                filename = "./audio/playerCall.wav"
                sound = mixer.Sound(filename)
                mixer.Sound.play(sound)                    
            if ( "Placed Bet" in data_string ):
                mixer.init()
                filename = "./audio/playerBet.wav"
                sound = mixer.Sound(filename)
                mixer.Sound.play(sound)          
            if ( "Player Raised" in data_string ):
                mixer.init()
                filename = "./audio/playerRaise.wav"
                sound = mixer.Sound(filename)
                mixer.Sound.play(sound)    
            if ( "Player Checked" in data_string ):
                mixer.init()
                filename = "./audio/playerCheck.wav"
                sound = mixer.Sound(filename)
                mixer.Sound.play(sound)                    
            if ( "Player Folds" in data_string ):
                mixer.init()
                filename = ["./audio/cardShove1.wav", "./audio/cardShove2.wav", "./audio/cardShove3.wav", "./audio/cardShove4.wav"]
                sound = mixer.Sound(filename[randint(0,3)])
                mixer.Sound.play(sound)                 
            
            if ( "P1Cards:" in data_string ):
                data_string = data_string.replace("P1Cards:", "")
                splitdata = data_string.splitlines()

                global P1_Card1
                global P1_Card2
                P1_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P1_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P1")
            elif ( "P2Cards:" in data_string ):
                data_string = data_string.replace("P2Cards:", "")
                splitdata = data_string.splitlines()

                global P2_Card1
                global P2_Card2
                P2_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P2_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P2")
            elif ( "P3Cards:" in data_string ):
                data_string = data_string.replace("P3Cards:", "")
                splitdata = data_string.splitlines()

                global P3_Card1
                global P3_Card2
                P3_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P3_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P3")
            elif ( "P4Cards:" in data_string ):
                data_string = data_string.replace("P4Cards:", "")
                splitdata = data_string.splitlines()

                global P4_Card1
                global P4_Card2
                P4_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P4_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P4")
            elif ( "P5Cards:" in data_string ):
                data_string = data_string.replace("P5Cards:", "")
                splitdata = data_string.splitlines()

                global P5_Card1
                global P5_Card2
                P5_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P5_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P5")
            elif ( "P6Cards:" in data_string ):
                data_string = data_string.replace("P6Cards:", "")
                splitdata = data_string.splitlines()

                global P6_Card1
                global P6_Card2
                P6_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P6_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P6")
            elif ( "P7Cards:" in data_string ):
                data_string = data_string.replace("P7Cards:", "")
                splitdata = data_string.splitlines()

                global P7_Card1
                global P7_Card2
                P7_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P7_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P7")
            elif ( "P8Cards:" in data_string ):
                data_string = data_string.replace("P8Cards:", "")
                splitdata = data_string.splitlines()

                global P8_Card1
                global P8_Card2
                P8_Card1 = "./DECK/"+str.lower(splitdata[0]).replace(" ", "_")+".png"
                P8_Card2 = "./DECK/"+str.lower(splitdata[1]).replace(" ", "_")+".png"
                splitdata = ""
                updateWindow("P8")                
            elif ( "FLOP[0]:" in data_string ):
                data_string = data_string.replace("FLOP[0]:", "")
                global Flop_Card1
                Flop_Card1 = "./DECK/"+str.lower(data_string).replace(" ", "_")+".png"
                print (Flop_Card1)
                data_string = ""
                updateWindow("F1")
            elif ( "FLOP[1]:" in data_string ):
                data_string = data_string.replace("FLOP[1]:", "")
                global Flop_Card2
                Flop_Card2 = "./DECK/"+str.lower(data_string).replace(" ", "_")+".png"
                print (Flop_Card2)
                data_string = ""
                updateWindow("F2")
            elif ( "FLOP[2]:" in data_string ):
                data_string = data_string.replace("FLOP[2]:", "")
                global Flop_Card3
                Flop_Card3 = "./DECK/"+str.lower(data_string).replace(" ", "_")+".png"
                print (Flop_Card3)
                data_string = ""
                updateWindow("F3")
            elif ( "TURN:" in data_string ):
                data_string = data_string.replace("TURN:", "")
                global Flop_Card4
                Flop_Card4 = "./DECK/"+str.lower(data_string).replace(" ", "_")+".png"
                print (Flop_Card4)
                data_string = ""
                updateWindow("F4")
            elif ( "RIVER:" in data_string ):
                data_string = data_string.replace("RIVER:", "")
                global Flop_Card5
                Flop_Card5 = "./DECK/"+str.lower(data_string).replace(" ", "_")+".png"
                print (Flop_Card5)
                data_string = ""
                updateWindow("F5")
            elif( "GAME_MSG:" in data_string ):
                global winMessage
                winMessage = data_string.replace("GAME_MSG:", "")
                time.sleep(0.5)
                updateWindow("GAME_MSG")
                data_string = ""
            elif( "RESET" in data_string ):
                setInitialCardFileNames()
                updateWindow("ALL")
                outgoing("REQUEST")
                data_string = ""
            else:
                ChatUpdate(data_string)

#Establish that we have joined
s.send("HELLO".encode())

# now for outgoing data -- Modify for chat
def outgoing(user_input):
    global out_buffer

    if user_input:
        out_buffer += [user_input.encode()]

        s.send(out_buffer[0])
        out_buffer = []
        user_input = []

thread_in = threading.Thread(target=incoming, args=())
thread_in.start() # this causes the thread to run

thread_udp = threading.Thread(target=UDP_Pinger, args=())
thread_udp.start() # this causes the thread to run

if __name__ == '__main__':
    main()
