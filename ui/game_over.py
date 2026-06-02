import cv2
from config.colors import COLOR_RED, COLOR_CYAN, COLOR_GREEN
from utils.locales import t
from ui.drawing_utils import draw_rounded_rect

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
