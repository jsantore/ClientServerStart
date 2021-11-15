import threading
import arcade
import asyncio
import socket
import Server

class GameClient(arcade.Window):
    def __init__(self, server_add, client_add):
        super().__init__()
        self.server_address = server_add
        self.client_address = client_add


def setup_client_connection(client: GameClient):
    client_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(client_event_loop)
    client_event_loop.create_task(communication_with_server(client, client_event_loop))
    client_event_loop.run_forever()

async  def communication_with_server(client: GameClient, event_loop):
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while True:
        data_to_send = input("what shall we send to the server:")
        UDPClientSocket.sendto(str.encode(data_to_send), (client.server_address, Server.SERVER_PORT))
        data_packet = UDPClientSocket.recvfrom(1024)
        data = data_packet[0] #get the encoded string
        print(f"The client got {data} from server")

def main():
    client_address = Server.find_ip_address()
    server_address = input("what is the IP address of the server:")
    game = GameClient(server_address, client_address)
    client_thread = threading.Thread(target=setup_client_connection, args=(game,), daemon=True)
    client_thread.start()
    arcade.run()

if __name__ == '__main__':
    main()