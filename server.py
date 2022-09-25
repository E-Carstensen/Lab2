import socket
import sys

def main():
    contacts = {}

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

    print("Server Ready For Connections")

    serverSocket.listen(1)

    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            print(addr, " Has Connected to Socket: ", connectionSocket)
            x  = 0

            while (x != 1):
                #print("Awaiting Message...")
                message = connectionSocket.recv(2048).decode('ascii')

                #print("Message Received: ", message)
                values = message.split('~')


                if (values[0] == '1'):
                    contacts = add_contact(contacts, values[1], values[2])
                    message = ' '.join(contacts[values[1]])

                elif (values[0] == '2'):
                    result = search(contacts, values[1])
                    message = '|'.join(result)

                elif (values[0] == '3'):
                    print("Goodbye.\n")
                    connectionSocket.close()

                    break
                else:
                    print("\n**Operation Not Recognized\n")

                print("Sending Data...")
                sent_size = connectionSocket.send(message.encode('ascii'))
                print(sent_size)

        except socket.error as e:
            print('An error occured:',e)
            connectionSocket.close()
            serverSocket.close()
            sys.exit(1)

def add_contact(contacts, name, num):

    if (name in contacts):
        contacts[name].append(num)
    else:
        contacts[name] = [num]

    return contacts


def search(contacts, value):
    results = []
    for key, nums in contacts.items():
        if (value in key):
            numbers = '~'.join(contacts[key])
            results.append('~'.join([key,numbers]))
            continue

        for num in nums:
            if value in num:
                numbers = '~'.join(contacts[key])
                results.append('~'.join([key,numbers]))
                break

    print(results)

    return results




main()
