import socket
import sys

def main():
    contacts = {}

    serverSocket = connect()

    while True:
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
                    connectionSocket.close()
                    break
                else:
                    connectionSocket.send("Invalid Input".encode('ascii'))

            connectionSocket.close()

        except socket.error as e:
            print('An error occured:',e)
            connectionSocket.close()
            serverSocket.close()
            sys.exit(1)



def connect():

    #Server Port
    serverPort = 13004

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


def search(connectionSocket, contacts):
    result = ''

    connectionSocket.send("Enter the Search Word: ".encode('ascii'))
    value = connectionSocket.recv(2048).decode('ascii')


    for key, nums in contacts.items():
        if (value in key):
            result += (f"{key:<16}{nums!s}")
            #result += key + ' '*8-len(key) + str(contacts[key]) + '\n'
            continue

        for num in nums:
            if value in num:
                #result += key + ' ' * (8-len(key)) + str(contacts[key]) + '\n'
                result += (f"{key:<16}{nums!s}\n")

                continue

    #print(result)
    connectionSocket.send(result.encode('ascii'))
    return result






main()
