import socket
from threading import Thread
from SocketServer import ThreadingMixIn

#NOT TRANSFORMED 
class ClientThread(Thread):
 
    def __init__(self,ip,port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for "+ip+":"+str(port)
 
 
    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print "received data:", data
            conn.send(data)  # echo

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



#This function calculates the math expressions received from the clients
def calculate_expression(message):
    term_list = [] # list of terms 
    op_list = []   # list of operators
    final_result = 0
    start = 0  # placeholder 
    operators = set("+-*/")
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

#Network Connection

#GEEK
#TCP_IP = '0.0.0.0'
#TCP_PORT = 62
#BUFFER_SIZE = 20  # Normally 1024, but we want fast response
 
serverPort=10000
serverSocket=socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#NEW
serverSocket.bind(('',serverPort)) # bind socket to server address
threads = []
#serverSocket.listen(1)  # listen for incoming connections
print("Server is ready")

#GEEK
#tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#tcpsock.bind((TCP_IP, TCP_PORT))
#threads = []
 
##while True:
##    tcpsock.listen(4) # # of threads? How do we chose or make different for diff computers?
##    print "Waiting for incoming connections..."
##    (conn, (ip,port)) = tcpsock.accept()
##    newthread = ClientThread(ip,port)
##    newthread.start()
##    threads.append(newthread)
 
for t in threads:  # WHERE BELOW DO WE PUT JOIN??? I DONT THINK IT CAN GO IN LOOP
    ##DO WE NEED IT???
    t.join()

while True:
    connectionSocket.listen(4) # # of threads? How do we chose or make different for diff computers?
    print("Waiting for incoming queries")
    connectionSocket,address=serverSocket.accept()
    newthread = ClientThread(connectionSocket,address)#is this good?
    newthread.start()
    threads.append(newthread)
    try:
        while True:
            message = connectionSocket.recv(4096).decode()
            if message:  # if message exists, calculate expression
                message_displayed=calc_expr_par(message) # evaluate parentheses first
                connectionSocket.sendto(repr(message_displayed).encode(),address)    
            else:
                break
    finally:                
	#close the connection where there are no more requests
        print("Closing server connection")
        connectionSocket.close()
        exit(0)  # works 3/6/18    
