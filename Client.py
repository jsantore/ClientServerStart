import threading
import arcade
import asyncio
import socket
import Server
import pathlib

class GameClient(arcade.Window):
    def __init__(self, server_add, client_add):
        super().__init__(1000, 1000)
        self.ip_addr = client_add
        self.image_path = pathlib.Path.cwd() / 'Assets' / 'captain1.png'
        self.player = arcade.Sprite(self.image_path)
        self.target = arcade.Sprite(str(pathlib.Path.cwd() / 'Assets' / 'gold-coins.png'))
        self.server_address = server_add
        self.player_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.target_list.append(self.target)
        self.player_list.append(self.player)
        self.from_server = 0
        #        self.player_state_list = PlayerState.GameState(player_states=[])
        # self.actions = PlayerState.PlayerMovement()

    def setup(self):
        self.player = arcade.Sprite(self.image_path)
        self.player_list.append(self.player)
        self.from_server = ""

    def on_update(self, delta_time: float):
        pass

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.target_list.draw()
        arcade.draw_text(f"Your Score {self.from_server}", 100, 900, color=(240, 30, 30), font_size=24)


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