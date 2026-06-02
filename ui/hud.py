import cv2
import time
from config.colors import *
from utils.locales import t
from ui.drawing_utils import draw_rounded_rect

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
            # Hits Circular Bar
            cx1, cy1 = offset_x + 10, y1 + 45
            cv2.circle(frame, (cx1, cy1), 12, (30, 40, 30), 2, cv2.LINE_AA)
            if acertos > 0:
                cv2.ellipse(frame, (cx1, cy1), (12, 12), -90, 0, (acertos/5)*360, COLOR_GREEN, 2, cv2.LINE_AA)
            cv2.putText(frame, str(acertos), (cx1-4, cy1+4), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_GREEN, 1, cv2.LINE_AA)

            # Misses Circular Bar
            cx2, cy2 = cx1 + 45, cy1
            cv2.circle(frame, (cx2, cy2), 12, (40, 30, 30), 2, cv2.LINE_AA)
            if erros > 0:
                cv2.ellipse(frame, (cx2, cy2), (12, 12), -90, 0, (erros/5)*360, COLOR_RED, 2, cv2.LINE_AA)
            cv2.putText(frame, str(erros), (cx2-4, cy2+4), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_RED, 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, f"{t('prog')}: {numero_alvo}/1023", (offset_x, y1 + 52), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 200, 0), 1, cv2.LINE_AA)
    
    # Maior Recorde (fora do Hud para destaque)
    if melhor_tempo < 999.0:
        cv2.putText(frame, f"{t('record')}: {melhor_tempo:.2f}s", (W - 180, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_CYAN, 1, cv2.LINE_AA)
