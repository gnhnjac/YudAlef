import pickle
import socket
import struct
import threading
import random
import hashlib
from AES import *
import AES
from uuid import uuid4
from tcp_by_size import *


class DH:

    @staticmethod
    def get_num_field():
        return random.randint(0, 65535)

    @staticmethod
    def send_public_keys(conn, G, P):
        conn.send(DH.int_to_bytes(P))
        conn.send(DH.int_to_bytes(G))

    @staticmethod
    def get_private_key(base, power, mod):
        return int(pow(base, power, mod))

    @staticmethod
    def int_to_bytes(x):
        return x.to_bytes((x.bit_length() + 7) // 8, 'big')


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

        # Initialize DH connection
        self.P = int.from_bytes(self.sock.recv(1024), "big")
        self.G = int.from_bytes(self.sock.recv(1024), "big")
        self.dh_power = DH.get_num_field()
        self.sock.send(DH.int_to_bytes(DH.get_private_key(self.G, self.dh_power, self.P)))
        self.private_key = DH.get_private_key(int.from_bytes(self.sock.recv(1024), "big"), self.dh_power, self.P)
        self.aes = AESCipher(hashlib.sha256(AES.int_to_bytes(self.private_key)).digest())

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

    def decode(self, msg):
        """
        Decode a message received from the server using aes
        :param msg:
        :return:
        """
        return self.aes.decrypt(msg).decode()

    def encode(self, msg):
        """
        Encode a message to be sent to the server using aes
        :param msg:
        :return:
        """
        return self.aes.encrypt(msg)

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
        self.send(b"COOR#" + str(self.renderer.player_id).encode() + b"|" + struct.pack("!i",int(x)) +  b"|" + struct.pack("!i", int(y)))

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

        # Diffie Hellman parameters
        self.private_key = None
        self.dh_power = DH.get_num_field()
        self.P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DCC4024FFFFFFFFFFFFFFFF
        self.G = 6666

        # Game variables
        self.max_conns = max_connections
        self.lobby = {}

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

        # send public key
        DH.send_public_keys(client, self.G, self.P)
        conn_private_key = DH.get_private_key(int.from_bytes(client.recv(1024), "big"), self.dh_power, self.P)
        client.send(DH.int_to_bytes(DH.get_private_key(self.G, self.dh_power, self.P)))

        # aes
        conn_aes = AESCipher(hashlib.sha256(AES.int_to_bytes(conn_private_key)).digest())

        while True:
            data = recv_by_size(client)
            if data == b'':
                break
            self.apply_instruction(data,client)
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

    def decode(self, aes, msg):
        """
        Decodes a message from the client using aes.
        :param aes:
        :param msg:
        :return:
        """
        return aes.decrypt(msg).decode()

    def encode(self, aes, msg):
        """
        Encodes a message using AES
        :param aes:
        :param msg:
        :return:
        """
        return aes.encrypt(msg)

    def apply_instruction(self, data, conn):
        """
        Parses a player instruction and applies it accordingly
        :param data:
        :return:
        """

        instruction = data[:4].decode()

        to_send = b''

        if instruction == 'PLPL':
            data = data[5:]
            payload = pickle.loads(data)
            with self.lock:
                self.lobby[conn] = payload
            self.broadcast_lobby_update()
            print(f'{payload.player.name} has joined the lobby, {len(self.lobby)}/{self.max_conns}')
        elif instruction == "COOR":
            self.broadcast_to_lobby(data, self.lobby[conn].player.id)
        elif instruction == "QUIT":
            print(f'{self.lobby[conn].player.name} has left the lobby, {len(self.lobby)-1}/{self.max_conns}')
            self.lobby.pop(conn)
            self.broadcast_lobby_update()

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
        for conn in self.lobby:
            send_with_size(conn, b"STRT")