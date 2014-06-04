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


def moveMouse(x, y):
    bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
    objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])
    CGWarpMouseCursorPosition((x, y))


class SurgeonListener(Leap.Listener):
    def __init__(self):
        super(SurgeonListener, self).__init__()

    def on_frame(self, controller):
        frame = controller.frame()
        if not frame.hands.is_empty:
            hand = frame.hands[0]
            position = hand.palm_position
            cur_x, cur_y = m.position()
            if position.y < 200:
                m.click(x_dim/2, y_dim/2, 1)

            if position.x < 0:
                print(cur_x)
                #moveMouse(0, int(cur_y))
                #m.move(cur_x-1, cur_y)
                autopy.mouse.smooth_move(0, 0)

            if position.x > 0:
                autopy.mouse.smooth_move(int(x_dim2)-1, int(y_dim2)-1)
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
