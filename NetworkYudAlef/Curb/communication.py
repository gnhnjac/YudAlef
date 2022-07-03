import pickle
import socket
import struct
import threading
import random
from uuid import uuid4
from tcp_by_size import *
from utils import Platform, HealthCoord, StaminaCoord, JumpCoord, JumpPadCoord, Ladder


class PlayerPayload:
    def __init__(self, p_id, name, player):
        self.player = player
        self.player.id = p_id
        self.player.name = name


class Client:
    def __init__(self, host, port, username, renderer=None):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        self.communication_thread = threading.Thread(target=self.communicate)
        self.communication_thread.start()

        # Game stuff
        self.username = username
        self.renderer = renderer

    def communicate(self):
        """
        Thread that handles the communication with the server
        :return:
        """
        while True:
            msg = recv_by_size(self.sock)
            if msg == b'':
                break
            self.apply_instruction(msg)
        self.close()

    def close(self):
        """
        Close the connection to the server
        :return:
        """
        self.communication_thread.join()
        self.sock.close()

    def apply_instruction(self, msg):
        """
        Parse the instruction received from the server and apply it
        :param msg:
        :return:
        """
        instruction = msg[:4].decode()
        msg = msg[5:]
        if instruction == "LOBB":
            self.handle_lobby(msg)
        elif instruction == "COOR":
            self.handle_coords(msg)
        elif instruction == "STRT":
            self.renderer.game_started = True
        elif instruction == "GOVR":
            self.renderer.game_over = True
        elif instruction == "BULL":
            self.renderer.add_bullet_from_obj(pickle.loads(msg))
        elif instruction == "WORL":
            msg = msg.split(b"#")
            id = msg[0].decode()
            wrld = msg[1].decode()
            self.renderer.get_player_by_id(id).world = wrld
        elif instruction == "DEAD":
            id = msg.decode()
            self.renderer.get_player_by_id(id).is_temp_dead = True
        elif instruction == "DASH":
            id = msg.decode()
            p = self.renderer.get_player_by_id(id)
            p.current_image = p.dash_image
            p.dash_timer = 0
        elif instruction == "LEVL":
            self.renderer.load_level(msg)
        else:
            print("Unknown instruction")

    def handle_lobby(self, msg):
        """
        Parses lobby update into renderer
        :param msg:
        :return:
        """
        lobby = []

        while len(msg) > 0:
            size = int.from_bytes(msg[:8], "big")
            msg = msg[9:]
            pl = pickle.loads(msg[:size])
            msg = msg[size:]
            lobby.append(pl)
        self.renderer.load_lobby(lobby)

    def handle_coords(self, msg):

        """
        Parses coordinates update into renderer
        :param msg:
        :return:
        """
        try:
            p_id = msg.split(b"|")[0].decode()
            msg = msg[len(p_id) + 1:]
            x = struct.unpack("!i", msg[:4])[0]
            y = struct.unpack("!i", msg[5:])[0]
            self.renderer.update_player_coords(p_id, x, y)
        except:
            print("Error parsing coordinates")
            print(msg)

    def send(self, msg):
        """
        Send a message to the server.
        Has to be pre-encoded.
        :param msg:
        :return:
        """
        send_with_size(self.sock, msg)

    def send_quit(self):
        """
        Send a quit instruction to the server
        :return:
        """
        self.send(b"QUIT")
        self.close()

    def send_pp(self, player):
        """
        Send a player payload to the server
        :param player:
        :return:
        """
        self.renderer.player_id = uuid4()
        player.pickelize()
        self.send(b"PLPL#" + pickle.dumps(PlayerPayload(self.renderer.player_id, self.username, player)))

    def send_player_coords(self, x, y):
        """
        Send a coordinate update to the server
        :param x:
        :param y:
        :return:
        """
        self.send(
            b"COOR#" + str(self.renderer.player_id).encode() + b"|" + struct.pack("!i", int(x)) + b"|" + struct.pack(
                "!i", int(y)))

    def send_bullet(self, bullet):
        """
        Send a bullet to the server
        :param bullet:
        :return:
        """
        self.send(b"BULL#" + pickle.dumps(bullet))

    def send_dead(self):
        self.send(b"DEAD#" + str(self.renderer.player_id).encode())

    def send_revived(self):
        self.send(b"REVD")

    def send_world(self, world):
        self.send(b"WORL#" + str(self.renderer.player_id).encode() +b"#" + world.encode())

    def send_dash(self):
        self.send(b"DASH#" + str(self.renderer.player_id).encode())

    def send_level(self, level):
        self.send(b"LEVL#" + level.encode())

