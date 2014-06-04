import objc
import sys

import autopy
import Leap

from pymouse import PyMouse
from pykeyboard import PyKeyboard


m = PyMouse()
k = PyKeyboard()
x_dim, y_dim = m.screen_size()
x_dim2, y_dim2 = autopy.screen.get_size()


def close_hand():
    k.press_key('a')
    k.press_key('w')
    k.press_key('e')
    k.press_key('r')
    k.press_key('space')


def open_hand():
    k.release_key('a')
    k.release_key('w')
    k.release_key('e')
    k.release_key('r')
    k.release_key('space')


from AppKit import NSWorkspace
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import CGEventPostToPSN
from Quartz.CoreGraphics import CGDisplayShowCursor
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import kCGEventTargetProcessSerialNumber
from Quartz.CoreGraphics import CGEventTapCreateForPSN
from Quartz.CoreGraphics import CGEventGetIntegerValueField

from ctypes import c_int
from ctypes import Structure


class ProcessSerialNumber(Structure):
    _fields_ = [("highLongOfPSN", c_int),
                ("lowLongOfPSN", c_int)]


def mouseEvent(type, posx, posy):
    surgeon_process = filter(lambda x: x, [x if x.get('NSApplicationName') == 'Surgeon Simulator 2013' else None for x in  NSWorkspace.sharedWorkspace().launchedApplications()])[0]
    #surgeon_process = filter(lambda x: x, [x if x.get('NSApplicationName') == 'Steam' else None for x in  NSWorkspace.sharedWorkspace().launchedApplications()])[0]
    high_psn = surgeon_process.get('NSApplicationProcessSerialNumberHigh')
    low_psn = surgeon_process.get('NSApplicationProcessSerialNumberLow')
    surgeon_psn = (high_psn, low_psn)

    #surgeon_psn = (low_psn, high_psn)
    #print(surgeon_process)
    #print(surgeon_psn)
    theEvent = CGEventCreateMouseEvent(None, type, (posx, posy), kCGMouseButtonLeft)
    #CGEventPost(kCGHIDEventTap, theEvent)
    CGEventPostToPSN(surgeon_psn, theEvent)


def mousemove(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx, posy)

def mouseclick(posx,posy):
    #mouseEvent(kCGEventMouseMoved, posx,posy); #uncomment this line if you want to force the mouse to MOVE to the click location first (i found it was not necesary).
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);


def moveMouse(x, y):
    bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
    objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])
    CGWarpMouseCursorPosition((x, y))

#filter(lambda x: x, [x if x.get('NSApplicationName') == 'Surgeon Simulator 2013' else None for x in  NSWorkspace.sharedWorkspace().launchedApplications()])


class SurgeonListener(Leap.Listener):
    def __init__(self):
        super(SurgeonListener, self).__init__()

    def on_frame(self, controller):
        CGDisplayShowCursor(1)
        frame = controller.frame()
        if not frame.hands.is_empty:
            hand = frame.hands[0]
            position = hand.palm_position
            cur_x, cur_y = m.position()
            if position.y < 200:
                pass
                #m.click(x_dim/2, y_dim/2, 1)
                mouseclick(x_dim/2, y_dim/2)

            if position.x < 0:
                print(cur_x)
                mousemove(cur_x-1, cur_y)
                #moveMouse(0, int(cur_y))
                #m.move(cur_x-1, cur_y)
                #autopy.mouse.smooth_move(0, 0)

            if position.x > 0:
                mousemove(cur_x+1, cur_y)
                #autopy.mouse.smooth_move(int(x_dim2)-1, int(y_dim2)-1)
                print(cur_x)
                #moveMouse(x_dim, int(cur_y))
                #m.move(cur_x+1, cur_y)

            fingers = hand.fingers
            if fingers.is_empty:
                close_hand()
            else:
                open_hand()


def main():
    listener = SurgeonListener()
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES);

    controller.add_listener(listener)

    sys.stdin.readline()
    controller.remove_listener(listener)


if __name__ == "__main__":
    main()
