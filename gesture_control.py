import math

class GestureController:
    def __init__(self, pinch_threshold=40):
        self.pinch_threshold = pinch_threshold

    def is_pinch(self, landmarks):
        if not landmarks:
            return False

        # Get index tip (id 8) and thumb tip (id 4)
        index_finger = next((x for x in landmarks if x[0] == 8), None)
        thumb = next((x for x in landmarks if x[0] == 4), None)

        if index_finger and thumb:
            _, x1, y1 = index_finger
            _, x2, y2 = thumb
            distance = math.hypot(x2 - x1, y2 - y1)
            return distance < self.pinch_threshold

        return False
    def is_fist(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return False

        # Fingertip IDs: index (8), middle (12), ring (16), pinky (20)
        # Lower joints: index (6), middle (10), ring (14), pinky (18)
        folded = 0
        finger_tip_ids = [8, 12, 16, 20]
        finger_base_ids = [6, 10, 14, 18]

        for tip_id, base_id in zip(finger_tip_ids, finger_base_ids):
            tip = next((lm for lm in landmarks if lm[0] == tip_id), None)
            base = next((lm for lm in landmarks if lm[0] == base_id), None)
            if tip and base and tip[2] > base[2]:  # y increases downward
                folded += 1

        return folded == 4
    
       



