import cv2
import numpy as np
from config.settings import *
from config.colors import *
from utils.locales import t, get_current_lang
from ui.drawing_utils import draw_rounded_rect

def draw_top_menu(frame, W, H, modo, aba_medalhas, voice_active):
    """Draws the top navigation menu."""
    top_h = 75
    frame[0:top_h, 0:W] = (20, 18, 12) # Deep dark blueish/black
    
    # White frame for the camera feed
    radius = 15
    cv2.line(frame, (radius, top_h), (W - radius, top_h), (255, 255, 255), 2)
    for y in range(top_h, top_h + radius):
        for x in range(0, radius):
            if (x - radius)**2 + (y - (top_h + radius))**2 > radius**2:
                frame[y, x] = (20, 18, 12)
        for x in range(W - radius, W):
            if (x - (W - radius))**2 + (y - (top_h + radius))**2 > radius**2:
                frame[y, x] = (20, 18, 12)
    cv2.ellipse(frame, (radius, top_h + radius), (radius, radius), 180, 0, 90, (255, 255, 255), 2)
    cv2.ellipse(frame, (W - radius, top_h + radius), (radius, radius), 270, 0, 90, (255, 255, 255), 2)

    labels = [t("menu_free"), t("menu_tutorial"), t("menu_challenge"), t("menu_medals"), t(f"lang_{get_current_lang()}"), "SOM ON", "SAIR"]
    total_menu_width = 6 * 104 + 95
    start_x = (W - total_menu_width) // 2
    for i, txt in enumerate(labels):
        is_active = (modo == "LIVRE" and i==0) or \
                    (modo == "TUTORIAL" and i==1) or \
                    (modo == "DESAFIO" and i==2) or \
                    (aba_medalhas and i==3)
        
        bx1, by1 = start_x + i * 104, 15
        bx2, by2 = bx1 + 95, 60
        
        if i == 4: # LANG
            display_txt = txt
            bg_color = (60, 40, 100) # Purple
            border_color = (90, 60, 150)
            text_color = COLOR_WHITE
        elif i == 5: # SOM
            display_txt = "SOM ON" if voice_active else "SOM OFF"
            bg_color = (22, 102, 40) if voice_active else (42, 32, 26)
            border_color = (42, 174, 76) if voice_active else (74, 63, 51)
            text_color = COLOR_WHITE
        elif i == 6: # SAIR
            display_txt = "SAIR"
            bg_color = (30, 28, 149)
            border_color = (56, 53, 209)
            text_color = COLOR_WHITE
        else:
            display_txt = txt
            if is_active:
                bg_color = (153, 110, 6) # Cyan BGR
                border_color = (226, 178, 12)
                text_color = COLOR_WHITE
            else:
                bg_color = (42, 32, 26)
                border_color = (74, 63, 51)
                text_color = COLOR_WHITE

        # Background and border
        draw_rounded_rect(frame, (bx1, by1), (bx2, by2), bg_color, -1, 8)
        draw_rounded_rect(frame, (bx1, by1), (bx2, by2), border_color, 1, 8)

        # Icons
        icon_x = bx1 + 10
        icon_y = by1 + 22
        
        if i == 0: # LIVRE
            cv2.rectangle(frame, (icon_x, icon_y-5), (icon_x+12, icon_y+3), (255,255,255), 1)
            cv2.line(frame, (icon_x-2, icon_y+6), (icon_x+14, icon_y+6), (255,255,255), 2)
        elif i == 1: # Tutorial
            pts = np.array([[icon_x+6, icon_y-6], [icon_x+14, icon_y-2], [icon_x+6, icon_y+2], [icon_x-2, icon_y-2]], np.int32)
            cv2.fillPoly(frame, [pts], (255,255,255))
            cv2.line(frame, (icon_x+1, icon_y+2), (icon_x+1, icon_y+6), (255,255,255), 1)
            cv2.line(frame, (icon_x+11, icon_y+2), (icon_x+11, icon_y+6), (255,255,255), 1)
            cv2.line(frame, (icon_x+1, icon_y+6), (icon_x+11, icon_y+6), (255,255,255), 1)
        elif i == 2: # DESAFIO
            cv2.rectangle(frame, (icon_x+2, icon_y-5), (icon_x+10, icon_y+2), (255,255,255), -1)
            cv2.line(frame, (icon_x-1, icon_y-4), (icon_x+2, icon_y-4), (255,255,255), 1)
            cv2.line(frame, (icon_x+10, icon_y-4), (icon_x+13, icon_y-4), (255,255,255), 1)
            cv2.line(frame, (icon_x+6, icon_y+2), (icon_x+6, icon_y+7), (255,255,255), 2)
            cv2.line(frame, (icon_x+2, icon_y+7), (icon_x+10, icon_y+7), (255,255,255), 2)
        elif i == 3: # MEDALHAS
            cv2.circle(frame, (icon_x+6, icon_y+1), 6, (255,255,255), 1)
            cv2.line(frame, (icon_x+6, icon_y-7), (icon_x+6, icon_y-5), (255,255,255), 2)
            cv2.line(frame, (icon_x+4, icon_y-7), (icon_x+8, icon_y-7), (255,255,255), 1)
            cv2.line(frame, (icon_x+6, icon_y+1), (icon_x+6, icon_y-2), (255,255,255), 1)
            cv2.line(frame, (icon_x+6, icon_y+1), (icon_x+8, icon_y+1), (255,255,255), 1)
        elif i == 4: # LANG
            cv2.circle(frame, (icon_x+6, icon_y+1), 6, (255,255,255), 1)
            cv2.line(frame, (icon_x, icon_y+1), (icon_x+12, icon_y+1), (255,255,255), 1)
            cv2.ellipse(frame, (icon_x+6, icon_y+1), (4,6), 0, 0, 360, (255,255,255), 1)
        elif i == 5: # SOM
            pts = np.array([[icon_x+5, icon_y-4], [icon_x+5, icon_y+6], [icon_x+1, icon_y+3], [icon_x-3, icon_y+3], [icon_x-3, icon_y-1], [icon_x+1, icon_y-1]], np.int32)
            cv2.fillPoly(frame, [pts], (255,255,255))
            cv2.ellipse(frame, (icon_x+5, icon_y+1), (4,4), 0, -60, 60, (255,255,255), 1)
            if voice_active:
                cv2.ellipse(frame, (icon_x+5, icon_y+1), (7,7), 0, -50, 50, (255,255,255), 1)
        elif i == 6: # SAIR
            cv2.rectangle(frame, (icon_x-2, icon_y-4), (icon_x+6, icon_y+6), (255,255,255), 1)
            cv2.line(frame, (icon_x+6, icon_y-2), (icon_x+6, icon_y+4), bg_color, 2)
            cv2.line(frame, (icon_x+2, icon_y+1), (icon_x+11, icon_y+1), (255,255,255), 1)
            cv2.line(frame, (icon_x+8, icon_y-2), (icon_x+11, icon_y+1), (255,255,255), 1)
            cv2.line(frame, (icon_x+8, icon_y+4), (icon_x+11, icon_y+1), (255,255,255), 1)

        font_scale = 0.4
        thickness = 1
        text_size = cv2.getTextSize(display_txt, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]
        tx = bx1 + 28 + (67 - text_size[0]) // 2
        ty = by1 + ((by2 - by1) + text_size[1]) // 2 - 2
        cv2.putText(frame, display_txt, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness, cv2.LINE_AA)
