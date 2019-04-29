import sys
import pylink
from pylinkwrapper import psychocal, connector
from psychopy import sound, visual,event, tools
from psychopy.tools import monitorunittools
import utils
deg2pix = monitorunittools.deg2pix

#define colors
red = (1.0, 0.0, 0.0)
green = (0.0, 1.0, 0.0)
white = (1.0, 1.0, 1.0)
black = (-1.0, -1.0, -1.0)
blue = (-1.0, -1.0, 1.0)
yellow = (1.0, 1.0, -1.0)

colors = {"red": red,
          "green": green,
          "white": white,
          "black": black,
          "blue": blue,
          "yellow": yellow}

class Calibration(psychocal.psychocal):
    def __init__(self, w,h, tracker, window,reward, target_color=1,target_size=20,
                 target_image=None,use_gabor=False,movie_stim=None):
        psychocal.psychocal.__init__(self, w, h, tracker, window)
        self.reward = reward
        self.duration = reward.duration
        self.phase = 0.0
        self.animate = False
        self.use_gabor = use_gabor
        self.correct_fixation = False
        self.use_movie = False
        self.tcolor = target_color
        if movie_stim is not None:
            self.targetout = visual.MovieStim(self.window, movie_stim, flipVert=False,
                                              size=target_size, pos=(0,0))
            self.use_movie = True
        elif target_image is None:
            if not use_gabor:
                self.targetout = visual.Circle(self.window, pos=(0, 0), radius=target_size,
                                       fillColor=self.tcolor,
                                       lineColor=self.tcolor, units='pix',
                                       fillColorSpace='rgb',
                                       lineColorSpace='rgb')
            else:
                self.targetout = visual.GratingStim(self.window, mask='gauss', units="pix", sf=5/target_size,
                                                ori=60.0, size=target_size,
                                                color=target_color, colorSpace='rgb')
        else:
            self.targetout = visual.ImageStim(self.window, target_image,
                                             size=target_size, units="pix")

        #override sound settings to use reward duration
        self.__target_beep__ = sound.Sound(800, secs=self.duration)
        self.__target_beep__done__ = sound.Sound(1200, secs=self.duration)
        self.__target_beep__error__ = sound.Sound(400, secs=self.duration)

    def play_beep(self,beepid):
        if beepid == pylink.DC_TARG_BEEP or beepid == pylink.CAL_TARG_BEEP:
            #self.reward.deliver()
            self.__target_beep__.play()
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
        if self.use_gabor or self.use_movie:
            self.animate = True
        else:
            # Display
            self.targetout.draw()
            self.window.flip()

    def erase_cal_target(self):
        if self.correct_fixation:
            self.reward.deliver()
            self.correct_fixation = False

        if self.use_gabor or self.use_movie:
            self.animate = False
        self.window.flip()

    def get_mouse_state(self):
        if self.mouse is None:
            self.mouse = event.Mouse()

        # Get mouse state
        mpos = self.mouse.getPos()
        mpre = self.mouse.getPressed()

        # Convert mpos to EyeLink coordinates
        mpos = [int(deg2pix(x, self.window.monitor)) for x in mpos]
        mpos = (int(mpos[0] + (self.sres[0] / 2)),
               int(mpos[1] + (self.sres[1] / 2)))

        # Return
        return (mpos, mpre[0])

    def get_input_key(self):
        ky = []
        v = event.getKeys()

        for key in v:
            pylink_key = None
            if len(key) == 1:
                pylink_key = ord(key)
            elif key == "escape":
                pylink_key = pylink.ESC_KEY
            elif key == "return":
                #self.reward.deliver()
                self.correct_fixation = True
                pylink_key = pylink.ENTER_KEY
            elif key == "pageup":
                pylink_key = pylink.PAGE_UP
            elif key == "pagedown":
                pylink_key = pylink.PAGE_DOWN
            elif key == "up":
                pylink_key = pylink.CURS_UP
            elif key == "down":
                pylink_key = pylink.CURS_DOWN
            elif key == "left":
                pylink_key = pylink.CURS_LEFT
            elif key == "right":
                pylink_key = pylink.CURS_RIGHT
            else:
                print('Error! :{} is not a used key.'.format(key))
                return

            ky.append(pylink.KeyInput(pylink_key, 0))
        #update the phase here as this function is polled regularly
        if self.animate:
            if self.use_gabor:
                self.targetout.phase += 0.05 #update the grating phase
            self.targetout.draw()
            self.window.flip()
        return ky



