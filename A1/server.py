# Import socket module
import time
import struct
import random
from socket import * 
import sys # In order to terminate the program

#Creates server socket 
#Assign a port number
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))
print('The server is ready to receive')

#serverSocket.settimeout(3) #time out for server 



#/////////////////////////////PHASE A////////////////////////////
#PACKET RECIEVED
#Packet received from Client PHASE A
#Receive packet from cleint within 3 seconds or else close the connection
try:
    serverSocket.settimeout(3)
    full_Packet, clientAddress = serverSocket.recvfrom(1024)
except:
      print("\nClient did not respond fast enough. Terminating Server.....\n")
      serverSocket.close()

if len(full_Packet) % 4 != 0:
    print("\nPacket was not divisible by 4; Terminating Server....\n")
    serverSocket.close()

#extract data
phaseA_header = full_Packet[:8]
phaseA_data = full_Packet[8:]

#unpack data
data_length, pcode, entity = struct.unpack("!IHH", phaseA_header)
sentence = phaseA_data.decode()

#Server Checks for data length, entity and pcode
total_len = len(sentence)
if total_len != data_length:
    print("\nData length did not match actual length of data; Terminating Server....\n")
    serverSocket.close()
elif entity != 1:
    print("Entity does not match expected entity: \n Received: ", entity, "\nExpected: 1\n Terminating Server....\n")
    serverSocket.close()
elif pcode != 0:
    print("P-Code does not match expected P-Code: \n Received: ", pcode, "\nExpected: 0\n Terminating Server....\n")
    serverSocket.close()


#print recieved packets
print("///////////////////PHASE A/////////////////////")
print("PACKET RECIEVED FROM CLIENT")
print("Header: ")
print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
print("Data: ")
print("Sentence =", sentence)
print("\n")


#PACKET SENT
#Data created to SEND to client PHASE A
repeat = random.randint(5, 20)
udp_port = random.randint(20000, 30000)
length = random.randint(50, 100)
codeA = random.randint(100, 400)

#packs data into packet  
packet_data = struct.pack("!IIHH", repeat, udp_port, length, codeA)

#Creates header data
data_length = len(packet_data)
pcode = 0
entity = 2

#packs header into packet 
packet_header = struct.pack("!IHH", data_length, pcode, entity)

#creates full packet by putting header and encoded data together 
Full_Packet = packet_header + packet_data 

#sends a packet back to the client
serverSocket.sendto(Full_Packet, clientAddress)

#print sent data
print("PACKET SENT TO CLIENT")
print("Header: ")
print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
print("Data: ")
print("Repeat =", repeat, "Udp Port =", udp_port, "Length =", length, "Code A =", codeA)

#close socket
serverSocket.close()

#server listens to udp_port
serverPort = udp_port
serverSocket = socket(AF_INET, SOCK_DGRAM)

#Bind the socket to server address and server port
serverSocket.bind(("", serverPort))


#/////////////////////////////PHASE B(B-1)////////////////////////////
#print statement
print("///////////////////PHASE B/////////////////////")
print("PHASE B-1")

#packets are accpeted in repeat times
counter = 0
for x in range(repeat):
	print("packet ", x)
	#PACKET RECIEVED
    #Receive packet from cleint within 3 seconds or else close the connection
	try:
		serverSocket.settimeout(3)
		full_Packet_B1, clientAddress = serverSocket.recvfrom(1024)
	except:
		print("\nClient did not respond fast enough. Terminating Server.....\n")
		serverSocket.close()

	if len(full_Packet_B1) % 4 != 0:
		print("\nPacket was not divisible by 4; Terminating Server....\n")
		serverSocket.close()

	print(len(full_Packet_B1))



	#extract packet
	udp_header_b_1 = full_Packet_B1[:8]
	data_b1 = full_Packet_B1[8:12]
	data = full_Packet_B1[12:]
	data = data.decode()

	#unpack packet
	data_length, p_code, entity = struct.unpack("!IHH", udp_header_b_1)
	packet_id = struct.unpack("!I", data_b1)


    #Server Checks for data length, entity and pcode
	total_len = len(packet_id) + len(data)
	total_len = total_len + (4 - (total_len%4)) #to account for padding 
	print("Total Len: ", total_len)
	if total_len != data_length:
		print("\nData length did not match actual length of data; Terminating Server....\n")
		serverSocket.close()
	elif entity != 1:
		print("Entity does not match expected entity:  Received: ", entity, "Expected: 1 Terminating Server....\n")
		serverSocket.close()
	elif p_code != codeA:
		print("P-Code does not match expected P-Code:  Received: ", p_code, "Expected: ", codeA, " Terminating Server....\n")
		serverSocket.close()


	#print recieved packets
	print("PACKET RECIEVED FROM CLIENT")
	print("Header: ")
	print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
	print("Data: ")
	print("Packet ID =", packet_id[0])
	print("Data =", data)


	#server checks for b-1
	while True:
		if ((data_length % 4) == 0) and (counter == packet_id[0]):
			
			#75 percent chance of sending an ack package
			if ((random.random() <= 0.90)):
				#data
				acked_packet_id = counter

				#pack data
				packet_data_b1 = struct.pack("!I", acked_packet_id)

				#Creates header 
				data_length = len(packet_data_b1)
				pcode = codeA
				entity = 2

				#packs data into packet 
				packet_header_b1 = struct.pack("!IHH", data_length, pcode, entity)
				
				#sends a packet back to the client
				Full_Packet_B_1 = packet_header_b1 + packet_data_b1
				serverSocket.sendto(Full_Packet_B_1, clientAddress)

				#print sent ack package
				print("ACK PACKET SENT")
				# print("Header: ")
				# print("Data length =",data_length, "Pcode =",pcode, "Entity =",entity)
				# print("Data: ")
				# print("Packet ID =", packet_id[0])
				print("ACK Packet ID: ", acked_packet_id)
				print("Packet ID: ", packet_id[0])
				print("\n")

				
				#count the ack packets
				counter = counter + 1
				break
			else:
				print("ACK Packet Not Sent")
				print("\n")

