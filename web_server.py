import socket
import mysql.connector
import ssl
import html_template

class WebServer:
    def __init__(self, address, port, certfile, keyfile):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.certfile =certfile
        self.keyfile = keyfile
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        

        self.running = True

    def _create_sock(self):
        # Create socket
        # self.context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)# load files here
        self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_sock.bind((self.address, self.port))
        self.tcp_sock.listen()
        print(f"[+]Server running....ip adress: {self.address}, port: {self.port}")

    def connect(self):
        self._create_sock()
        while self.running:   
            # Wait for client connections
            client_conn, client_ip = self.tcp_sock.accept()
            # connection_stream = context.wrap_socket(client_conn, server_side=True)

            print(f"[+][+] New Request")

            # Get the client request
            request = client_conn.recv(1024).decode()
            # request = connection_stream.recv(1024).decode()
            header_list = request.split("\n")
            req_directory = header_list[0].split()[1]
            #accept only GET or POST method
            req_method = header_list[0].split()[0]

            if req_method == 'POST' or req_method == "GET":
                try:
                    if req_directory == '/':
                        req_directory = 'index.html'
                    elif req_directory == '/form.html':
                        html_template.create_html()
                        req_directory = 'form.html'
                        if req_method == 'POST':
                            post_data = header_list[len(header_list)-1]
                            #here the comment.txt file is for storage
                            #for database implementation, store the data in a db
                            msg = post_data.replace("=", ": ").replace("&", "</br>").replace("+"," ")+"</br>\n"
                            with open("comment.txt", 'a') as comment_file:
                                comment_file.write(msg)
                                comment_file.close()
                    else:
                        req_directory = req_directory.strip('/')

                    with open(req_directory, 'r') as rensp_file:
                        file_content = rensp_file.read()
                        response = 'HTTP/1.0 200 OK\n\n'+file_content
                        client_conn.sendall(response.encode())
                    # connection_stream.sendall(response.encode())
                    client_conn.close()
                except:
                    response = 'HTTP/1.0 404 ok\n\n <h1>404 File Not Found</h1>'
                    client_conn.sendall(response.encode())
                    
                
            else:
                response = 'HTTP/1.0 404 BAD Request\n\n <h1>Bad Request</h1>'
                client_conn.sendall(response.encode())
                client_conn.close()

                

        self.tcp_sock.close()

server = WebServer('localhost', 8080,'gfdg', "gfdgdfg")
server.connect()
