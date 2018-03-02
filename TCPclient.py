from socket import *



# ____________________Function Defenitions______________________________

#This function let's the user enter a mathematical expression 
def enter_expression():
	print()
	expression = input("Math expression ---> ")
	return expression 

#This function sends a message to the servers (request)
def send_message(message):
    serverName='localhost'
    serverPort=10000
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(message.encode())
    modifiedMessage=clientSocket.recv(2048) #message length
    print (modifiedMessage.decode())
    clientSocket.close()

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
            return choice 
            break
        except:
            print()
            print("That's not a valid option!")
        
        

#________________________________________________________________________


user_choice = menu()   #Allow user to make a choice 
while(user_choice < 1 or user_choice > 2):  #If there is a wrong entry display a message indicating that
    print()
    print("That's not a valid option!")
    print()
    user_choice = menu()


while(user_choice == 1 ):  #Let user enter a mathematical expression 
    message = enter_expression()
    send_message(message)
    user_choice = menu()
    
    while(user_choice < 1 or user_choice > 2):  #If there is a wrong entry display a message indicating that 
        print()
        print("That's not a valid option")
        print()
        user_choice = menu()

if(user_choice == 2): #if the user prefers to exit out, display a goodbye message
    print()
    print("Goodbye....!!!")