class Server:
    def __init__(self, host, port, max_connections):

        # Initialize socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)

        # Thread variables
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()
        self.client_threads = []
        self.lock = threading.Lock()

        # Game variables
        self.max_conns = max_connections
        self.lobby = {}
        self.levels = []

    def accept_connections(self):
        """
        Accept connections from clients and spawn a thread for each one
        :return:
        """
        while True:
            client, address = self.socket.accept()

            if len(self.lobby) + 1 <= self.max_conns:
                print(f'Connection from {address} has been established!')
                communicate_thread = threading.Thread(target=self.communicate, args=(client, address))
                communicate_thread.start()
                self.client_threads.append(communicate_thread)
            else:
                client.close()

    def communicate(self, client, addr):
        """
        Threaded function to communicate with clients
        :param client:
        :param addr:
        :return:
        """

        while True:
            data = recv_by_size(client)
            if data == b'':
                break
            self.apply_instruction(data, client)
        client.close()

    def broadcast_to_lobby(self, data, sender_id=None):
        """
        Broadcast data to lobby, if sender is not none it sends it to everyone except the sender
        :param data:
        :param sender:
        :return:
        """
        for conn in self.lobby:
            with self.lock:
                payload = self.lobby[conn]
                if payload.player.id != sender_id:
                    send_with_size(conn, data)

    def close(self):
        """
        Closes the server.
        :return:
        """
        for thread in self.client_threads:
            thread.join()
        self.socket.close()

    def apply_instruction(self, data, conn):
        """
        Parses a player instruction and applies it accordingly
        :param data:
        :return:
        """

        instruction = data[:4].decode()
        if instruction == 'PLPL':
            data = data[5:]
            payload = pickle.loads(data)
            with self.lock:
                self.lobby[conn] = payload
            self.broadcast_lobby_update()
            print(f'{payload.player.name} has joined the lobby, {len(self.lobby)}/{self.max_conns}')
        elif instruction == "COOR":
            self.broadcast_to_lobby(data, self.lobby[conn].player.id)
        elif instruction == "DEAD":
            self.lobby[conn].player.is_dead = True
            gameover = True
            for connection in self.lobby:
                payload = self.lobby[connection]
                if not payload.player.is_dead:
                    gameover = False
                    break
            if gameover:
                self.broadcast_game_over()
            else:
                self.broadcast_to_lobby(data, self.lobby[conn].player.id)

        elif instruction == "REVD":
            self.lobby[conn].player.is_dead = False
        elif instruction == "BULL":
            self.broadcast_to_lobby(data, self.lobby[conn].player.id)
        elif instruction == "QUIT":
            print(f'{self.lobby[conn].player.name} has left the lobby, {len(self.lobby) - 1}/{self.max_conns}')
            self.lobby.pop(conn)
            self.broadcast_lobby_update()
        elif instruction == "WORL":
            self.broadcast_to_lobby(data, self.lobby[conn].player.id)
        elif instruction == "DASH":
            self.broadcast_to_lobby(data,self.lobby[conn].player.id)
        elif instruction == "LEVL":
            num = int(data[5:].decode())
            self.generate_level_and_send(num, conn)
        else:
            print("Unknown instruction")

    def broadcast_lobby_update(self):
        """
        sends the updated lobby to all clients
        :return:
        """
        data = b"LOBB#"
        for conn in self.lobby:
            payload = self.lobby[conn]
            pickled = pickle.dumps(payload)
            data += len(pickled).to_bytes(8, "big") + b"|" + pickled
        self.broadcast_to_lobby(data)

    def broadcast_start(self):
        self.broadcast_to_lobby(b"STRT")

    def broadcast_game_over(self):
        self.broadcast_to_lobby(b"GOVR")

    def generate_level_and_send(self, num, conn):
        """
        Generates a level and sends it to all clients
        :return:
        """
        if num > len(self.levels):
            level = []
            level_addables = []

            # overgrown level
            if random.random() < 0.5:

                level.append(Platform((0, 1878), 4000, 122))
                level.append(Platform((1537,1123), 323, 877))
                level.append(Platform((341, 1355), 690, 76))
                level.append(Platform((132, 845), 1091, 97))
                level.append(Platform((678, 497), 694, 74))
                level.append(Platform((2096, 438), 692, 76))
                level.append(Platform((2090, 829), 694, 74))
                level.append(Platform((2218,1526), 1090, 94))
                level.append(Platform((3486, 1141), 514, 93))
                for i in range(3):
                    plat = random.choice(level)
                    level_addables.append(StaminaCoord(plat.x + random.randint(0, plat.width), plat.y - 100))
                for i in range(3):
                    plat = random.choice(level)
                    level_addables.append(HealthCoord(plat.x + random.randint(0, plat.width), plat.y - 100))
                level.append(Ladder((554, 820), 99, 1045))
                level.append(Ladder((894,480), 85, 384))
                level.append(Ladder((2805, 1501), 103, 375))
                level.append(Ladder((2351, 816), 111, 716))
                level.append(Ladder((2570, 439), 129, 390))

            else: # mirage level
                level.append(Platform((0, 1778), 4000, 222))
                level.append(Platform((291, 1291), 881, 136))
                level.append(Platform((291, 831), 880, 137))
                level.append(Platform((1463, 825), 636, 946))
                level.append(Platform((2306, 1338), 1252, 130))
                level.append(Platform((2589, 809), 1411, 137))
                for i in range(3):
                    plat = random.choice(level)
                    level_addables.append(StaminaCoord(plat.x + random.randint(0, plat.width), plat.y - 100))
                for i in range(3):
                    plat = random.choice(level)
                    level_addables.append(HealthCoord(plat.x + random.randint(0, plat.width), plat.y - 100))

                level.append(JumpPadCoord(1212,1790 - 115/2))
                level.append(JumpPadCoord(2131,1790 - 115/2))
                level.append(JumpCoord(1279, 1319))
                level.append(JumpCoord(1279, 870))
                level.append(JumpCoord(141, 870))
                level.append(JumpCoord(141, 1319))
                level.append(JumpCoord(2161, 1364))
                level.append(JumpCoord(3639, 1364))
                level.append(JumpCoord(2301, 682))
            level.extend(level_addables)

            self.levels.append(level)

        data = b"LEVL#"
        for platform in self.levels[num-1]:
            pickled = pickle.dumps(platform)
            data += len(pickled).to_bytes(8, "big") + b"|" + pickled
        send_with_size(conn, data)