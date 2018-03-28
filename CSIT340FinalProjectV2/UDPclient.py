import socket 

# UDPclient.py

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET specifies IPv4
server_address = ('localhost', 10000) # (serverName,serverPort)

# ____________________Function Definitions______________________________

#This function lets the user enter a mathematical expression 
def enter_expression():
	expression = input("Math expression ---> ")
	return expression 

#This function sends a message to the servers (request)
def send_message(message):
    #send the  expression to server for calculation
    sock.sendto(message.encode(), server_address)  # this was tied to an unused variable sent, I deleted) -TK
    
    #receive a response from server
    message, server = sock.recvfrom(4096)  # server = unused variable??
    print(message.decode())
        
def check_type(entry):
    if(type(entry) == int):
        return True 
    else:
        return False

#Display menu 
def menu():
    print("1.Enter a math expression")
    print("2.Exit")
    while True:
        try:
            choice = int(input('Choose a menu option --->'))
            while(choice<1 or choice>2):  # loop until user meets input parameters
                print("That's not a valid option!")
                choice = int(input('Choose a menu option --->'))
            return choice
        except:         # catch input exception
            print("That's not a valid option!")
        

#________________________________________________________________________

user_choice = menu()   #Allow user to make a choice 

while(user_choice == 1 ):  #Let user enter a mathematical expression 
    message = enter_expression()
    send_message(message)
    user_choice = menu()
    
if(user_choice == 2): #if the user prefers to exit out, display a goodbye message
    print("Goodbye....!!!")
    sock.close()  # close socket if user terminates program
