import socket
import sys


def main():

    serverName = '127.0.0.1'
    serverPort = 13000

    #Take server name from user
    serverName = input("Enter the server name or IP address: ")

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

        while (1):
            #Call menu funtion to get user choice and format message
            message = menu()

            #If user chose Disconnect, send server Disconnect message
            if message == False:
                clientSocket.send('3'.encode('ascii'))
                clientSocket.close()
                print("Goodbye")
                return

            #print("Sending Data...")
            sent_size =  clientSocket.send(message.encode('ascii'))
            #print(sent_size, "Bytes sent")

            #print("Awaiting Response... ")
            response = clientSocket.recv(2048).decode('ascii')

            print(response)

            if message.split('~')[0] == '2':
                format(response)





    except socket.error as e:
        print("Error:", e)
        clientSocket.close()
        sys.exit(1)

# Returns a string with the opeation requested and the required values
# joined by a '~' character to diferentiate them
def menu():

    #Print menu options and take user input
    option = input("""Please select the operation
1)Add a new entry
2)Search
3)Terminate the connection
        """)

    #Add Contact
    if (option == '1'):
        #Take name and number for new contact
        name = input("Enter the Name: ")
        num = input("Enter the Phone Number: ")
        #Return 'operation~name~number'
        return '~'.join([option, name, num])
    #Search
    if (option == '2'):
        #Take seach term, can be name or number
        value = input("Enter Search term: ")

        return '~'.join([option, value])

    #Disconnect
    if(option == '3'):

        return False

    #If code makes it this far without returning, the input is invalid
    print("Input Not Recognized")
    #So recursively call menu function
    return menu()

#Format search results to be displayed
def format(temp):
    #Print header text
    print("\n\nName(s):\tPhoneNumber(s):\n")

    #Split result text on key character
    results = temp.split('|')

    #For each contact returned, print all numbers assosiated with it
    for val in results:
        x = val.split('~')
        print(f"{x[0]}         {x[1:]}")



main()
