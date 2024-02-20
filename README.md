# CP372 Computer-Networks
Introduction to computer communication networks. The OSI reference model. Protocols for error and flow control, medium access protocols, routing and congestion control. Internet architecture and protocols and Unix network programming.

A1
In this assignment, you will develop a client and server application that communicate using a
specific protocol called HaveFunCoding (HFC). The protocol consists of four phases. The initial
two phases use UDP for communication, while the last two phases use TCP. Communication
occurs through the exchange of packets, each comprising a header and data. The general
format of a packet is shown in the following figure:
As you can see, a packet consists of a header and a data part. The header is located in the
initial part of the packet and is 8 bytes. Within the header, the first four bytes represent
data_length, indicating the length of the data part of the packet (Note: this length excludes the
header length, it only specifies the data part’s length).
The pcode is the code generated and sent by the server in the previous phase of the protocol.
In the initial phase, pcode is set to zero. The client must extract the code sent by the server in
each phase and use it in the subsequent phase. The server verifies that the client adheres to
the protocol and will terminate the connection in case of any deviation from the protocol.
The following two bytes indicate entity. This field specifies whether the sender is the client
(always represented as 1) or the server (always represented as 2).
The data part can vary in size; what’s important is that the packet’s overall size must be divisible
by 4. In other words, when constructing a packet, the data part must be padded to ensure the
packet length is evenly divisible by 4


A2
Your task is to develop a simple mail client that sends email to any recipient. Your client will
need to connect to a mail server, dialogue with the mail server using the SMTP protocol, and
send an email message through the mail server. Refer to the slides on Application layer where a
sample SMTP interaction is provided.
