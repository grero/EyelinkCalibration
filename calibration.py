import pylink
from pylinkwrapper import psychocal
from psychopy import sound, visual,event, tools
from psychopy.tools import monitorunittools
deg2pix = monitorunittools.deg2pix


class Calibration(psychocal.psychocal):
    def __init__(self, w,h, tracker, window,reward, target_color=1,target_size=20):
        psychocal.psychocal.__init__(self, w, h, tracker, window)
        self.reward = reward
        self.duration = reward.duration

        self.tcolor = target_color
        self.targetout = visual.Circle(self.window, pos=(0, 0), radius=target_size,
                                       fillColor=self.tcolor,
                                       lineColor=self.tcolor, units='pix',
                                       fillColorSpace='rgb',
                                       lineColorSpace='rgb')
        #override sound settings to use reward duration
        self.__target_beep__ = sound.Sound(800, secs=self.duration)
        self.__target_beep__done__ = sound.Sound(1200, secs=self.duration)
        self.__target_beep__error__ = sound.Sound(400, secs=self.duration)

    def play_beep(self,beepid):
        if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
            self.__target_beep__.play()
            self.reward.deliver()
        elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
            self.__target_beep__error__.play()
        else:  # CAL_GOOD_BEEP or DC_GOOD_BEEP
            self.__target_beep__done__.play()

    def setup_cal_display(self):
        self.window.flip()

    def draw_cal_target(self, x, y):
        # Convert to psychopy coordinates
        x = x - (self.sres[0] / 2)
        y = -(y - (self.sres[1] / 2))

        # Set calibration target position
        self.targetout.pos = (x, y)

        # Display
        self.targetout.draw()
        self.window.flip()

    def get_mouse_state(self):
        if self.mouse is None:
            self.mouse = event.Mouse()

        # Get mouse state
        mpos = self.mouse.getPos()
        mpre = self.mouse.getPressed()

        # Convert mpos to EyeLink coordinates
       # mpos = [int(deg2pix(x, self.window.monitor)) for x in mpos]
       # mpos = (int(mpos[0] + (self.sres[0] / 2)),
       #         int(mpos[1] + (self.sres[1] / 2)))

        # Return
        return (mpos, mpre[0])


def calibrate(tracker, reward, cnum=13, paval=1000,target_color=1,
              target_size=1.0):
    """
    Calibrates eye-tracker using psychopy stimuli.

    :param cnum: Number of points to use for calibration. Options are 3, 5,
                 9, 13.
    :type cnum: int
    :param paval: Pacing of calibration, i.e. how long you have to fixate
                  each target in milliseconds.
    :type paval: int
    """

    # Generate custom calibration stimuli
    genv = Calibration(tracker.sres[0], tracker.sres[1],
                               tracker.tracker, tracker.win, reward,
                       target_color, target_size)

    if tracker.realconnect:
        # Set calibration type
        calst = 'HV{}'.format(cnum)
        tracker.tracker.setCalibrationType(calst)

        # Set calibraiton pacing
        tracker.tracker.setAutoCalibrationPacing(paval)

        # Execute custom calibration display
        print '*' * 150
        print 'Calibration Mode'
        print '*' * 150
        pylink.openGraphicsEx(genv)

        # Calibrate
        tracker.tracker.doTrackerSetup(tracker.sres[0], tracker.sres[1])
    else:
        genv.dummynote()


