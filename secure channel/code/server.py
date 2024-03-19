""" 
References: 
    - https://python.readthedocs.io/fr/latest/library/socket.html
    - https://docs.python.org/3/library/ssl.html
"""
import socket 
import common_function as cf
import ssl


##########################################################################
#                       Set parameters                                   #
##########################################################################

#HOST = "127.0.0.1"           # using only localhost
HOST = ''                     # Using all available interfaces
PORT = 7007                   # arbitrary port

##########################################################################
#                           Define TLS                                   #
##########################################################################

server_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_ssl.minimum_version = ssl.TLSVersion.TLSv1_2
server_ssl.maximum_version = ssl.TLSVersion.TLSv1_3

# Load AIS_CA cert as trusted
server_ssl.load_verify_locations('./certs/AIS_CA.pem')

# Load server's certificate
server_ssl.load_cert_chain(certfile='./certs/server.crt', keyfile='./certs/server.key')

# Verify client's certificate
server_ssl.verify_mode = ssl.CERT_REQUIRED


##########################################################################
#                       Define socket                                    #
##########################################################################

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    with server_ssl.wrap_socket(sock=sock,server_side=True,\
                                 server_hostname=HOST) as s:
        try: 
            conn, addr = s.accept()
            cf.log_execution(f"SSL Handshake successfully established with {addr}: {s.version()} {s.cipher()}")
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)

                    # Request to terminate connection
                    if data.decode('UTF-8').lower() == 'exit':
                        conn.sendall('server_done_finished'.encode('UTF-8'))
                        conn.close()
                        cf.log_execution("Client requested termination. Connection terminated!")
                        break

                    # Execute request from the client
                    processed = cf.execute_command(data.decode('UTF-8'))
                    conn.sendall(processed.encode('UTF-8')) 

            s.close()
        except Exception as e:
            cf.log_execution(f"Exception: {e}")