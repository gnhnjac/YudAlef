import sys

import wx

from communication import *

from configparser import ConfigParser
config = ConfigParser()
config.read('conf.ini')
MAX_PLAYERS = int(config.get('settings', "MAX_PLAYERS"))


APP_SIZE_X = 300
APP_SIZE_Y = 500

class ServerApp(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(APP_SIZE_X, APP_SIZE_Y))
        wx.Button(self, 1, 'Close', (0, 30))
        wx.Button(self, 2, 'Start Game', (0, 0), (110, -1))

        self.log = wx.TextCtrl(self, wx.ID_ANY,pos=(0,170), size=(284,APP_SIZE_Y-209),style=wx.TE_READONLY | wx.TE_MULTILINE | wx.ALIGN_LEFT)

        self.Bind(wx.EVT_BUTTON, self.close, id=1)
        self.Bind(wx.EVT_BUTTON, self.start, id=2)

        self.s = Server('0.0.0.0', 5555, MAX_PLAYERS)
        sys.stdout = self.log

        self.Centre()
        self.ShowModal()

    def start(self, event):
        self.s.broadcast_start()

    def close(self, event):
        self.s.close()
        self.Destroy()

app = wx.App(0)
ServerApp(None, -1, 'CYE Server')
app.MainLoop()