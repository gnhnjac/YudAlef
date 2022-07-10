import threading
import AES
import hashlib
import wx
import random
import socket


PORT = 5555
IP = '192.168.0.42'

threads = []

APP_SIZE_X = 300
APP_SIZE_Y = 500

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

class ClientApp(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_X, APP_SIZE_Y))
        wx.Button(self, 1, 'Close', (50, 130))
        wx.Button(self, 2, 'TcpConnect', (150, 100), (110, -1))
        wx.Button(self, 3, 'TcpSend', (150, 130), (110, -1))

        self.editname = wx.TextCtrl(self, value="", pos=(40, 0), size=(140,-1))
        self.data_to_server = wx.TextCtrl(self, value="", pos=(53, 30), size=(140,-1))

        # diffy vars

        self.private_num_field = wx.TextCtrl(self, value="", pos=(75, 60), size=(140,-1))
        self.private_key = None
        self.P = None
        self.G = None

        self.log = wx.TextCtrl(self, wx.ID_ANY,pos=(0,170), size=(284,APP_SIZE_Y-209),style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.NameLabel = wx.StaticText(self, 4, 'Name:',pos=(0,3))
        self.MsgLabel = wx.StaticText(self, 4, 'Message:',pos=(0,33))
        self.KeyLabel = wx.StaticText(self, 4, 'Hellman Key:',pos=(0,66))


        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnTcpConnect, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnTcpSend, id=3)


        self.Centre()
        self.ShowModal()
        # self.Destroy()

    def OnClose(self, event):
        global client_sock
        global threads

        for thread in threads:
            thread.join()
        client_sock.close()
        self.Close(True)

    def OnTcpConnect(self, event):
        global client_sock
        global threads
        client_sock.connect((IP, PORT))
        self.log.AppendText(f"Connected to {IP} on port {PORT}\n")
        t = threading.Thread(target=self.Communicate)
        t.start()
        threads.append(t)

    def Communicate(self):
        global client_sock

        self.SetPublicKeys()
        client_sock.send(int_to_bytes(self.GetSharedKeys(self.G)))
        private_key = self.GetSharedKeys(int.from_bytes(client_sock.recv(1024),"big"))

        self.Encryptor = AES.AESCipher(hashlib.sha256(int_to_bytes(private_key)).digest())

        self.private_num_field.Destroy()
        self.KeyLabel.Destroy()

        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            else:
                data = self.DecodeMsg(data)
                self.log.AppendText(data + "\n")

    def OnTcpSend(self, event):
        global client_sock
        client_sock.send(self.EncodeMsg(self.editname.Value + ": " + self.data_to_server.Value))
        self.log.AppendText(self.editname.Value + ": " + self.data_to_server.Value + '\n')

    def SetPublicKeys(self):
        global client_sock
        self.P = int.from_bytes(client_sock.recv(1024),"big")
        self.G = int.from_bytes(client_sock.recv(1024),"big")

    def GetSharedKeys(self,base):
        return int(pow(base,int(self.private_num_field.Value),self.P))

    def DecodeMsg(self,msg):
        return self.Encryptor.decrypt(msg).decode()

    def EncodeMsg(self,msg):
        return self.Encryptor.encrypt(msg)



client_sock = socket.socket()

app = wx.App(0)
ClientApp(None, -1, 'ICQ CLIENT')
app.MainLoop()