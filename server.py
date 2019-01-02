import socket
import threading

bind_port = 9999
bind_ip = '0.0.0.0'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
print "Listening connection from %s: %d" % (bind_ip, bind_port)
server.listen(5)


def server_handle(socket_client):
    request = socket_client.recv(1024)
    print "Received %s" %request
    socket_client.send('ack')
    socket_client.close()

while True:
    conn, addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
    client_handler = threading.Thread(target=server_handle,args=(conn,))
    client_handler.start()
    
    