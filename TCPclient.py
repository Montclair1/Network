from socket import *

# TCPclient.py 

# ____________________Function Definitions______________________________

#This function let's the user enter a mathematical expression 
def enter_expression():
	print()
	expression = input("Math expression ---> ")
	return expression 

serverName='localhost'
serverPort=10000
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
#This function sends a message to the servers (request)
def send_message(message):
    clientSocket.send(message.encode())
    modifiedMessage=clientSocket.recv(2048) #message length
    print (modifiedMessage.decode())
    print()
    #clientSocket.close()

def check_type(entry):
    if(type(entry) == int):
        return True 
    else:
        return False

#Display a menu 
def menu():
    print("1.Enter a math expression")
    print("2.Exit")
    print()
    while True:
        try:
            choice = int(input('Choose a menu option --->'))
            while(choice<1 or choice>2):  # loop until user meets input parameters
                print()
                print("That's not a valid option!")
                print()
                choice = int(input('Choose a menu option --->'))
                print()
            return choice
        except:         # catch input exception
            print()
            print("That's not a valid option!")
            print()
        
#________________________________________________________________________

user_choice = menu()   #Allow user to make a choice 

while(user_choice == 1):  #Let user enter a mathematical expression 
    message = enter_expression()
    send_message(message)
    user_choice = menu()

if(user_choice == 2): #if the user prefers to exit out, display a goodbye message
    print()
    print("Goodbye....!!!")
    clientSocket.close()