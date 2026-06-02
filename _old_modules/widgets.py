import cv2
import numpy as np
import time
from config.settings import *
from config.colors import *
from config.medals import *
from utils.locales import t, get_current_lang
from .visuals import draw_rounded_rect

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

def draw_hud(frame, W, H, modo, total_val, numero_alvo, acertos, erros, tempo_inicio, tempo_round, melhor_tempo):
    """Draws the Heads Up Display."""
    is_livre = (modo == "LIVRE")
    
    # Super compact dynamic sizes (Single Row)
    if is_livre:
        hud_w = 160
    elif modo == "TUTORIAL":
        hud_w = 460
    else:
        hud_w = 380
        
    hud_h = 70
    
    x1, y1 = 20, H - hud_h - 20
    x2, y2 = x1 + hud_w, H - 20
    
    # Dark Glassmorphism for HUD
    roi = frame[y1:y2, x1:x2]
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        blurred = cv2.GaussianBlur(roi, (25, 25), 0)
        overlay = blurred.copy()
        cv2.rectangle(overlay, (0, 0), (hud_w, hud_h), (15, 15, 20), -1)
        frame[y1:y2, x1:x2] = cv2.addWeighted(blurred, 0.5, overlay, 0.5, 0)
        
    draw_rounded_rect(frame, (x1, y1), (x2, y2), COLOR_CYAN, 1, 8)
    
    # Header (Modo)
    cv2.putText(frame, f"{t('mode')}: {modo}", (x1 + 12, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_CYAN, 1, cv2.LINE_AA)
    cv2.line(frame, (x1 + 8, y1 + 28), (x2 - 8, y1 + 28), (80, 80, 90), 1)
    
    if is_livre:
        # Compact LIVRE layout
        cv2.putText(frame, f"{t('value')}:", (x1 + 15, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)
        cv2.putText(frame, str(total_val), (x1 + 75, y1 + 54), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 100), 1, cv2.LINE_AA)
    else:
        # Single Row Layout for TUTORIAL / DESAFIO
        # 1. VALOR
        cv2.putText(frame, f"{t('value')}:", (x1 + 12, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
        cv2.putText(frame, str(total_val), (x1 + 65, y1 + 54), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 100), 1, cv2.LINE_AA)
        
        # 2. ALVO
        cv2.putText(frame, f"{t('target')}:", (x1 + 105, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1, cv2.LINE_AA)
        cv2.putText(frame, str(numero_alvo), (x1 + 150, y1 + 54), cv2.FONT_HERSHEY_DUPLEX, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)
        
        # 3. BOTÃO REINICIAR (em frente ao alvo)
        offset_x = x1 + 195
        if modo == "TUTORIAL":
            bx_r, by_r = offset_x, y1 + 35
            draw_rounded_rect(frame, (bx_r, by_r), (bx_r + 65, by_r + 25), (40, 40, 45), -1, 4)
            draw_rounded_rect(frame, (bx_r, by_r), (bx_r + 65, by_r + 25), COLOR_CYAN, 1, 4)
            cv2.putText(frame, t("btn_restart"), (bx_r + 4, by_r + 16), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_CYAN, 1, cv2.LINE_AA)
            offset_x += 80 # Espaço após o botão
        else:
            offset_x += 10 # Espaço menor se não tiver botão

        # 4. TEMPO
        t_curr = time.time() - (tempo_inicio if modo == "DESAFIO" else tempo_round)
        cv2.putText(frame, f"{t('time')}: {t_curr:.1f}s", (offset_x, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1, cv2.LINE_AA)
        
        # 5. PROG / ERROS
        offset_x += 85
        if modo == "DESAFIO":
            cv2.putText(frame, f"{t('hits')}: {acertos}/5", (offset_x, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_GREEN, 1, cv2.LINE_AA)
            cv2.putText(frame, f"{t('misses')}: {erros}", (offset_x + 55, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_RED, 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, f"{t('prog')}: {numero_alvo}/1023", (offset_x, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 200, 0), 1, cv2.LINE_AA)
    
    # Maior Recorde (fora do Hud para destaque)
    if melhor_tempo < 999.0:
        cv2.putText(frame, f"{t('record')}: {melhor_tempo:.2f}s", (W - 180, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_CYAN, 1, cv2.LINE_AA)

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

def draw_achievement_popup(frame, W, H, popup_timer, popup_nome):
    """Draws achievement unlock popup."""
    y_pop = H // 2 - (60 - popup_timer)
    txt1 = t("new_medal")
    ts1 = cv2.getTextSize(txt1, cv2.FONT_HERSHEY_DUPLEX, 0.8, 2)[0]
    cv2.putText(frame, txt1, (W // 2 - ts1[0] // 2, y_pop - 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, COLOR_WHITE, 2, cv2.LINE_AA)
    
    ts2 = cv2.getTextSize(popup_nome, cv2.FONT_HERSHEY_DUPLEX, 1.0, 2)[0]
    cv2.putText(frame, popup_nome, (W // 2 - ts2[0] // 2, y_pop), cv2.FONT_HERSHEY_DUPLEX, 1.0, COLOR_CYAN, 2, cv2.LINE_AA)

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

def draw_dashboard(frame, W, H, desafio_tempos):
    """Draws performance dashboard with graph."""
    margin_x, margin_y = 100, 100
    roi = frame[margin_y:H-margin_y, margin_x:W-margin_x]
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        blurred = cv2.GaussianBlur(roi, (25, 25), 0)
        overlay_blur = blurred.copy()
        cv2.rectangle(overlay_blur, (0, 0), (W-2*margin_x, H-2*margin_y), (15, 15, 18), -1)
        frame[margin_y:H-margin_y, margin_x:W-margin_x] = cv2.addWeighted(blurred, 0.5, overlay_blur, 0.5, 0)
    
    draw_rounded_rect(frame, (margin_x, margin_y), (W-margin_x, H-margin_y), COLOR_CYAN, 1, 15)
    
    cv2.putText(frame, t("performance"), (margin_x + 30, margin_y + 40), cv2.FONT_HERSHEY_DUPLEX, 0.7, COLOR_CYAN, 1, cv2.LINE_AA)
    cv2.line(frame, (margin_x + 30, margin_y + 55), (W-margin_x - 30, margin_y + 55), (40, 40, 50), 1)
    
    if desafio_tempos:
        max_t = max([t for n, t in desafio_tempos] + [1])
        for i, (n, t) in enumerate(desafio_tempos):
            bar_h = int((t/max_t) * 150)
            x_b = margin_x + 50 + i*90
            cv2.rectangle(frame, (x_b, H-margin_y-80), (x_b+40, H-margin_y-80-bar_h), COLOR_GREEN, -1)
            cv2.putText(frame, f"{t:.1f}s", (x_b, H-margin_y-80-bar_h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_WHITE, 1, cv2.LINE_AA)
            cv2.putText(frame, f"#{n}", (x_b+5, H-margin_y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1, cv2.LINE_AA)
        
        avg_t = sum(t for n, t in desafio_tempos)/len(desafio_tempos)
        cv2.putText(frame, t("avg").format(f"{avg_t:.2f}"), (W//2-60, H-margin_y-25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_GREEN, 1, cv2.LINE_AA)
    else:
        cv2.putText(frame, t("dashboard_empty"), (W//2-130, H//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1, cv2.LINE_AA)

def draw_game_over(frame, W, H, melhor_tempo):
    """Draws the Game Over screen with options to try again or go to tutorial."""
    margin_x, margin_y = 150, 150
    roi = frame[margin_y:H-margin_y, margin_x:W-margin_x]
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        blurred = cv2.GaussianBlur(roi, (25, 25), 0)
        overlay = blurred.copy()
        cv2.rectangle(overlay, (0, 0), (W-2*margin_x, H-2*margin_y), (30, 15, 15), -1)
        frame[margin_y:H-margin_y, margin_x:W-margin_x] = cv2.addWeighted(blurred, 0.4, overlay, 0.6, 0)
        
    draw_rounded_rect(frame, (margin_x, margin_y), (W-margin_x, H-margin_y), COLOR_RED, 1, 15)

    cv2.putText(frame, t("msg_game_over"), (W//2-90, margin_y + 60), cv2.FONT_HERSHEY_DUPLEX, 1.0, COLOR_RED, 1, cv2.LINE_AA)
    cv2.putText(frame, t("msg_too_many_errors"), (W//2-90, margin_y + 90), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

    if melhor_tempo < 999.0:
        record_text = t("best_record").format(f"{melhor_tempo:.2f}")
        cv2.putText(frame, record_text, (W//2-100, margin_y + 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_CYAN, 1, cv2.LINE_AA)

    # Botões de Game Over
    btn_y = H - margin_y - 80
    draw_rounded_rect(frame, (W//2-140, btn_y), (W//2-10, btn_y+45), (20, 35, 20), -1, 8)
    draw_rounded_rect(frame, (W//2-140, btn_y), (W//2-10, btn_y+45), COLOR_GREEN, 1, 8)
    cv2.putText(frame, t("btn_try"), (W//2-105, btn_y+28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_GREEN, 1, cv2.LINE_AA)

    draw_rounded_rect(frame, (W//2+10, btn_y), (W//2+140, btn_y+45), (35, 35, 20), -1, 8)
    draw_rounded_rect(frame, (W//2+10, btn_y), (W//2+140, btn_y+45), COLOR_CYAN, 1, 8)
    cv2.putText(frame, t("btn_tutorial"), (W//2+35, btn_y+28), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_CYAN, 1, cv2.LINE_AA)

