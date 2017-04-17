PYTHON ONLINE TEXAS HOLD'EM

CNT4713 - (Edward Terry & Sandra Hurtado)

CREDITS:
    AUDIO:
        https://gamesounds.xyz/?dir=Kenney%27s%20Sound%20Pack/Casino
    GRAPHICS:
        https://opengameart.org/content/playing-cards-vector-png
    Hand Evaluation Code:
        https://gist.github.com/imoran21/72d95f223c1f838a827a

This program demonstrates communication between TCP server and clients
for the purpose of sending all gameplay information from the server to
each client. UDP is used for the purpose of pinging active clients to
determine latency. The game also features chat capability over TCP.

USAGE:  python srv.py
            (Dependencies - maingame.py)
        python holdem_main.py   <IP> <PORT>
            (Depencies - chatwindow_support.py, holdem_main_support.py, poker_ref.py)
            
        
GAMEPLAY: 
    
    Begins once table is full (8 players)

    Players are able to see their own cards. 

    First round of betting occurs before flop. All players must make a play.
    3 community cards are then placed on table, sent from the server's deck to each player.
    This continues for both the turn and the river.

    Once the final round of betting takes places, the server evaluates each player's hand
    and determines who the winner is, revealing the winner's cards.

HOW IT WORKS:

    The server creates the deck, shuffling it before generating player hands.
    
    The server then generates hands for every active player. For the flop, turn,
    and river, the server sends messages regarding which cards are to be displayed.
    
    The server sends gameplay specific messages to each player. Player commands
    send a message to server to carry out the corresponsing activity, assigned to
    that client.