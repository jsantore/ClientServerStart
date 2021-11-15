
import socket

SERVER_PORT = 25001

def find_ip_address():
    """returns the LAN IP address of the current machine as a string
    A minor revision of this answer:
    https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib#28950776"""
    server_address = ""
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        connection.connect(('10.255.255.255', 1))
        server_address = connection.getsockname()[0]
    except IOError:
        server_address = '127.0.0.1'
    finally:
        connection.close()
    return server_address

def main():
    server_address = find_ip_address()
    print(f"Server Address is: {server_address} on port: {SERVER_PORT}")
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((server_address,SERVER_PORT))
    count = 0
    while True:
        data_packet = UDPServerSocket.recvfrom(1024)
        count +=1
        message = data_packet[0] #data is first in tuple
        client_addr = data_packet[1] #client IP is second
        print(f"Server recieved {message} from {client_addr}")
        UDPServerSocket.sendto(str.encode(f"Got your message number {count} waiting for more...."), client_addr)

if __name__ == '__main__':
    main()
