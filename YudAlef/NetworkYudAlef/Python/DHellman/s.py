__author__ = 'Yossi'
import wx
import random
import socket
import threading

PORT = 5555
IP = '0.0.0.0'
done = False
threads = []
connections = []

APP_SIZE_X = 300
APP_SIZE_Y = 500

class ServerApp(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_X, APP_SIZE_Y))
        wx.Button(self, 1, 'Close', (50, 130))
        wx.Button(self, 2, 'TcpHost', (150, 100), (110, -1))
        wx.Button(self, 3, 'TcpSend', (150, 130), (110, -1))

        self.editname = wx.TextCtrl(self, value="", pos=(40, 0), size=(140,-1))
        self.data_to_server = wx.TextCtrl(self, value="", pos=(53, 30), size=(140,-1))
        self.log = wx.TextCtrl(self, wx.ID_ANY,pos=(0,170), size=(284,APP_SIZE_Y-209),style=wx.TE_READONLY | wx.TE_MULTILINE)

        # diffy vars

        self.private_num_field = wx.TextCtrl(self, value="", pos=(75, 60), size=(140,-1))
        self.private_key = None
        self.P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DCC4024FFFFFFFFFFFFFFFF
        self.G = 6666

        self.NameLabel = wx.StaticText(self, 4, 'Name:',pos=(0,3))
        self.NameLabel = wx.StaticText(self, 4, 'Message:',pos=(0,33))
        self.KeyLabel = wx.StaticText(self, 4, 'Hellman Key:',pos=(0,66))

        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnTcpHost, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnTcpSend, id=3)


        self.Centre()
        self.ShowModal()
        # self.Destroy()

    def OnClose(self, event):
        global server_sock
        global done
        global threads

        for thread in threads:
            thread.join()

        done = True
        server_sock.close()
        self.Close(True)

    def OnTcpHost(self, event):
        global server_sock
        global threads
        server_sock.bind((IP, PORT))
        server_sock.listen()
        self.log.AppendText("Listening on port "+str(PORT)+'\n')
        t = threading.Thread(target=self.ListenForConnections)
        t.start()
        threads.append(t)

    def OnTcpSend(self, event):
        for connection in connections:
            connection.send(self.EncodeMsg(self.editname.Value + ": " + self.data_to_server.Value))
        self.log.AppendText(self.editname.Value + ": " + self.data_to_server.Value + "\n")

    def ListenForConnections(self):
        global server_sock
        global done
        global threads
        self.log.AppendText("Listening for connections\n")

        while not done:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=self.ClientConnection,args=[conn,addr])
            t.start()
            threads.append(t)


    def ClientConnection(self,conn,addr):
        global connections
        connections.append(conn)
        self.log.AppendText(f"New connection: {addr}\n")

        self.SendPublicKeys(conn)
        self.private_key = self.GetSharedKeys(int.from_bytes(conn.recv(1024), "big"))
        conn.send(int_to_bytes(self.GetSharedKeys(self.G)))

        self.KeyLabel.Destroy()
        self.private_num_field.Destroy()

        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                data = self.DecodeMsg(data)
                self.log.AppendText(data + "\n")

        connections.remove(conn)
        conn.close()

    def SendPublicKeys(self,conn):
        conn.send(int_to_bytes(self.P))
        conn.send(int_to_bytes(self.G))

    def GetSharedKeys(self,base):
        return int(pow(base,int(self.private_num_field.Value),self.P))

    def DecodeMsg(self,msg):
        return "".join([chr(ord(letter)-self.private_key%100) for letter in msg.decode()])

    def EncodeMsg(self,msg):
        return "".join([chr(ord(letter) + self.private_key%100) for letter in msg]).encode()


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')



server_sock = socket.socket()

app = wx.App(0)
ServerApp(None, -1, 'ICQ SERVER')
app.MainLoop()