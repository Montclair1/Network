import socket
import sys
import threading


host = ''
port = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket Created")

try:
	s.bind((host,port))
except socket.error:
	print("Binding failed")
	sys.exit()
print("Socket has been bounded")

s.listen(8888)

print("Socket is ready")



#This function calculates the math expressions received from the clients
def calculate_expression(message):
    term_list = [] # list of terms 
    op_list = []   # list of operators
    final_result = 0
    start = 0  # placeholder 
    operators = set("+-*/")
    message = message.replace(" ", "") # take out spaces

    for i in range(len(message)):  # separate and store all terms and operators
        if(message[i] in operators):
            term_list.append(message[start:i])  #add term to term list
            op_list.append(message[i])  #add operator to operator list
            start = i+1
        if i == len(message)-1:     # store last term
            term_list.append(message[start:])          

    # Multiplication Calculations
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





#client thread function 
#create a new thread for each client
def clientthread(conn):
	
    message = conn.recv(4096).decode()
    conn.send(str(calculate_expression(message)).encode())

    while True:
        message = conn.recv(4096).decode()
        conn.send(str(calculate_expression(message)).encode())
        if not message:
            break ;
    conn.close()



while 1:
	conn, addr = s.accept()
	print("Connected with + " + addr[0] + str(addr[1]))
	clientthread(conn)  #for each client create a new thread

s.close()  #if there are no more requests close all threads.


