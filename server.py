import socket
import sys

def main():
    contacts = {}

    serverSocket = connect()
    try:
        while 1:
            try:
                connectionSocket, addr = serverSocket.accept()
                #print(addr, " Has Connected to Socket: ", connectionSocket)

                while 1:

                    operation = connectionSocket.recv(2048).decode('ascii')

                    if (operation == '1'):
                        add_contact(connectionSocket, contacts)
                    elif (operation == '2'):
                        search(connectionSocket, contacts)
                    elif (operation == '3'):
                        #connectionSocket.close()
                        break
                    else:
                        connectionSocket.send("Invalid Input".encode('ascii'))

                connectionSocket.close()

            except socket.error as e:
                print('An error occured:',e)
                connectionSocket.close()
                serverSocket.close()
                sys.exit(1)

    except KeyboardInterrupt:
            #connectionSocket.close()
            serverSocket.close()
            sys.exit(1)


#Create and bind server socket, returns serverSocket object
def connect():

    #Server Port
    serverPort = 13000

    #Create socket using IPv4 and TCP protocols
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error Creating Socket: ", e)
        sys.exit(1)

    #Bind Server Socket to chosen port
    try:
        serverSocket.bind(('', serverPort))
    except socket.error as e:
        print("Error Binding Socket: ", e)
        sys.exit(1)

    #Set connection queue to max 1
    serverSocket.listen(1)

    #return serverSocket object
    return serverSocket







def add_contact(connectionSocket, contacts):

    connectionSocket.send("Enter Name: ".encode('ascii'))
    name = connectionSocket.recv(2048).decode('ascii')

    connectionSocket.send("Enter Number: ".encode('ascii'))
    num = connectionSocket.recv(2048).decode('ascii')

    if (name in contacts):
        contacts[name].append(num)
    else:
        contacts[name] = [num]

    return contacts

#Sends prompt and recieves search term
#Returns and sends formatted search result string
def search(connectionSocket, contacts):
    #Define header text
    result = "\n\nName:\tPhoneNumber(s):\n"

    #send client prompt message
    connectionSocket.send("Enter the Search Word: ".encode('ascii'))
    #recieve search term
    value = connectionSocket.recv(2048).decode('ascii')

    #For contact in contact dictionary
    for key, nums in contacts.items():
        #If the search term is in the key
        if (value in key):
            #append formatted information
            result += (f"{key:<13}{nums!s}\n")
            continue
        #For each phone number for this contact
        for num in nums:
            #If the search term is in the phone number
            if value in num:
                #append entire contact, formatted
                result += (f"{key:<13}{nums!s}\n")

                continue
    #Send results to client and return
    connectionSocket.send(result.encode('ascii'))
    return result






main()
