from socket import *
import threading
import time
import sys
import traceback
import errno
import math

## global variables
tList = []

from maingame import compare_hands, evaluate_hand
import random

Deck = [] #Holds all cards for gameplay
Flop = []
Hand1 = [] 	#Player 1
Hand2 = []	#Player 2
Hand3 = []	#Player 3
Hand4 = []  #Player 4
Hand5 = [] 	#Player 5
Hand6 = []	#Player 6
Hand7 = []	#Player 7
Hand8 = []  #Player 8

'''
Player1 = False
Player2 = False
Player3 = False
Player4 = False
Player5 = False
Player6 = False
Player7 = False
Player8 = False
'''

numPlayers = 8

'''
numPlayers = int(sys.argv[1]) #Number of players required for gameplay to begin

if (numPlayers < 2):
    print("ERROR: Must be more than 1 player")
    sys.exit(0)
'''
    
class Card(object):

	def __init__(self,value,suit):
		if ( suit == 1 ):
			suit = "Clubs"
		elif ( suit == 2 ):
			suit = "Diamonds"
		elif ( suit == 3 ):
			suit = "Hearts"
		elif ( suit == 4 ):
			suit = "Spades"

		if ( value == 11 ):
			value = "J"
		elif ( value == 12 ):
			value = "Q"
		elif ( value == 13 ):
			value = "K"
		elif ( value == 14 ):
			value = "A"

		self.value = value
		self.suit = suit

		tuple_val = value
		if ( value == 10 ):
			tuple_val = "T"
		self.tuple = str(tuple_val)+suit[0:1]

		#print("Creating card: ",self.value, "\t", self.suit)

	def __str__(self):
		return (str(self.value) + " of " + self.suit)

def createDeck():
	for i in range(1,5):	#suits
		for j in range(2,15): #cards
			#Create Object here
			Deck.append(Card(j,i))

def resetGame():
    #Clear Game
    del Deck[:]
    
    del Hand1[:]
    del Hand2[:]
    del Hand3[:]
    del Hand4[:]    
    del Hand5[:]
    del Hand6[:]
    del Hand7[:]
    del Hand8[:]     
    
    del Flop[:]
	
    with clients_lock:
        for c in clients:
            c.send("RESET".encode())
	
    time.sleep(0.5)

    createDeck()
    random.shuffle(Deck)
    #generateHands()    
	
    time.sleep(3)
	
    bettingRound(1) #TEMP Simulate second round gameplay
    time.sleep(6)
    bettingRound(2)
    time.sleep(6)
    bettingRound(3)
    time.sleep(6)
    bettingRound(4)
    time.sleep(6)
	
    resetGame()
	
	#Clear the deck, all player hands, and regenerate everything!

def generateHands(PlayerCards): #Include value i for # of active players
    if ( PlayerCards == "P1" ):
        for i in range(0,2):
            Hand1.append(Deck.pop(0))
    if ( PlayerCards == "P2" ):            
        for i in range(0,2):
            Hand2.append(Deck.pop(0))
    if ( PlayerCards == "P3" ):              
        for i in range(0,2):
            Hand3.append(Deck.pop(0))
    if ( PlayerCards == "P4" ):              
        for i in range(0,2):
            Hand4.append(Deck.pop(0))
    if ( PlayerCards == "P5" ):              
        for i in range(0,2):
            Hand5.append(Deck.pop(0))
    if ( PlayerCards == "P6" ):              
        for i in range(0,2):
            Hand6.append(Deck.pop(0))
    if ( PlayerCards == "P7" ):              
        for i in range(0,2):
            Hand7.append(Deck.pop(0))
    if ( PlayerCards == "P8" ):              
        for i in range(0,2):
            Hand8.append(Deck.pop(0))    
        
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

def Broadcast_Message(message):
    with clients_lock:
        for c in clients:
            c.send(message.encode())       

global allActions      
 
global p1_action
global p2_action
global p3_action
global p4_action
global p5_action
global p6_action
global p7_action
global p8_action

