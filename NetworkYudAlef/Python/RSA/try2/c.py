import pickle
import threading
import rsa
import hashlib
import wx
import random
import socket


PORT = 5555
IP = '127.0.0.1'

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

        # RSA vars
        self.public, self.private = rsa.newkeys(1024)
        self.other_public = None


        self.log = wx.TextCtrl(self, wx.ID_ANY,pos=(0,170), size=(284,APP_SIZE_Y-209),style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.NameLabel = wx.StaticText(self, 4, 'Name:',pos=(0,3))
        self.MsgLabel = wx.StaticText(self, 4, 'Message:',pos=(0,33))


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

        self.other_public = pickle.loads(client_sock.recv(1024))
        client_sock.send(pickle.dumps(self.public))

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



    def EncodeMsg(self, msg):
        return rsa.encrypt(msg.encode(), self.other_public)

    def DecodeMsg(self, msg):
        return rsa.decrypt(msg, self.private).decode()



client_sock = socket.socket()

app = wx.App(0)
ClientApp(None, -1, 'ICQ CLIENT')
app.MainLoop()