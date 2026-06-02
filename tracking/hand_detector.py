import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self, max_hands=2, detection_con=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame):
        """Processes the frame and returns (total_value, MultiHandLandmarks)"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        total_val = 0
        
        if results.multi_hand_landmarks:
            for hl in results.multi_hand_landmarks:
                # Landmark 0.x < 0.5 usually means the hand is on the right side of the frame after flip
                lado_e = hl.landmark[0].x < 0.5 
                vals = [32,64,128,256,512] if lado_e else [1,2,4,8,16]
                
                tips = [8,12,16,20]
                mids = [6,10,14,18]
                up = [False]*5
                
                # Thumb logic
                up[0] = math.dist([hl.landmark[4].x, hl.landmark[4].y], [hl.landmark[17].x, hl.landmark[17].y]) > \
                        math.dist([hl.landmark[3].x, hl.landmark[3].y], [hl.landmark[17].x, hl.landmark[17].y]) * 1.15
                
                # Other fingers
                for i in range(4):
                    up[i+1] = math.dist([hl.landmark[tips[i]].x, hl.landmark[tips[i]].y], [hl.landmark[0].x, hl.landmark[0].y]) > \
                             math.dist([hl.landmark[mids[i]].x, hl.landmark[mids[i]].y], [hl.landmark[0].x, hl.landmark[0].y]) * 1.25
                
                for i in range(5):
                    if up[i]: 
                        total_val += vals[i]
                
                self.mp_draw.draw_landmarks(frame, hl, self.mp_hands.HAND_CONNECTIONS)
                
        return total_val, results
