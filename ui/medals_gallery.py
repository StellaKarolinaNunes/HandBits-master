import cv2
import numpy as np
from config.medals import CONQUISTAS
from config.colors import COLOR_CYAN, COLOR_WHITE
from utils.locales import t
from ui.drawing_utils import draw_rounded_rect

def desenhar_vitrine_medalhas(frame, W, H, conquistas_destravadas, page=0):
    """Draws the trophy gallery screen."""
    overlay = frame.copy()
    margin_x, margin_y = 60, 60
    
    # Dark Glassmorphism Window
    roi = frame[margin_y:H-margin_y, margin_x:W-margin_x]
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        blurred = cv2.GaussianBlur(roi, (31, 31), 0)
        overlay_blur = blurred.copy()
        cv2.rectangle(overlay_blur, (0, 0), (W-2*margin_x, H-2*margin_y), (15, 15, 18), -1)
        frame[margin_y:H-margin_y, margin_x:W-margin_x] = cv2.addWeighted(blurred, 0.4, overlay_blur, 0.6, 0)
    
    draw_rounded_rect(frame, (margin_x, margin_y), (W-margin_x, H-margin_y), COLOR_CYAN, 1, 15)
    
    # Header
    cv2.putText(frame, t("title_medals"), (margin_x + 30, margin_y + 40), cv2.FONT_HERSHEY_DUPLEX, 0.7, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.line(frame, (margin_x + 30, margin_y + 55), (W-margin_x - 30, margin_y + 55), (40, 40, 50), 1)
    
    cols = 4
    rows = 2
    per_page = cols * rows
    col_spacing = (W - 2 * margin_x) // cols
    
    start_idx = page * per_page
    end_idx = min(len(CONQUISTAS), start_idx + per_page)
    
    for i in range(start_idx, end_idx):
        cid, nome, alvo, cor, ttype = CONQUISTAS[i]
        obtido = cid in conquistas_destravadas
        
        idx_page = i - start_idx
        row, col = idx_page // cols, idx_page % cols
        x_c = margin_x + int((col + 0.5) * col_spacing)
        y_c = margin_y + 115 + row * 125
        
        # Shadow
        cv2.circle(frame, (x_c+2, y_c+4), 35, (10, 10, 15), -1)
        
        c = cor if obtido else (35, 35, 40)
        cv2.circle(frame, (x_c, y_c), 35, c, -1)
        cv2.circle(frame, (x_c, y_c), 35, (255, 255, 255) if obtido else (60, 60, 65), 1, cv2.LINE_AA)
        
        if obtido:
            # Inner ring glow
            cv2.circle(frame, (x_c, y_c), 25, (255, 255, 255), 1, cv2.LINE_AA)
        
        text_size = cv2.getTextSize(nome, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)[0]
        t_color = COLOR_WHITE if obtido else (150, 150, 150)
        cv2.putText(frame, nome, (x_c - text_size[0]//2, y_c + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.45, t_color, 1, cv2.LINE_AA)
        
        desc = f"{alvo}" + (" bits" if ttype=="VAL" else " seg")
        desc_size = cv2.getTextSize(desc, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        cv2.putText(frame, desc, (x_c - desc_size[0]//2, y_c + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (120, 120, 120), 1, cv2.LINE_AA)

    # Draw slider arrows
    if page > 0:
        cv2.fillPoly(frame, [np.array([[margin_x+20, H//2], [margin_x+35, H//2-10], [margin_x+35, H//2+10]])], COLOR_CYAN)
    if end_idx < len(CONQUISTAS):
        cv2.fillPoly(frame, [np.array([[W-margin_x-20, H//2], [W-margin_x-35, H//2-10], [W-margin_x-35, H//2+10]])], COLOR_CYAN)
        
    # Page indicator
    max_page = (len(CONQUISTAS) - 1) // per_page
    page_txt = f"{t('page')} {page+1}/{max_page+1}"
    pt_size = cv2.getTextSize(page_txt, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
    cv2.putText(frame, page_txt, (W//2 - pt_size[0]//2, H - margin_y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (100, 100, 100), 1, cv2.LINE_AA)
