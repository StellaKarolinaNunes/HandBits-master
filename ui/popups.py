import cv2
from config.colors import COLOR_WHITE, COLOR_CYAN
from utils.locales import t
from ui.drawing_utils import draw_rounded_rect

def draw_achievement_popup(frame, W, H, popup_timer, popup_nome):
    """Draws achievement unlock popup with modern card style and shadow."""
    # Ease out slide animation
    target_y = H // 2 - 50
    start_y = H + 100
    
    # Simple interpolation based on timer (60 to 0)
    # 60 to 45: slide up
    # 45 to 15: hold
    # 15 to 0: slide down
    if popup_timer > 45:
        progress = (60 - popup_timer) / 15.0
        y_pop = int(start_y + (target_y - start_y) * progress)
    elif popup_timer < 15:
        progress = popup_timer / 15.0
        y_pop = int(start_y + (target_y - start_y) * progress)
    else:
        y_pop = target_y

    pop_w, pop_h = 420, 90
    pop_x = W // 2 - pop_w // 2

    # Draw Shadow
    draw_rounded_rect(frame, (pop_x + 5, y_pop + 5), (pop_x + pop_w + 5, y_pop + pop_h + 5), (15, 15, 15), -1, 15)
    
    # Draw Background
    draw_rounded_rect(frame, (pop_x, y_pop), (pop_x + pop_w, y_pop + pop_h), (40, 30, 20), -1, 15)
    
    # Draw Border
    draw_rounded_rect(frame, (pop_x, y_pop), (pop_x + pop_w, y_pop + pop_h), COLOR_CYAN, 2, 15)

    txt1 = t("new_medal")
    ts1 = cv2.getTextSize(txt1, cv2.FONT_HERSHEY_DUPLEX, 0.6, 1)[0]
    cv2.putText(frame, txt1, (W // 2 - ts1[0] // 2, y_pop + 30), cv2.FONT_HERSHEY_DUPLEX, 0.6, (200, 200, 200), 1, cv2.LINE_AA)
    
    ts2 = cv2.getTextSize(popup_nome, cv2.FONT_HERSHEY_DUPLEX, 0.8, 2)[0]
    cv2.putText(frame, popup_nome, (W // 2 - ts2[0] // 2, y_pop + 65), cv2.FONT_HERSHEY_DUPLEX, 0.8, COLOR_CYAN, 2, cv2.LINE_AA)

