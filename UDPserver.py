#implementing the server (UDP)

from socket import *


#This function calculates the math expressions received from the clients
def calculate_expression(message):
    store_integers = [] 
    final_result = 0 
    
    for i in message:
        if(i != ' '):
            store_integers.append(i)  #store the information to a list
            
    #Perform calculations
    if(store_integers[1] =='+'):
        final_result = int(store_integers[0]) + int(store_integers[2])
    if(store_integers[1] =='*'):
        final_result = int(store_integers[0]) * int(store_integers[2])
    if(store_integers[1] =='/'):
        final_result = int(store_integers[0]) / int(store_integers[2])
    if(store_integers[1] =='-'):
        final_result = int(store_integers[0]) - int(store_integers[2])
    
    return final_result 
        
        
        

#send result back to clients 
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 10000))

print("Server is up and running")

while True:
	message, address = serverSocket.recvfrom(4096)
	message_displayed = calculate_expression(message.decode())
	serverSocket.sendto(repr(message_displayed).encode(), address)


