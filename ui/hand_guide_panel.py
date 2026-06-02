import cv2
from config.settings import INDICADORES_POS
from config.colors import COLOR_CYAN, COLOR_GREEN
from ui.drawing_utils import draw_rounded_rect

def draw_hand_guide_widget(frame, W, H, mao_tutorial, numero_alvo):
    """Draws the tutorial hand guide."""
    if mao_tutorial is not None:
        h_m, w_m = mao_tutorial.shape[:2]
        mx, my = W - w_m - 20, H - h_m - 20
        
        # Light Glassmorphism background for the guide
        roi = frame[my-10:my+h_m+10, mx-10:mx+w_m+10]
        if roi.shape[0] > 0 and roi.shape[1] > 0:
            blurred = cv2.GaussianBlur(roi, (25, 25), 0)
            overlay = blurred.copy()
            cv2.rectangle(overlay, (0, 0), (w_m+20, h_m+20), (240, 240, 250), -1)
            frame[my-10:my+h_m+10, mx-10:mx+w_m+10] = cv2.addWeighted(blurred, 0.2, overlay, 0.8, 0)
        
        draw_rounded_rect(frame, (mx-10, my-10), (mx+w_m+10, my+h_m+10), COLOR_CYAN, 2, 15)
        
        guia_frame = mao_tutorial.copy()
        for i in range(10):
            if (numero_alvo >> i) & 1:
                rx, ry = INDICADORES_POS[i]
                cx, cy = int(rx * w_m), int(ry * h_m)
                # Cooler glowing target circles
                cv2.circle(guia_frame, (cx, cy), 6, COLOR_GREEN, -1)
                cv2.circle(guia_frame, (cx, cy), 10, (0, 255, 0), 2)
                cv2.circle(guia_frame, (cx, cy), 15, (0, 200, 0), 1)
        
        frame[my:my+h_m, mx:mx+w_m] = guia_frame
