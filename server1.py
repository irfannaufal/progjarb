import sys 
import socket 
import select
import logging

HOST = 'localhost' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 10000

def chat_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
def login(self):
        global clients
        global messages
        global accounts
        global onlines

        logging.info('Connected from: %s:%s' %
                     (self.addr[0], self.addr[1]))
        clients.add((self.conn, self.addr))
        msg = '\n## selamat datang\n## masukkan `!q` to keluar\n'

        # new user
        print accounts
        if self.ip not in accounts:
            msg += '## Please enter your name:'
            self.print_indicator(msg)
            accounts[self.ip] = {
                'name': '',
                'pass': '',
                'lastlogin': time.ctime()
            }
            while 1:
                name = self.conn.recv(BUF_SIZE).strip()
                if name in messages:
                    self.print_indicator(
                        '## This name already exists, please try another')
                else:
                    break
            accounts[self.ip]['name'] = name
            self.name = name
            logging.info('%s logged as %s' % (self.addr[0], self.name))
            messages[name] = []
            self.print_indicator(
                '## Hello %s, please enter your password:' % (self.name,))
            password = self.conn.recv(BUF_SIZE)
            accounts[self.ip]['pass'] = password.strip()
            self.print_indicator('## Welcome, enjoy your chat')
        else:
            self.name = accounts[self.ip]['name']
            msg += '## Hello %s, please enter your password:' % (self.name,)
            # print accounts
            self.print_indicator(msg)
            while 1:
                password = self.conn.recv(BUF_SIZE).strip()
                if password != accounts[self.ip]['pass']:
                    self.print_indicator(
                        '## Incorrect password, please enter again')
                else:
                    self.print_indicator(
                        '## Welcome back, last login: %s' %
                        (accounts[self.ip]['lastlogin'],))
                    accounts[self.ip]['lastlogin'] = time.ctime()
                    break

 
    print "Chat server started on port " + str(PORT)
 
    while 1:

        # get the list sockets which are ready to be read through select
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "self.name connected"
                 
                broadcast(server_socket, sockfd, "self.name masuk ke chatting room\n")
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "your friend" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client self.name) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client self.name) is offline\n" % addr)
                    continue

    server_socket.close()

def list():

    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())


         

