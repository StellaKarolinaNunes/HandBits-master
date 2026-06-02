# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
import random
import math
from config.colors import *
from config.settings import *
from utils.locales import t

def draw_rounded_rect(img, pt1, pt2, color, thickness, radius):
    """Draws a rectangle with rounded corners."""
    x1, y1 = pt1; x2, y2 = pt2
    
    if thickness == -1: # Filled
        for p in [(x1+radius,y1+radius),(x2-radius,y1+radius),(x1+radius,y2-radius),(x2-radius,y2-radius)]:
            cv2.circle(img, p, radius, color, -1)
        cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, -1)
    else: # Outlined
        cv2.ellipse(img, (x1+radius, y1+radius), (radius, radius), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2-radius, y1+radius), (radius, radius), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x2-radius, y2-radius), (radius, radius), 0, 0, 90, color, thickness)
        cv2.ellipse(img, (x1+radius, y2-radius), (radius, radius), 90, 0, 90, color, thickness)
        
        cv2.line(img, (x1+radius, y1), (x2-radius, y1), color, thickness)
        cv2.line(img, (x1+radius, y2), (x2-radius, y2), color, thickness)
        cv2.line(img, (x1, y1+radius), (x1, y2-radius), color, thickness)
        cv2.line(img, (x2, y1+radius), (x2, y2-radius), color, thickness)

class ParticleSystem:
    def __init__(self):
        self.particulas = [] # [x, y, dx, dy, cor, ttl]

    def spawn(self, x, y, cor):
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 12)
            self.particulas.append([x, y, math.cos(angle)*speed, math.sin(angle)*speed, cor, random.randint(40, 80)])

    def update(self, frame):
        for p in self.particulas[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.2  # Gravity
            p[5] -= 1
            alpha = min(1.0, p[5] / 40.0)
            c = tuple(int(v * alpha) for v in p[4])
            cv2.circle(frame, (int(p[0]), int(p[1])), random.randint(2, 5), c, -1)
            if p[5] <= 0: 
                self.particulas.remove(p)


def pre_process_hand_guide(filename):
    """Pre-processes 'guia.png' for alpha blending."""
    img_guia = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    if img_guia is None:
        return None
        
    h_g, w_g = img_guia.shape[:2]
    new_h = 180 
    new_w = int(w_g * (new_h / h_g))
    img_guia = cv2.resize(img_guia, (new_w, new_h))
    
    if img_guia.shape[2] == 4:
        alpha = img_guia[:, :, 3] / 255.0
        bgr = img_guia[:, :, :3]
        bg = np.ones_like(bgr, dtype=np.uint8) * 255 # White background
        for c in range(3):
            bgr[:, :, c] = (bgr[:, :, c] * alpha + bg[:, :, c] * (1.0 - alpha)).astype(np.uint8)
        return bgr
    else:
        gray = cv2.cvtColor(img_guia, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY_INV)
        img_guia[mask > 0] = [255, 255, 255]
        return img_guia
