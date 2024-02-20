#import libraries needed for communication with a secure email server
from socket import *
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.base64mime import body_encode as encode_base64

#main function
def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password

#auth object
def auth_plain(sender_email, password):
    """ Authobject to use with PLAIN authentication. Requires
    self.user and
    self.password to be set."""
    return "\0%s\0%s" % (sender_email, password)

#content of email to be sent
imageHTML = '''
<html>
    <head>
    </head>
    <body>
        <img src = 'https://images.ctfassets.net/ub3bwfd53mwy/5zi8myLobtihb1cWl3tj8L/45a40e66765f26beddf7eeee29f74723/6_Image.jpg?w=750'>
        <img src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Labrador_Retriever_portrait.jpg/435px-Labrador_Retriever_portrait.jpg'>
        <img src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Labrador_Retriever_portrait.jpg/435px-Labrador_Retriever_portrait.jpg'>
    </body>
</html>

'''
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

#email and password
sender_email = sys.argv[1]
password = sys.argv[2]
destination_email = sys.argv[3]

#ensuring correct number of args
if (len(sys.argv) != 4):
    print("Incorrect number of arguments")
    sys.exit(1)

# Choose a mail server (e.g. Google mail server)
mailserver = 'smtp.gmail.com'
mailport= 587

# Make a TCP connection with mailserver and receive the server response
clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.connect((mailserver, mailport))

#check the server response and print it to the screen
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '220':
    print("220 reply not received from server.")

# Send HELO command to the server and print server response. It should be ehlo not helo
heloCommand = 'ehlo [' + mailserver +']\r\n'
print(heloCommand)
clientsocket.send(heloCommand.encode())

#ehlo response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '250':
    print("250 reply not received from server.")

# Send STARTTLS command and print server response.
startCommand = 'STARTTLS \r\n'
print(startCommand)
clientsocket.send(startCommand.encode())

#STARTTLS response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '220':
    print("220 reply not received from server.")
else:
# wrap the socket you created earlier in a ssl context. Assuming you
# named you socket, clientSocket, you can use the following two lines
# to do so:
    context = ssl.create_default_context()
    clientsocket = context.wrap_socket(clientsocket, server_hostname=mailserver)

#AUTH command sent
authCommand = 'AUTH PLAIN\r\n'
print(authCommand)
clientsocket.send(authCommand.encode())

#AUTH response back
response = clientsocket.recv(1024).decode()
print(response)

#encoding to base64
loginInfo = auth_plain(sender_email, password)
base64_loginInfo = encode_base64(loginInfo.encode('ascii'), eol = '') + '\r\n'

#sending login info
print(base64_loginInfo)
clientsocket.send(base64_loginInfo.encode())

#login info response code
response = clientsocket.recv(1024).decode()
print(response)

#mail command sent
mailCommand = 'MAIL FROM: <'+ sender_email +'>\r\n'
print(mailCommand)
clientsocket.send(mailCommand.encode())

#mail response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '250':
    print("250 reply not received from server.")

#recp command sent
rcptCommand = 'RCPT TO: <'+ destination_email +'>\r\n'
print(rcptCommand)
clientsocket.send(rcptCommand.encode())

#recp response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '250':
    print("250 reply not received from server.")

#data command sent
dataCommand = 'DATA \r\n'
print(dataCommand)
clientsocket.send(dataCommand.encode())

#data response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '354':
    print("354 reply not received from server.")

#content created
data = MIMEMultipart()
data['Subject'] = 'SMPT Test'
data.attach(MIMEText(msg, 'plain'))
data.attach(MIMEText(imageHTML, 'html'))
image_string = data.as_string()

#content sent
clientsocket.send(image_string.encode())
clientsocket.send(endmsg.encode())
print(image_string)
print(endmsg)

#sent response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '250':
    print("250 reply not received from server.")

#quit command sent
quitCommand = 'QUIT \r\n'
print(quitCommand)
clientsocket.send(quitCommand.encode())

#quit response back
response = clientsocket.recv(1024).decode()
print(response)
if response[:3] != '221':
    print("221 reply not received from server.")

# Close the connection
clientsocket.close()
