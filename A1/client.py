import time
import random
import struct 
from socket import * 
import sys # In order to terminate the program

#Connecting to server
serverName = 'localhost' #personal server 
#serverName = '34.67.93.93' # prof sever 

#Assign a port number
serverPort = 12000

#Bind the socket to server address and server port
clientSocket = socket(AF_INET, SOCK_DGRAM)


### Prof error check function 
def check_server_response(response):
    data_len, pcode, entity = struct.unpack_from('!IHH', response)
    if pcode == 555:
        response = response[8:]
        print(response.decode())
        sys.exit()
    return


#/////////////////////////////PHASE A////////////////////////////////////
#DATA SENT
#data *sent* to server PHASE A
data = "Hello World!!!. "
packet = data.encode()

#header details in PHASE A
data_length = len(data)
pcode = 0
entity = 1

#Header Packet 
packet_header = struct.pack("!IHH", data_length, pcode, entity)

#header and data packet 
Full_packet = packet_header + packet

#Send packet to server 
#clientSocket.connect((serverName, serverPort))
clientSocket. sendto( Full_packet, (serverName, serverPort))

#print sent packets
print("///////////////////PHASE A/////////////////////")
print("PACKET SENT TO SERVER")
print("Header: ")
print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
print("Data: ")
print("Sentence =", data)
print("\n")


#DATA RECIEVED
#Data *received* from client PHASE A
full_Packet, serverAddress = clientSocket.recvfrom(2048)

#extract data and header from packet 
udp_header = full_Packet[:8]
data = full_Packet[8:]

#unpack data
repeat, udp_port, leng, codeA = struct.unpack("!IIHH",data)
data_len, pcode, entity = struct.unpack("!IHH", udp_header) # must unpack udp header 



#print recieved packets
print("PACKET RECIEVED FROM SERVER")
print("Header: ")
print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
print("Data: ")
print("Repeat =", repeat, "Udp Port =", udp_port, "Length =", leng, "Code A =", codeA)




#/////////////////////////////PHASE B////////////////////////////////////
counter = 0

#print statement
print("///////////////////PHASE B/////////////////////")

#loop for sending packets repeat amount of times
for x in range(repeat):
    #PACKET SENT
    #data
    packet_id = counter 
    data = b'0'*leng
    data_decoded = data.decode()

    #data padding
    padding = leng % 4
    if padding != 0:
        padding = 4 - padding
        data = data + bytearray(padding)

    #header
    pcode = codeA
    entity = 1
    data_length = leng + padding + 4

    #pack packet
    packet_header_B = struct.pack("!IHH", data_length, pcode, entity)
    packet_data_B = struct.pack("!I", packet_id)
    full_Packet_B = packet_header_B + packet_data_B + data

    #send packet to server
    clientSocket.sendto(full_Packet_B, (serverName, udp_port))

    #print sent packets
    print("PACKET SENT TO SERVER")
    print("Header: ")
    print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
    print("Data: ")
    print("Packet ID =", packet_id)
    print("Data =", data_decoded)
    print("\n")

    #resending packets if ack not found
    while True:
        try:
            # Receive acknowledgment packet
            full_Packet_b_1, serverAddress = clientSocket.recvfrom(2048)
            udp_header_b = full_Packet_b_1[:8]
            data_b = full_Packet_b_1[8:]

            udp_header_b = struct.unpack("!IHH", udp_header_b)
            data_b = struct.unpack("!I", data_b)

            packet_ID_ack = data_b[0]

            print("Packet ID Ack: ", packet_ID_ack)
            counter += 1
            break  # Acknowledgment received, exit the loop

        except timeout:
            # Timeout occurred, resend the packet
            print("Timeout: Resending packet with packet_id", packet_id)
            clientSocket.sendto(full_Packet_B, (serverName, udp_port))

    # try:
    #     full_Packet_b_1, serverAddress = clientSocket.recvfrom(2048)
    # except:
    #     counter = counter - 1
    #     continue

    


    #PACKET RECIEVED
    # udp_header_b = full_Packet_b_1[:8]
    # data_b = full_Packet_b_1[8:]

    # udp_header_b = struct.unpack("!IHH", udp_header_b)
    # data_b = struct.unpack("!I", data_b)

    # packet_ID_ack = data_b[0]

    # print("Packet ID Ack: ", packet_ID_ack)
    # counter= counter + 1

