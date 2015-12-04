import sys
import socket 
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4000
PORT = 10001
MAP = {}
def chat_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)
 
    #print "Chat server mulai pada port " + str(PORT)
 
    while 1:
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      		
        for sock in ready_to_read:
            if sock == server_socket: 
                socked, addr = server_socket.accept()
                SOCKET_LIST.append(socked)
                print "Client (%s, %s) terhubung" % addr
                #broadcast(server_socket, sockfd, "\r[%s:%s] memasuki chatting room kami\n" % addr)
            else:
                
                try:
		        data = sock.recv(RECV_BUFFER)
		        if data:
			   global MAP
			   a= data.split()
			   if a[2] =="sendto" :
				test =False
				for key,value in MAP.iteritems():
					if value == sock :
						test=True
				if test==True :
					sendto(a[3],a)
				else :
					sock.send("\rsilahkan login dulu\n")
				
			   elif a[2] =="2" :
				test =False
				for key,value in MAP.iteritems():
					if value == sock :
						test=True
				if test==True :
					daftar(sock,server_socket)
				else :
					sock.send("\rsilahkan login dulu\n")
				
			   elif a[2]=="sendall" :
				datautuh = "\r" + a[0] + " says "
				count = 0
				while count !=len(a):
					if count >2:
						datautuh += (a[count]+" ")
					count+=1
				datautuh += "\n"
				test =False
				for key,value in MAP.iteritems():
					if value == sock :
						test=True
				if test==True :
					broadcast(server_socket, sock, datautuh)
				else :
					sock.send("\rsilahkan login dulu\n")
			   elif (a[0]==a[2]):
				login(sock,a[0],server_socket)
			   elif a[2]=="1" :
				login(sock,a[3],server_socket)
			   else:
				sock.send("\rinvalid command\n")
		        else:          
		           if sock in SOCKET_LIST:
		                SOCKET_LIST.remove(sock)
			   simpan = MAP[sock]     
		           broadcast(server_socket, sock, "\rClient (%s) off\n" % simpan) 
 
                except:
                    broadcast(server_socket, sock, "\rclient off\n" )
                    continue

    server_socket.close()

def daftar(sock1,server_socket):
	data ="\rlist yang online\n"	
	for socket in SOCKET_LIST :
		for key,value in MAP.iteritems():
			if socket == value :
				data+=(key + " is online \n")
	try:	
		sock1.send(data)
	except:
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
	
def sendto(destination,message):
	data = "\r"+message[0] + " says "
	count = 0 
	while count!=len(message):
		if count>3 :
			data+=(message[count]+" ")
		count +=1	
	data += "\n"
	socket = MAP[destination]
	try :
		socket.send(data)
	except :
		socket.close()
		if socket in SOCKET_LIST :
			SOCKET_LIST.remove(socket)
def login(sock,name,server_socket):
	test =True
	for key,value in MAP.iteritems():
		if key == name :
			test=False
	if(test==False):
		sock.send("\rnama sudah dipake\n")
	else :
		MAP[name]=sock
		broadcast1(sock,server_socket,name)			
def broadcast (server_socket, sock, message):
    
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)	
def broadcast1 (sock,server_socket,name):
   	broadcast(server_socket,sock,"\r%s sedang online \n"%name)
 
if __name__ == "__main__":

    sys.exit(chat_server())