#print statement
print("END OF PHASE B-1")
print("\n")


#PHASE B-2
#PACKET SENT

#data
tcp_port = random.randint(20000, 30000)
codeB = random.randint(100, 400)

#pack data
packet_data_B = struct.pack("!II", tcp_port, codeB)

#header
data_length_B = len(packet_data_B)
pcode = codeA
entity = 2

#pack header
packet_header_B = struct.pack("!IHH", data_length_B, pcode, entity)

#send to client
full_Packet_B_2 = packet_header_B + packet_data_B
serverSocket.sendto(full_Packet_B_2, clientAddress)

#print statements
print("PHASE B-2")
print("PACKET SENT TO CLIENT")
print("Header: ")
print("Data length =",data_length_B, "Pcode =",pcode, "Entity =",entity)
print("Data: ")
print("TCP Port: ", tcp_port, "\nCode B: ", codeB)
print("///////////////////END PHASE B/////////////////////")
print("\n")


#########################################################
########### PHASE C and D TCP PART ######################
#########################################################

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = tcp_port

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time but 5 in queue
serverSocket.listen(5)
print ('The TCP server is connected')

# Server should be up and running and listening to the incoming connections

# Set up a new connection from the client
connectionSocket, addr = serverSocket.accept()


#Phase C server data
repeat2 = random.randint(5,20)
len2 = random.randint(50,100)
codeC = random.randint(100,400)
char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

data = struct.pack("!IHHc", repeat2, len2, codeC, char.encode())

##header details in PHASE C
data_length = len(data)
pcode = 0 # has to be set to codeC (FROM PHASE B)
entity = 2

packet = struct.pack("!IHH", data_length, pcode, entity) + data




#capitalizedSentence = afterHeader.upper()
connectionSocket.send(packet)

for x in range(repeat2):
    #Receive packet from cleint within 3 seconds or else close the connection
    try:
        serverSocket.settimeout(3)
        dataRecieved = connectionSocket.recv(1024)
    except:
        print("\nClient did not respond fast enough. Terminating Server.....\n")
        serverSocket.close()

    if len(dataRecieved) % 4 != 0:
        print("\nPacket was not divisible by 4; Terminating Server....\n")
        serverSocket.close()

    #Extract info based on bytes
    header = dataRecieved[:8]
    tcp_data = dataRecieved[8:]

    #Unpack response from server
    headerUnpack = struct.unpack("!IHH", header)

    #Assign server response to values
    data_length, pcode, entity = headerUnpack
    data = tcp_data
    char = data.decode()
	
        #Server Checks for data length, entity and pcode
    total_len = len(char)
    total_len = total_len 
    print("Total Len: ", total_len)
    print("expected len: ", data_length)
    if total_len != data_length:
        print("\nData length did not match actual length of data; Terminating Server....\n")
        serverSocket.close()
    elif entity != 1:
        print("Entity does not match expected entity:  Received: ", entity, "Expected: 1 Terminating Server....\n")
        serverSocket.close()
    elif pcode != codeC:
        print("P-Code does not match expected P-Code:  Received: ", pcode, "Expected: ", codeC, " Terminating Server....\n")
        serverSocket.close()


data_len = struct.calcsize("!I")
pcode = codeC
entity = 2
codeD = random.randint(100, 400)

print("Code D: ", codeD)



full_Packet_D = struct.pack("!IHH", data_len, pcode, entity) + struct.pack("!I", codeD)

connectionSocket.send(full_Packet_D)

print("\nProcess Completed. Terminating Server.....\n")

connectionSocket.close()


serverSocket.close()  
sys.exit()#Terminate the program after sending the corresponding data