def calibrate(tracker, reward, cnum=13, paval=1000,target_color=1,
              target_size=1.0,target_image=None,use_gabor=False,pulse_dot=False,
              manual_calibration=False,movie_stim=None):
    """
    Calibrates eye-tracker using psychopy stimuli.
    :param tracker: Tracker object to communicate with eyelink

    :param reward: Reward object to disperse liquid reward through a serial port

    :param cnum: Number of points to use for calibration. Options are 3, 5,
                 9, 13.
    :type cnum: int
    :param paval: Pacing of calibration, i.e. how long you have to fixate
                  each target in milliseconds.
    :type paval: int

    :param target_color: Color of calibration target
    :type target_color: int or (float, float, float)

    :param target_size: Radius of calibration target in pixels
    :type target_size: float
    """

    # Generate custom calibration stimuli
    genv = Calibration(tracker.sres[0], tracker.sres[1],
                               tracker.tracker, tracker.win, reward,
                       target_color, target_size,target_image,use_gabor,
                       movie_stim)

    if tracker.realconnect:
        # Set calibration type
        calst = 'HV{}'.format(cnum)
        tracker.tracker.setCalibrationType(calst)

        # Set calibration pacing
        if manual_calibration:
            print "Using manual calibration"
            tracker.send_command("remote_cal_enable = 1")
            tracker.send_command("key_function 1 'remote_cal_target 1'")
            tracker.send_command("key_function 2 'remote_cal_target 2'")
            tracker.send_command("key_function 3 'remote_cal_target 3'")
            tracker.send_command("key_function 4 'remote_cal_target 4'")
            tracker.send_command("key_function 5 'remote_cal_target 5'")
            tracker.send_command("key_function 6 'remote_cal_target 6'")
            tracker.send_command("key_function 7 'remote_cal_target 7'")
            tracker.send_command("key_function 8 'remote_cal_target 8'")
            tracker.send_command("key_function 9 'remote_cal_target 9'")
            tracker.send_command("key_function y 'remote_cal_complete'")
        else:
            print "Using autmoatic calibration"
            tracker.send_command("remote_cal_enable = 0")
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


def start_calibration(exp_info):
    """
    Parse calibration from exp_info and start the calibration
    """
    screen_width = exp_info.get("screen_width", 1680)
    screen_height = exp_info.get("screen_height", 1050)
    #setup window
    if sys.platform == 'darwin':
        fullscreen = False
    else:
        fullscreen = True

    win = visual.Window(
        size=(screen_width, screen_height), fullscr=fullscreen, screen=1,
        allowGUI=True, allowStencil=False,
        monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
        blendMode='avg', useFBO=False)
    calibration_stim = exp_info.get("calibration_stimulus")
    manual_calibration = exp_info.get("manual_calibration", False)
    pulse_dot = exp_info.get("Pulse", False) # whether to pulse the dot
    if calibration_stim == "Gabor patch":
        use_calibration_gabor = True
        calibration_image_path = None
    else:
        use_calibration_gabor = False
        if not (calibration_stim == "Circle"):
            calibration_image_path = calibration_stim
        else:
            calibration_image_path = None
    calibration_target_size = exp_info.get("calibration_target_size", 1.0)/2
    if (calibration_image_path is not None) or (use_calibration_gabor):
        """
        for circle, the size is given as a radius. For image or gabor patch, we need
        to multiple by two to get the diameter
        """
        calibration_target_size *= 2
    # convert from degress to pixels
    calibration_target_size = deg2pix(calibration_target_size,win.monitor)
    calibration_target_color = colors[exp_info.get("calibration_target_color", "white")]
    ctype = exp_info.get("calibration_type", "9 points")
    cnum = int(ctype.split()[0])
    # change reward duration during calibration
    calibration_reward_duration = exp_info.get("calibration_reward_duration", 0.5)
    reward_cnx.duration = calibration_reward_duration
    calibration_movie_path = None
    if calibration_image_path is not None:
        bn, ext = os.path.splitext(calibration_image_path)
        if ext in [".mp4"]:
            calibration_movie_path = calibration_image_path
            calibration_image_path = None
    calibrate(tracker, reward_cnx, cnum=cnum,
                          target_color=calibration_target_color,
                          target_size=calibration_target_size,
                          target_image=calibration_image_path,
                          use_gabor=use_calibration_gabor,
                          pulse_dot=pulse_dot,
                          manual_calibration=manual_calibration,
                          movie_stim=calibration_movie_path)
