import socket
import threading
from protocol import User, AddOrganRequest, BuyOrganRequest, SuccessResponse, ErrorResponse, Balance, BuyOrganResponse
import pickle
from SQL_ORM import OrganRequestManager


HOST = '0.0.0.0'
PORT = 2000


class HTTPServer(object):
    threads = []
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Server started")
        self.orm = OrganRequestManager()
        self.sock.bind((HOST, PORT))

    def listen(self) -> None:
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            print(f'Client connected {client}')
            t = threading.Thread(target=self.listen_to_client, args=(client, address))
            t.start()
            HTTPServer.threads.append(t)

    def listen_to_client(self, client: socket.socket, address: tuple) -> None:
        print(f"New connection from {address}")
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    raise Exception('Client disconnected')
                self.recv_handler(data, client)
        except Exception as e:
            print(e)
            client.close()
    
    def recv_handler(self, data, client):
        try:
            req = pickle.loads(data)

            if isinstance(req, AddOrganRequest):
                self.orm.add_new_organ(req.name, req.organ_type, req.organ_price, req.organ_expiration_date)
                print(f"{req.name} added {req.organ_type}")
                client.send(pickle.dumps(SuccessResponse()))
            elif isinstance(req, BuyOrganRequest):
                organ = self.orm.buy_organ(req.organ_id, req.name)
                print(f"{req.name} bought {req.organ_id}")
                client.send(pickle.dumps(BuyOrganResponse(organ[1], organ[2], organ[3], (organ[4], organ[5]))))
            elif isinstance(req, User):
                balance = self.orm.get_dealer_balance(req.name)
                print(f"{req.name} requested balance")
                client.send(pickle.dumps(Balance(balance)))
            else:
                raise Exception("Unknown request")
        except Exception as e:
            print(e)
            client.send(pickle.dumps(ErrorResponse()))

    def on_quit(self) -> None:
        self.sock.close()
        for t in HTTPServer.threads:
            t.join()
        print("Server stopped")


def main():
    HTTPServer().listen()


if __name__ == '__main__':
    main()