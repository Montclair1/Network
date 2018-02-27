
from socket import *


#This function calculates the math expressions received from the clients
def calculate_expression(message):
    term_list = [] # list of terms 
    op_list = []   # list of operators
    final_result = 0
    start = 0  # placeholder 
    operators = set("+-*/")
    message = message.replace(" ", "") # take out spaces
    lastchar=""

    for i in range(len(message)):  # separate and store all terms and operators
        if((lastchar=="" or lastchar=="/" or lastchar=="*" or lastchar=="+" or lastchar=="-") and message[i]=="-"):
            #treat as divided by a negative number
            x=0
        elif(message[i] in operators):
            lastchar=message[i]
            term_list.append(message[start:i])  #add term to term list
            op_list.append(message[i])  #add operator to operator list
            start = i+1
        if i == len(message)-1:     # store last term
            term_list.append(message[start:])          

    # Multiplation Calculations
    for i in range(len(op_list)):
        if op_list[i] == '*':
            term_list[i+1]=float(term_list[i])*float(term_list[i+1])
            term_list[i] = None  # replace first multiplicand with null value
    # delete performed operations/terms        
    while '*' in op_list:     # remove *
        op_list.remove('*')
    while None in term_list:  # remove nulls
        term_list.remove(None)

    # Division Calculations
    for i in range(len(op_list)):
        if op_list[i] == '/':
            term_list[i+1]=float(term_list[i])/float(term_list[i+1])
            term_list[i] = None # replace dividend with null
    # delete performed operations/terms        
    while '/' in op_list:
        op_list.remove('/')    # remove /
    while None in term_list: 
        term_list.remove(None)  # remove nulls

    # Addition and Subtraction Calculations
    for i in range(len(op_list)):  # iteratively add/subtract each term
        if op_list[i] == '+':
            term_list[i+1]=float(term_list[i])+float(term_list[i+1])
        if op_list[i] == '-':
            term_list[i+1]=float(term_list[i])-float(term_list[i+1])
    final_result = term_list[-1]
        
    return final_result 
        
        
        

#send result back to clients 
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 10000))

print("Server is up and running")

while True:
	message, address = serverSocket.recvfrom(4096)
	message_displayed = calculate_expression(message.decode())
	serverSocket.sendto(repr(message_displayed).encode(), address)
