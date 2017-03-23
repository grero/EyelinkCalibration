import pylink
from pylinkwrapper import psychocal
from psychopy import sound

class Calibration(psychocal.psychocal):
    def __init__(self, w,h, tracker, window,reward):
        psychocal.psychocal.__init__(self, w, h, tracker, window)
        self.reward = reward
        self.duration = reward.duration

        #override sound settings to use reward duration
        self.__target_beep__ = sound.Sound(800, secs=self.duration)
        self.__target_beep__done__ = sound.Sound(1200, secs=self.duration)
        self.__target_beep__error__ = sound.Sound(400, secs=self.duration)

    def play_beep(self,beepid):
        if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
            self.reward.open()
            self.__target_beep__.play()
            self.reward.close()
        elif beepid == pylink.CAL_ERR_BEEP or beepid == pylink.DC_ERR_BEEP:
            self.__target_beep__error__.play()
        else:  # CAL_GOOD_BEEP or DC_GOOD_BEEP
            self.__target_beep__done__.play()

def calibrate(tracker, reward, cnum=13, paval=1000):
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
                               tracker.tracker, tracker.win, reward)

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


