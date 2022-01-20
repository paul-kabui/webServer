import socket
import mysql.connector

class WebServer:
    def __init__(self, address, port):
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.running = True

    def _create_sock(self):
        # Create socket
        self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_sock.bind((self.address, self.port))
        self.tcp_sock.listen()
        print(f"[+]Server running....ip adress: {self.address}, port: {self.port}")

    def connect(self):
        self._create_sock()
        while self.running:   
            # Wait for client connections
            client_conn, client_ip = self.tcp_sock.accept()
            print(f"[+][+] New Request")

            # Get the client request
            request = client_conn.recv(1024).decode()
            header_list = request.split("\n")
            req_directory = header_list[0].split()[1]
            #accept only GET or POST method
            req_method = header_list[0].split()[0]
            print(header_list)

            if req_method == 'POST' or req_method == "GET":
                if req_directory == '/':
                    req_directory = 'index.html'
                else:
                    req_directory = req_directory.strip('/')
    
                with open(req_directory, 'r') as rensp_file:
                    file_content = rensp_file.read()
    
                response = 'HTTP/1.0 200 OK\n\n'+file_content
                client_conn.sendall(response.encode())
                if req_method == 'POST':
                    post_data = header_list[len(header_list)-1]
                    print(post_data.split('&')[0].strip('='))
                client_conn.close()
                
            else:
                response = 'HTTP/1.0 200 OK\n\n <h1>Bad Request</h1>'
                client_conn.sendall(response.encode())
                client_conn.close()

                

        self.tcp_sock.close()

server = WebServer('localhost', 8080)
server.connect()