"""
if packet_ID_ack != packet_id:
    print("sending again.....")
    clientSocket. sendto(full_Packet_B, (serverName, udp_port))
else:
    print("correct ID")

"""
#####Pseudo code for resend if timer catches 
"""
while true:
    settimeout(5)
    listen to server
    if timeout has hit zero 
        send packet again "repeat" amount of times 
    else
        break 

"""


print("here")

full_Packet_b_2, serverAddress = clientSocket.recvfrom(2048)
print("b2 len: ", len(full_Packet_b_2))
### SEPERATE DATA FROM HEADER BY BYTES 
udp_header = full_Packet_b_2[:8]
data = full_Packet_b_2[8:]

print('From server Data: ', struct.unpack("!II",data)) # must unpack data *testing purposes* 
print('From server header: ', struct.unpack("!IHH",udp_header)) # must unpack data *testing purposes*

check_server_response(full_Packet_b_2) #Prof check error 

data_len, pcode, entity = struct.unpack("!IHH", udp_header) # must unpack udp header 
tcp_port, codeB = struct.unpack("!II",data)

#testing purposes
print("TCP Port: ", tcp_port, "\nCode B: ", codeB)




#########################################################
########### PHASE C and D TCP PART ######################
#########################################################
time.sleep(5)
serverName = 'localhost' #personal server
#serverName = '34.67.93.93'
# Assign a port number
serverPort = tcp_port

# Bind the socket to server address and server port
TclientSocket = socket(AF_INET, SOCK_STREAM)
TclientSocket.connect((serverName, serverPort))


#Phase C

#Recieve from server
serverResponse = TclientSocket.recv(1024)

#Extract info based on bytes
header = serverResponse[:8]
tcp_data = serverResponse[8:]

#Unpack response from server
headerUnpack = struct.unpack("!IHH", header)
tcp_dataUnpack = struct.unpack("!IHHc", tcp_data)

#Assign server response to values
data_length, pcode, server_entity = headerUnpack
repeat2, len2, codeC, char = tcp_dataUnpack
char = char.decode()

#print server response
print("Header:")
print("Data Length = ", data_length)
print("Pcode = ",pcode)
print("Entity = ",server_entity)
print("Data: ")
print("Repeat2 = ",repeat2)
print("Len2 = ",len2)
print("CodeC = ",codeC)
print("Char = ",char)



padding = len2 % 4
if padding != 0:
    padding = 4 - padding


print("\n")

#Phase D
#Phase D data
#Sending repeat2 pacts to server
for i in range(repeat2):
    data_PD = char * (len2 + padding)
    print("data_PD: ", data_PD)
    print("padded len2 : ", len2+padding)
    data_PD_encoded = data_PD.encode()
    data_length = len(data_PD)
    print("data len: ", data_length)
    pcode = codeC
    print("Pcode: ",pcode)
    entity = 1
    fullPacket = struct.pack("!IHH", data_length, pcode, entity) + data_PD_encoded
    TclientSocket.send(fullPacket)
    #time.sleep(0.1)  # Sleep for a short interval to allow the server to process the packet



serverResponse = TclientSocket.recv(1024)
print(serverResponse)

tcp_header = serverResponse[:8]
data = serverResponse[8:]

header = struct.unpack("!IHH", tcp_header)
data = struct.unpack("!I", data)

print("Header: ", header)

print("Code D: ", data[0])

print("\nProcess Completed. Terminating Client......\n")

#server wait time



#close client

TclientSocket.close()
