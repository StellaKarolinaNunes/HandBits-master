import cv2
from config.colors import COLOR_CYAN, COLOR_GREEN, COLOR_WHITE
from utils.locales import t
from ui.drawing_utils import draw_rounded_rect

def draw_dashboard(frame, W, H, desafio_tempos):
    """Draws performance dashboard with modern Glassmorphism and Cards."""
    margin_x, margin_y = 100, 100
    roi = frame[margin_y:H-margin_y, margin_x:W-margin_x]
    
    if roi.shape[0] > 0 and roi.shape[1] > 0:
        blurred = cv2.GaussianBlur(roi, (35, 35), 0)
        overlay_blur = blurred.copy()
        cv2.rectangle(overlay_blur, (0, 0), (W-2*margin_x, H-2*margin_y), (25, 20, 25), -1)
        frame[margin_y:H-margin_y, margin_x:W-margin_x] = cv2.addWeighted(blurred, 0.3, overlay_blur, 0.7, 0)
    
    draw_rounded_rect(frame, (margin_x, margin_y), (W-margin_x, H-margin_y), COLOR_CYAN, 2, 15)
    
    if not desafio_tempos:
        cv2.putText(frame, t("dashboard_empty"), (W//2-130, H//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, cv2.LINE_AA)
        return
        
    avg_t = sum(t for n, t in desafio_tempos)/len(desafio_tempos)
    
    # Header Card
    card1_y = margin_y + 30
    draw_rounded_rect(frame, (margin_x + 30, card1_y), (W - margin_x - 30, card1_y + 80), (45, 40, 50), -1, 10)
    cv2.putText(frame, t("performance"), (margin_x + 50, card1_y + 35), cv2.FONT_HERSHEY_DUPLEX, 0.8, COLOR_CYAN, 1, cv2.LINE_AA)
    cv2.putText(frame, t("avg").format(f"{avg_t:.2f}"), (margin_x + 50, card1_y + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_GREEN, 1, cv2.LINE_AA)
    
    # Graph Card
    card2_y = card1_y + 100
    card2_h = H - margin_y - card2_y - 30
    draw_rounded_rect(frame, (margin_x + 30, card2_y), (W - margin_x - 30, card2_y + card2_h), (35, 30, 40), -1, 10)
    
    max_t = max([t for n, t in desafio_tempos] + [1])
    for i, (n, t_val) in enumerate(desafio_tempos):
        bar_max_h = card2_h - 60
        bar_h = int((t_val/max_t) * bar_max_h)
        x_b = margin_x + 60 + i*110
        y_b = card2_y + card2_h - 30
        
        # Bar track
        cv2.rectangle(frame, (x_b, y_b - bar_max_h), (x_b+50, y_b), (20, 20, 25), -1)
        # Bar fill
        cv2.rectangle(frame, (x_b, y_b - bar_h), (x_b+50, y_b), COLOR_GREEN, -1)
        
        cv2.putText(frame, f"{t_val:.1f}s", (x_b+2, y_b - bar_h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        cv2.putText(frame, f"#{n}", (x_b+10, y_b + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1, cv2.LINE_AA)

