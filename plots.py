import socket
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pylab as pylab
import numpy as np
import time
pylab.ion()

class ExperimentPlot:
    def __init__(self,left, bottom, width,height):
        self.figure = pylab.figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlim(left, left + width)
        self.ax.set_ylim(bottom, bottom + height)
        self.ax.set_autoscale_on(False)
        self.figure.canvas.draw()
        self.background = self.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.eyepos, = self.ax.plot([-1],[-1],'.',markersize=20)
        self.figure.canvas.draw()
        #pylab.show(block=False)


    def update_eyepos(self,x,y):
        self.figure.canvas.restore_region(self.background)
        self.eyepos.set_xdata([x])
        self.eyepos.set_ydata([y])
        self.ax.draw_artist(self.eyepos)
        self.figure.canvas.blit(self.ax.bbox)


def test():
    eplot = ExperimentPlot(-10,-10,20,20)
    x =0.0
    y = 0.0
    for i in xrange(1000):
        x += 0.1*np.random.randn()
        y += 0.1*np.random.randn()
        eplot.update_eyepos(x,y)
        time.sleep(0.01)


if __name__ == "__main__":
    #create a socket
    #listen to the socket
    #plot the x,y position from the socket
    #pylab.ion()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 2364))
    sock.listen(10)
    while 1:
        conn,addr = sock.accept()
        explot = ExperimentPlot(800,600)
        pylab.ion()
        while True:
            data = conn.recv(1024)
            if data == "":
                break
            x,y = [float(x) for x in data.split(",")]
            print x,y
            explot.update_eyepos(x,y)
            pylab.draw()

        conn.close()

    sock.close()
