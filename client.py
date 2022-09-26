import socket
import sys


def main():

    clientSocket = connect()
    try:
        while (1):
            #Call menu funtion to get user choice and format message
            option = menu()
            clientSocket.send(option.encode('ascii'))

            if (option == '1'):
                add_contact(clientSocket)
            elif(option == '2'):
                search(clientSocket)
            elif(option == '3'):
                disconnect(clientSocket)
                break

    except socket.error as e:
        print("Error:", e)
        clientSocket.close()
        sys.exit(1)


    print("Goodbye")
    clientSocket.close()
    sys.exit(1)



#Displays main menu options, takes input and returns string if input is valid
def menu():

    #Print menu options and take user input
    option = input("""Please select the operation
1)Add a new entry
2)Search
3)Terminate the connection
        """)

    #If input is one of options and only 1 character
    if(option in "123" and len(option) == 1):
        return option
    else:
        #If code makes it this far without returning, the input is invalid
        print("Input Not Recognized")
        #Recursively call menu function
        return menu()




#Take server information from user, initiate socket, and connect to server
#Returns clientSocket object
def connect():
    #Default server information
    serverName = '127.0.0.1'
    serverPort = 13004

    #Take server name from user
    temp = input("Enter the server name or IP address: ")
    if (len(temp) != 0):
        #If user does not enter an address, use default serverName
        serverName = temp

    #Attempt to create client socket with IPv4 and TCP protocols
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Error in client socket creation:',e)
        sys.exit(1)

    #Attempt to connect client port to given server name and port 13000
    try:
        clientSocket.connect((serverName, serverPort))
        print("Welcome to the online phone book. \n")
    except socket.error as e:
        print("Error:", e)
        clientSocket.close()
        sys.exit(1)

    return clientSocket



def search(clientSocket):

    message = clientSocket.recv(2048).decode('ascii')

    val = input(message + ": ")

    clientSocket.send(val.encode('ascii'))

    result = clientSocket.recv(2048).decode('ascii')

    format(result)


def add_contact(clientSocket):

    message = clientSocket.recv(2048).decode('ascii')

    name = input(message)

    clientSocket.send(name.encode('ascii'))

    message = clientSocket.recv(2048).decode('ascii')

    num = input(message)

    clientSocket.send(num.encode('ascii'))



def disconnect(clientSocket):
    clientSocket.send('3'.encode('ascii'))
    clientSocket.close()
    print("Goodbye")
    return


#Format search results to be displayed
def format(temp):
    #Print header text
    print("\n\nName(s):\tPhoneNumber(s):\n")

    #Split result text on key character
    results = temp.split('|')

    #For each contact returned, print all numbers assosiated with it
    for val in results:
        x = val.split('~')
        print(f"{x[0]:16}{x[1:]}")

main()
