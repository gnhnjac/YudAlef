__author__ = 'Yossi'
import wx
import random
import socket
import threading

PORT = 5555
IP = '127.0.0.1'
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
        self.NameLabel = wx.StaticText(self, 4, 'Name:',pos=(0,3))
        self.NameLabel = wx.StaticText(self, 4, 'Message:',pos=(0,33))

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
            connection.send(self.editname.Value.encode() + ": ".encode() + self.data_to_server.Value.encode())
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
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                self.log.AppendText(data.decode() + "\n")

        connections.remove(conn)
        conn.close()





server_sock = socket.socket()

app = wx.App(0)
ServerApp(None, -1, 'ICQ SERVER')
app.MainLoop()