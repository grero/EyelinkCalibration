import socket
import numpy as np
import time
import subprocess as sp

class PlotClient():
    def __init__(self, hostname="localhost", port=1234):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((hostname, port))
        except:
            self.sock = None

    def set_width(self,width):
        self.sock.sendall("width : %f\n" %(width,))

    def set_height(self,height):
        self.sock.sendall("height : %f\n" %(height,))

    def set_bottom(self,bottom):
        self.sock.sendall("bottom : %f\n" %(bottom, ))

    def set_left(self,left):
        self.sock.sendall("left : %f\n" %(left, ))

    def plot(self,x,y):
        self.sock.sendall("%f,%f\n" %(x,y))


def test(port=4578):
    #pp = sp.Popen("/Users/roger/Documents/programming/julia/SocketPlot/src/SocketPlot.jl")
    client = PlotClient(port=port)
    if client.sock is not None:
        client.set_width(20)
        client.set_height(20)
        client.set_left(-10)
        client.set_bottom((-10))
        x = 0.0
        y = 0.0
        for i in xrange(1000):
            x += np.random.randn()
            y += np.random.randn()
            client.plot(x,y)
            time.sleep(0.1)





