""" 
References: 
    - https://python.readthedocs.io/fr/latest/library/socket.html
    - https://docs.python.org/3/library/ssl.html
"""
import socket 
import sys
import ssl

##########################################################################
#           Check and extract arguments + define parameters              #
##########################################################################
if len(sys.argv) < 4:
    print("Please, specify following arguments when calling programe:" \
          "`message`, `ip address`, and `port` for server. Example call:"\
          "`client.py <message> <ip address> <port>`.")
    sys.exit(42)

MESSAGE, HOST, PORT = (sys.argv[1]).encode('UTF-8'), sys.argv[2], int(sys.argv[3])


##########################################################################
#                           Define TLS                                   #
##########################################################################

client_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client_ssl.options |= ssl.OP_ALL
client_ssl.minimum_version = ssl.TLSVersion.TLSv1_2
client_ssl.maximum_version = ssl.TLSVersion.TLSv1_3

# Load AIS_CA cert as trusted
client_ssl.load_verify_locations('./certs/AIS_CA.pem')

# Load client's certificate
client_ssl.load_cert_chain(certfile='./certs/client.crt', keyfile='./certs/client.key')

# Verify servers' certificate
client_ssl.verify_mode = ssl.CERT_REQUIRED


##########################################################################
#                           Define socket                                #
##########################################################################

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    with client_ssl.wrap_socket(sock=sock, server_side=False, \
                                server_hostname=HOST) as s:
        s.connect((HOST, PORT))
        s.sendall(MESSAGE)              # Send initial message

        # Main program prints data (communication)
        while True:
            data = s.recv(1024)
            if data.decode('UTF-8').lower() == 'server_done_finished':
                break
            print('<<', data.decode('UTF-8'), flush=True)        
            
            # Read data (line) from STDIN (if there is any)
            s.sendall(input('>>').encode('UTF-8'))   
        s.close() 