p1_action = False
p2_action = False  
p3_action = False
p4_action = False  
p5_action = False
p6_action = False  
p7_action = False
p8_action = False 

allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)
   
def ResetActions():   
    global allActions 
    global p1_action
    global p2_action
    global p3_action
    global p4_action
    global p5_action
    global p6_action
    global p7_action
    global p8_action 
    
    p1_action = False
    p2_action = False  
    p3_action = False
    p4_action = False  
    p5_action = False
    p6_action = False  
    p7_action = False
    p8_action = False 
    allActions = False
    
def bettingRound(bettingRoundNum):
    global winMessage
    
    global allActions 
    
    global p1_action
    global p2_action
    global p3_action
    global p4_action
    global p5_action
    global p6_action
    global p7_action
    global p8_action 
    
    p1_action = False
    p2_action = False  
    p3_action = False
    p4_action = False  
    p5_action = False
    p6_action = False  
    p7_action = False
    p8_action = False 
    
    if  ( bettingRoundNum == 1 ):
		#TAKE BETS
        print("Taking bets")
        time.sleep(3)
        
        winMessage = "Place your bets!"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg) 
                
        #TEMP: (Concept)   
        time.sleep(1)
        while ( allActions != True ):
            #print(allActions)
            time.sleep(0.1)
        ResetActions()
            
        time.sleep(2)

        winMessage = "Pre Flop Bet Complete"
        print("Pre-flop Bet Complete")
        
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)       

        
        generateFlop()
    elif ( bettingRoundNum == 2 ):
        Deck.pop(0) #"Burn" top card

        for index, x in enumerate(Flop):
            data = 'FLOP[' + str(index) +']:'+ str(x)
            print (data)
            with clients_lock:
                for c in clients:
                    c.send(data.encode())
                    time.sleep(0.5)

		#TAKE BETS
        print("Taking bets")
        
        winMessage = "Place your bets!"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg) 
        
        #TEMP: (Concept)   
        time.sleep(1)
        while ( allActions != True ):
            #print(allActions)
            time.sleep(0.1)
        ResetActions()
            
        time.sleep(2)

        winMessage = "Flop Bet Complete"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)         
        print("Flop Bet Complete")
        
    elif ( bettingRoundNum == 3 ):
        generateTurn()
        #setCardFileNames(2)
        Turn = str(Flop[3])
        data = 'TURN:'+ Turn
        print (data)
        with clients_lock:
            for c in clients:
                c.send(data.encode())
                time.sleep(0.5)
		#TAKE BETS
        print("Taking bets")
        
        winMessage = "Place your bets!"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg) 
        
        #TEMP: (Concept)   
        time.sleep(1)
        while ( allActions != True ):
            #print(allActions)
            time.sleep(0.1)
        ResetActions()
            
        time.sleep(2)

        winMessage = "Turn Bet Complete"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)           
        
        print("Turn Bet Complete")
        
    elif ( bettingRoundNum == 4 ):
        generateRiver()

        River = str(Flop[4])
        data = 'RIVER:'+ River
        
        print (data)
        with clients_lock:
            for c in clients:
                c.send(data.encode())
                time.sleep(0.5)
                
		#TAKE BETS
        print("Taking bets")
        
        winMessage = "Taking Bets"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)           
 
        #TEMP: (Concept)   
        time.sleep(1)
        while ( allActions != True ):
            #print(allActions)
            time.sleep(0.1)
        ResetActions()
            
        time.sleep(2)

        winMessage = "Bets complete! Reveal Cards!"
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)           
        
        print("River Bet Complete. Reveal cards!")

        time.sleep(2)
		
        P1 = []
        for x in Hand1:
            P1.append(x.tuple)
        for x in Flop:
            P1.append(x.tuple)

        P2 = []
        for x in Hand2:
            P2.append(x.tuple)
        for x in Flop:
            P2.append(x.tuple)
            
        P3 = []
        for x in Hand3:
            P3.append(x.tuple)
        for x in Flop:
            P3.append(x.tuple)    
            
        P4 = []
        for x in Hand4:
            P4.append(x.tuple)
        for x in Flop:
            P4.append(x.tuple)  

        P5 = []
        for x in Hand5:
            P5.append(x.tuple)
        for x in Flop:
            P5.append(x.tuple)  

        P6 = []
        for x in Hand6:
            P6.append(x.tuple)
        for x in Flop:
            P6.append(x.tuple)  

        P7 = []
        for x in Hand7:
            P7.append(x.tuple)
        for x in Flop:
            P7.append(x.tuple)  

        P8 = []
        for x in Hand8:
            P8.append(x.tuple)
        for x in Flop:
            P8.append(x.tuple)              

        print("\n")

        V1 = evaluate_hand(P1)[2]
        V2 = evaluate_hand(P2)[2]
        V3 = evaluate_hand(P3)[2]
        V4 = evaluate_hand(P4)[2]
        V5 = evaluate_hand(P5)[2]
        V6 = evaluate_hand(P6)[2]
        V7 = evaluate_hand(P7)[2]
        V8 = evaluate_hand(P8)[2]
        
        if (V1 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 1 Wins with ",evaluate_hand(P1)[0])
            winMessage = "Player 1 Wins with "+evaluate_hand(P1)[0]
            
            data = "P1Cards:"+str(Hand1[0])+"\n"+str(Hand1[1])
            Broadcast_Message(data)
            
        elif (V2 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 2 Wins with ",evaluate_hand(P2)[0]) 
            winMessage = "Player 2 Wins with "+evaluate_hand(P2)[0]
            
            data = "P2Cards:"+str(Hand2[0])+"\n"+str(Hand2[1])
            Broadcast_Message(data)
            
        elif (V3 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 3 Wins with ",evaluate_hand(P3)[0]) 
            winMessage = "Player 3 Wins with "+evaluate_hand(P3)[0]
            
            data = "P3Cards:"+str(Hand3[0])+"\n"+str(Hand3[1])
            Broadcast_Message(data)
            
        elif (V4 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 4 Wins with ",evaluate_hand(P4)[0]) 
            winMessage = "Player 4 Wins with "+evaluate_hand(P4)[0]
            
            data = "P4Cards:"+str(Hand4[0])+"\n"+str(Hand4[1])
            Broadcast_Message(data)
            
        elif (V5 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 5 Wins with ",evaluate_hand(P5)[0]) 
            winMessage = "Player 5 Wins with "+evaluate_hand(P5)[0]
            
            data = "P5Cards:"+str(Hand5[0])+"\n"+str(Hand5[1])
            Broadcast_Message(data)
            
        elif (V6 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 6 Wins with ",evaluate_hand(P6)[0]) 
            winMessage = "Player 6 Wins with "+evaluate_hand(P6)[0]
            
            data = "P6Cards:"+str(Hand6[0])+"\n"+str(Hand6[1])
            Broadcast_Message(data)
            
        elif (V7 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 7 Wins with ",evaluate_hand(P7)[0]) 
            winMessage = "Player 7 Wins with "+evaluate_hand(P7)[0]
            
            data = "P7Cards:"+str(Hand7[0])+"\n"+str(Hand7[1])
            Broadcast_Message(data)            
        elif (V8 == max(V1,V2,V3,V4,V5,V6,V7,V8) ):
            print("Player 8 Wins with ",evaluate_hand(P8)[0]) 
            winMessage = "Player 8 Wins with "+evaluate_hand(P8)[0]
            
            data = "P8Cards:"+str(Hand8[0])+"\n"+str(Hand8[1])
            Broadcast_Message(data)            

            
        del P1[:]
        del P2[:]
        del P3[:]
        del P4[:]
        del P5[:]
        del P6[:]
        del P7[:]
        del P8[:]     

        
        time.sleep(0.5)
		#Send win message to clients
        game_msg = "GAME_MSG:"+winMessage
        Broadcast_Message(game_msg)   

# And calls to holdem_main
clients = set()
clients_lock = threading.Lock()
def clientThread(connectionSocket, addr):
    print ("Accepted connection from: ", addr)
    with clients_lock:
        clients.add(connectionSocket)
    try:
        print ("Thread Client Entering Now...")
        print (addr)
        stra = threading.local()
        strb = threading.local()
        pBet = threading.local() #BET
        pCheck = threading.local() #CHECK
        pFold = threading.local() #FOLD
        strm = threading.local()
        while True:
            #print ("TID = ",threading.current_thread())
            msg = connectionSocket.recv(1024).decode()
        #    print ("--> ",msg[0:5])
            global allActions
            global p1_action
            global p2_action
            global p3_action
            global p4_action
            global p5_action
            global p6_action
            global p7_action
            global p8_action
                
            if (msg[0:5] == "HELLO" or msg[0:7] == "REQUEST"):
			
                #Just a timer to ensure we send it after initialCards is called
                time.sleep(2)
				
                if ( msg[0:7] == "HELLO"):
                    stra = "Hello Player ["
                    stra += str(addr[0])
                    stra += ":"
                    stra += str(addr[1])
                    stra += "]"
                    print(stra)
                    print ("TID = ",threading.current_thread())
                else:
                    stra = "--New Game--"
                
                connectionSocket.send(stra.encode())

                if( "Thread-2" in str(threading.current_thread()) ):
                    #for x in Hand1:
                    generateHands("P1")
                    
                    data = "P1Cards:"+str(Hand1[0])+"\n" + "P1Cards:"+str(Hand1[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-3" in str(threading.current_thread()) ):
                    #for x in Hand2:
                    generateHands("P2")
                    
                    data = "P2Cards:"+str(Hand2[0])+"\n" + "P2Cards:"+str(Hand2[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-4" in str(threading.current_thread()) ):
                    #for x in Hand3:
                    generateHands("P3")
                    
                    data = "P3Cards:"+str(Hand3[0])+"\n" + "P3Cards:"+str(Hand3[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-5" in str(threading.current_thread()) ):
                    #for x in Hand4:
                    generateHands("P4")
                    
                    data = "P4Cards:"+str(Hand4[0])+"\n" + "P4Cards:"+str(Hand4[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-6" in str(threading.current_thread()) ):
                    #for x in Hand5:
                    generateHands("P5")
                    
                    data = "P5Cards:"+str(Hand5[0])+"\n" + "P5Cards:"+str(Hand5[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-7" in str(threading.current_thread()) ):
                    #for x in Hand6:
                    generateHands("P6")
                    
                    data = "P6Cards:"+str(Hand6[0])+"\n" + "P6Cards:"+str(Hand6[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-8" in str(threading.current_thread()) ):
                    #for x in Hand7:
                    generateHands("P7")
                    
                    data = "P7Cards:"+str(Hand7[0])+"\n" + "P7Cards:"+str(Hand7[1])
                    connectionSocket.send(data.encode())
                elif( "Thread-9" in str(threading.current_thread()) ):
                    #for x in Hand8:
                    generateHands("P8")
                    
                    data = "P8Cards:"+str(Hand8[0])+"\n" + "P8Cards:"+str(Hand8[1])
                    connectionSocket.send(data.encode())                        
            elif (msg[0:3] == "BYE"):
                strb = "Goodbye Client ["
                strb += str(addr[0])
                strb += ":"
                strb += str(addr[1])
                strb += "]"
                print(strb)
                connectionSocket.send(strb.encode())
                connectionSocket.close()
                return
            elif (msg[0:4] == "CALL"):
                pBet = "Player Called ["
                pBet += str(addr[0])
                pBet += ":"
                pBet += str(addr[1])
                pBet += "]"
                print(pBet)
                print ("TID = ",threading.current_thread())
                with clients_lock:
                    for c in clients:
                            c.send(pBet.encode())                            
                
                if ( "Thread-2" in str(threading.current_thread()) ):
                    p1_action = True
                elif ( "Thread-3" in str(threading.current_thread()) ):
                    p2_action = True       
                elif ( "Thread-4" in str(threading.current_thread()) ):
                    p3_action = True
                elif ( "Thread-5" in str(threading.current_thread()) ):
                    p4_action = True              
                elif ( "Thread-6" in str(threading.current_thread()) ):
                    p5_action = True
                elif ( "Thread-7" in str(threading.current_thread()) ):
                    p6_action = True     
                elif ( "Thread-8" in str(threading.current_thread()) ):
                    p7_action = True
                elif ( "Thread-9" in str(threading.current_thread()) ):
                    p8_action = True
                    
                allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)                   
                    
                            #c.sendall("Second message".encode())
            elif (msg[0:5] == "RAISE"):
                pBet = "Player Raised ["
                pBet += str(addr[0])
                pBet += ":"
                pBet += str(addr[1])
                pBet += "]"
                print(pBet)
                print ("TID = ",threading.current_thread())
                with clients_lock:
                    for c in clients:
                            c.send(pBet.encode())                            
                
                if ( "Thread-2" in str(threading.current_thread()) ):
                    p1_action = True
                elif ( "Thread-3" in str(threading.current_thread()) ):
                    p2_action = True       
                elif ( "Thread-4" in str(threading.current_thread()) ):
                    p3_action = True
                elif ( "Thread-5" in str(threading.current_thread()) ):
                    p4_action = True              
                elif ( "Thread-6" in str(threading.current_thread()) ):
                    p5_action = True
                elif ( "Thread-7" in str(threading.current_thread()) ):
                    p6_action = True     
                elif ( "Thread-8" in str(threading.current_thread()) ):
                    p7_action = True
                elif ( "Thread-9" in str(threading.current_thread()) ):
                    p8_action = True
                    
                allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)                   
                    
                            #c.sendall("Second message".encode())                            
            elif (msg[0:3] == "BET"):
                pBet = "Placed Bet ["
                pBet += str(addr[0])
                pBet += ":"
                pBet += str(addr[1])
                pBet += "]"
                print(pBet)
                print ("TID = ",threading.current_thread())
                with clients_lock:
                    for c in clients:
                            c.send(pBet.encode())                            
                
                if ( "Thread-2" in str(threading.current_thread()) ):
                    p1_action = True
                elif ( "Thread-3" in str(threading.current_thread()) ):
                    p2_action = True       
                elif ( "Thread-4" in str(threading.current_thread()) ):
                    p3_action = True
                elif ( "Thread-5" in str(threading.current_thread()) ):
                    p4_action = True              
                elif ( "Thread-6" in str(threading.current_thread()) ):
                    p5_action = True
                elif ( "Thread-7" in str(threading.current_thread()) ):
                    p6_action = True     
                elif ( "Thread-8" in str(threading.current_thread()) ):
                    p7_action = True
                elif ( "Thread-9" in str(threading.current_thread()) ):
                    p8_action = True
                    
                allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)                   
                    
                            #c.sendall("Second message".encode())
            elif (msg[0:5] == "CHECK"):
                pCheck = "Player Checked ["
                pCheck += str(addr[0])
                pCheck += ":"
                pCheck += str(addr[1])
                pCheck += "]"
                print(pCheck)
                #print ("TID = ",threading.current_thread())
                with clients_lock:
                    for c in clients:
                        c.send(pCheck.encode())
                        
                if ( "Thread-2" in str(threading.current_thread()) ):
                    p1_action = True
                elif ( "Thread-3" in str(threading.current_thread()) ):
                    p2_action = True       
                elif ( "Thread-4" in str(threading.current_thread()) ):
                    p3_action = True
                elif ( "Thread-5" in str(threading.current_thread()) ):
                    p4_action = True              
                elif ( "Thread-6" in str(threading.current_thread()) ):
                    p5_action = True
                elif ( "Thread-7" in str(threading.current_thread()) ):
                    p6_action = True     
                elif ( "Thread-8" in str(threading.current_thread()) ):
                    p7_action = True
                elif ( "Thread-9" in str(threading.current_thread()) ):
                    p8_action = True
                    
                allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)                   
                        
            elif (msg[0:4] == "FOLD"):
                pFold = "Player Folds ["
                pFold += str(addr[0])
                pFold += ":"
                pFold += str(addr[1])
                pFold += "]"
                print(pFold)
                #print ("TID = ",threading.current_thread())
                with clients_lock:
                    for c in clients:
                        c.send(pFold.encode())
                        
                if ( "Thread-2" in str(threading.current_thread()) ):
                    p1_action = True
                elif ( "Thread-3" in str(threading.current_thread()) ):
                    p2_action = True       
                elif ( "Thread-4" in str(threading.current_thread()) ):
                    p3_action = True
                elif ( "Thread-5" in str(threading.current_thread()) ):
                    p4_action = True              
                elif ( "Thread-6" in str(threading.current_thread()) ):
                    p5_action = True
                elif ( "Thread-7" in str(threading.current_thread()) ):
                    p6_action = True     
                elif ( "Thread-8" in str(threading.current_thread()) ):
                    p7_action = True
                elif ( "Thread-9" in str(threading.current_thread()) ):
                    p8_action = True
                    
                allActions = (p1_action & p2_action & p3_action & p4_action & p5_action & p6_action & p7_action & p8_action)                   
                        
            else:
                pID = "["
                pID += str(addr[0])
                pID += ":"
                pID += str(addr[1])
                pID += "] - "            
                strm = pID + msg
                print(strm)
                with clients_lock:
                    for c in clients:
                        c.send(strm.encode())
        else:
                strm = "You said what? " + msg
                print(strm)
                connectionSocket.send(strm.encode())

    except OSError as e:
        # A socket error
          print("Socket error:",e)


def joinAll():
    global tList
    for t in tList:
        t.join()

def main():

    #Create deck to start up, and shuffle it
    createDeck()
    random.shuffle(Deck)
    #generateHands()

    try:
        global tList
        serverPort = 12001
        serverSocket = socket(AF_INET,SOCK_STREAM)
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind(('127.0.0.1',serverPort))
        serverSocket.listen(15)
        
        print('The server is ready to receive')

        while True:
        
            connectionSocket, addr = serverSocket.accept()
            t = threading.Thread(target=clientThread,args=(connectionSocket,addr))
            t.start()
            tList.append(t)
            print("Thread started")
            print("Waiting for another connection")
            print(len(tList))
            if ( len(tList) >= numPlayers ): #8 but for now, we test with 3
            
                print("Enough players for gameplay")
                gameBegin = False
                
                #while 1:
                
                if ( gameBegin == False ):
                    print("Game BEGIN")
                                            
                    gameBegin = True
                                            
                    bettingRound(1)

                    time.sleep(6) #TEMP SOLUTION

                    bettingRound(2)

                    time.sleep(6) #TEMP SOLUTION

                    bettingRound(3)

                    time.sleep(6) #TEMP SOLUTION

                    bettingRound(4)
                                            
                    time.sleep(7)
                                            
                    resetGame()

    except KeyboardInterrupt:
        print ("Keyboard Interrupt. Time to say goodbye!!!")
        joinAll()
    #except Exception:
     #   traceback.print_exc(file=sys.stdout)

    print("The end")
    sys.exit(0)
    
##UDP SERVER
UDPserverSocket = socket(AF_INET, SOCK_DGRAM)
UDPserverSocket.bind(('', 12000))       
def udp_ping():
    ##UDP PING BEGIN
    while 1:
        rand = random.randint(0, 10)
        message, address = UDPserverSocket.recvfrom(1024)
        message = message.upper()
        if rand >= 4:
            UDPserverSocket.sendto(message, address)   
    ##UDP PING END        
    
thread_udp = threading.Thread(target=udp_ping, args=())
thread_udp.start() # this causes the thread to run

if __name__ == "__main__":
    # execute only if run as a script
    main()
