
from socket import *

def isanum(char):
    nums = set("0123456789")
    if(char in nums):
        return True
    else:
        return False
#This function calculates the math expressions received from the clients
def calculate_expression(message):
    term_list = [] # list of terms 
    op_list = []   # list of operators
    final_result = 0
    start = 0  # placeholder 
    operators = set("+-*/")
    message = message.replace(" ", "") # take out spaces
    lastchar=""
    nexneg=False
    i=0
    #print("equation="+message)
    while(i<len(message)):  # separate and store all terms and operators
        if((lastchar=="" or lastchar=="/" or lastchar=="*" or lastchar=="+" or lastchar=="-") and message[i]=="-"):
            #treat - as a negative sign
            nexneg=True
            lastchar=message[i]
            i=i+1
        elif(message[i] in operators):
            lastchar=message[i]
            op_list.append(message[i])  #add operator to operator list
            i=i+1
        elif(message[i]=="("):
            i=i+1
            lastchar=message[i]
            mesg=""
            parencount=1
            while(not parencount==0):
                if(message[i]=="("):
                    parencount+=1
                elif(message[i]==")"):
                    parencount-=1
                if(not parencount==0):
                    #print(message[i])
                    mesg+=message[i]
                lastchar=message[i]
                i=i+1
            nextresult=calculate_expression(mesg)
            #print(nextresult)
            term_list.append(nextresult)
        else:
            num=message[i]
            lastchar=message[i]
            i=i+1
            while((i<len(message)) and isanum(message[i])):
                num+=message[i]
                lastchar=message[i]
                i=i+1
            if(nexneg):
                nexneg=False
                num=float(num)*-1
            term_list.append(num)

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

test="(2+3)*4"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))


test="(2/3)*(4+2)"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="-2+3"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="((5*-2*3)*(4+2))"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="2+3*4"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="3*2-8"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="-2*(3+4)-5"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

test="2+2-1"
print(str(test)+"="+str(calculate_expression(test)))
print(eval(test)==calculate_expression(test))

print("Server is up and running")

while True:
	message, address = serverSocket.recvfrom(4096)
	message_displayed = calculate_expression(message.decode())
	serverSocket.sendto(repr(message_displayed).encode(), address)
