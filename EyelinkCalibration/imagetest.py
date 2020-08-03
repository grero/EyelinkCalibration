from psychopy import visual, core, monitors, logging, event, tools, data, parallel
import sys
import time
import numpy as np

class MovingGratingStim(visual.GratingStim):
    def draw(self,win=None):
        self.phase += 0.01
        visual.GratingStim.draw(self, win)

win2 = visual.Window(
            size=(800, 600), fullscr=False, screen=0,
            allowGUI=True, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            blendMode='avg', useFBO=False, winType='pyglet')

aspect_ratio = 1200/1600.0
image = visual.ImageStim(win2, "banana_small_alpha.png",size=4.0,units="deg")
grating = MovingGratingStim(win2, mask='gauss', units="deg", sf=1.0, ori=60.0,size=2.0,
                             color=(1.0, 0.0, 0.0),colorSpace='rgb')
movie = visual.MovieStim(win2, "/Users/roger/Documents/research/monkey/data/movies/animals.mp4",
                         flipVert=False)

fixation_dot = visual.Circle(win2, 50.0, units="pix",fillColor=(1.0, 1.0, 1.0),
                             fillColorSpace='rgb')

def do_every(period,f,*args):
    def g_tick():
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count*period - time.time(),0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        f(*args)

def update_phase(grating):
    grating.phase = grating.phase + 0.01

#do_every(0.016, update_phase, grating)
clock = core.Clock()
clock.reset()
while True:
    keys = event.getKeys()
    if "escape" in keys:
        break
    movie.draw()
    #fixation_dot.contrast = np.sin(2*np.pi*clock.getTime()/5.0)
    #fixation_dot.draw()
    win2.flip()
win2.close()