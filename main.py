import cv2
import pyautogui

from hand_tracker import HandTracker
from gesture_control import GestureController
from mouse_controller import MouseController
from gesture_settings import GestureSettings


def main():
    # Initialize components
    tracker = HandTracker()
    gesture = GestureController()
    screen_w, screen_h = pyautogui.size()
    mouse = MouseController(screen_w, screen_h)
    settings = GestureSettings()
    settings.start_ui()

    # Wait until the user clicks "Start"
    if not settings.should_start:
        return



    # Start webcam
    cap = cv2.VideoCapture(0)
    

    click_state = False  # To prevent repeated clicks
    right_click_state = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)  # Mirror the frame
        h, w, _ = frame.shape

        landmarks = tracker.find_hand_landmarks(frame, draw=True)

        # Find index fingertip to move mouse
        index = next((x for x in landmarks if x[0] == 8), None)
        if settings.move_enabled.get() and index:
            _, x, y = index
            mouse.move_cursor(x, y, w, h)

        # Check for pinch gesture to click
        if settings.click_enabled.get() and gesture.is_pinch(landmarks):
            if not click_state:
                mouse.click()
                click_state = True
        else:
            click_state = False

        cv2.imshow("Virtual Mouse", frame)
               

        # Right Click: fist detection
        if settings.right_click_enabled.get() and gesture.is_fist(landmarks):
            if not right_click_state:
                mouse.right_click()
                right_click_state = True
        else:
            right_click_state = False
        



        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
