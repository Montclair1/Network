from socket import *
from _thread import*
import threading
import sys

# TCPserverMultithread.py
# CJ Conti
# Livio Beqiri
# Thomson Kneeland

# attempt at a multithreaded version of our TCPserver
# program performs repeated outputs using new threads, however, does not exit
# properly, loose threads remain preventing server close

# prevent thread from being accessed
print_lock = threading.Lock()
 
# thread fuction
def threaded(connectionSocket):
    while True:  # data received from TCPclient
        message = connectionSocket.recv(4096).decode()
        if not message:
            #print_lock.release()
            #print("print lock release")
            break    
        if message:  # if message exists, calculate expression
            #print_lock.acquire()
            print("Incoming message")
            thread_id=threading.get_ident()
            print("thread_id is:",thread_id)
            message_displayed=calc_expr_par(message) # evaluate parentheses first
            connectionSocket.sendto(repr(message_displayed).encode(),address)
            #print_lock.release() # trial
            return 0
        #else:
        #   print_lock.release()
        #   print("print lock release")
        #   break
 
    # connection close
    print_lock.release()
    print("closing thread")
    serverSocket.close()
    connectionSocket.close() # Close thread
    #exit()  #alternate exit code
    sys.exit()  #NOT EXITING

# method for parsing any number of parentheses in any order
# NOT INCLUDED : exception if wrong # of parentheses entered by user
def calc_expr_par(input):
    par_list_open = []  # list of elements with "("
    calc ="" # substring for calculating inner parenthetical expression
    result=""
    count=input.count('(')  # count number of opening parentheses in expression
    while (count>0): # loop until all parenthetical expressions eliminated (count =0)
        par_incrementer=0  # variable for referencing opening parentheses
        for j in range(len(input)):
            if input[j] == "(":
                par_list_open.append(j)
                par_incrementer+=1
            elif input[j] == ")":
                count-=1
                par_incrementer-=1
                start = par_list_open[-1] # element with last "("
                parExpr = input[start:j+1] # full expression including parentheses
                expr=input[start+1:j] # expression within parentheses
                calc=str(calculate_expression(expr)) # calculate value inner parentheses
                result=input.replace(parExpr,calc) # replace inner parentheses with calculated value
                input=result
                break
    return calculate_expression(input)  # all parentheses eliminated, calculate final expression        

# Method for exponents
def power(a,b):
    i=0
    result=1
    while(i<b):
        result=result*a
        i=i+1
    return result

#This function calculates the math expressions received from the clients
def calculate_expression(message):
    term_list = [] # list of terms 
    op_list = []   # list of operators
    final_result = 0
    start = 0  # placeholder 
    operators = set("+-*/^")
    message = message.replace(" ", "") # take out spaces
    negative = 1.0 # multiplier for negative values

    if (message[0]=="-"):   # check if first term negative
        negative=-1.0
        message = message[1:]  # delete negative sign from message
    for i in range(len(message)):  # separate and store all terms and operators
        if i == len(message)-1:     # if last digit reached, store last term
            term_list.append(negative*float(message[start:]))
            break
        if(message[i] in operators and message[i+1]=="-"):  # if next term negative
            term_list.append(negative*float(message[start:i]))  #add term to term list
            op_list.append(message[i])  #add operator to operator list
            messageList = list(message)  # replace negative with '0' so it is not operator in next iteration
            messageList[i+1]='0'  
            message="".join(messageList)
            start = i+1  # increment placeholder
            negative = -1.0  # next term is negative
            continue
        elif(message[i] in operators):  # if next term positive
            term_list.append(negative*float(message[start:i]))  #add term to term list
            op_list.append(message[i])  #add operator to operator list
            start = i+1     # increment placeholder     
            negative = 1.0  # next term is positive
            
    # Exponent Calculations
    for i in range(len(op_list)):
        if op_list[i] == '^':
            term_list[i+1]=power(float(term_list[i]),float(term_list[i+1]))
            term_list[i] = None  # replace first multiplicand with null value
    # delete performed operations/terms        
    while '^' in op_list:     # remove ^
        op_list.remove('^')
    while None in term_list:  # remove nulls
        term_list.remove(None)

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

# Network Connection
serverPort=10000 # port number
serverSocket=socket(AF_INET,SOCK_STREAM) # AF_INET = ipv4  SOCK_STREAM - connection oriented TCP protocol
serverSocket.bind(('',serverPort)) # bind socket to server address
serverSocket.listen(1)  # listen for incoming connections
print("Server is ready")
while True:
    connectionSocket,address=serverSocket.accept() # should this be outside loop so we can close connection at end?
    print("Connected to :", address[0], ":", address[1])
    try:
        while True:
            print_lock.acquire() 
            start_new_thread(threaded, (connectionSocket,))  # create new thread, see method above
            start_new_thread(threaded, (connectionSocket,))
            start_new_thread(threaded, (connectionSocket,))
            #t1=threading.Thread(target=threaded,args=(connectionSocket,))
            #t2=threading.Thread(target=threaded,args=(connectionSocket,))
            #t3=threading.Thread(target=threaded,args=(connectionSocket,))
            #t1.start()
            #t2.start()
            #t1.join()
            #t2.join()
            
       
    finally:                
	#close the connection where there are no more requests
        print("Closing server connection")
        #print_lock.release()  # testing
        connectionSocket.close()
        exit()
