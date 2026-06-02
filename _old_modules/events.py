import cv2
import os
from config.medals import CONQUISTAS
from utils.locales import cycle_lang, t
from storage.data_handler import salvar_dados
from .game_logic import set_mode

def handle_mouse_click(app, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Dashboard handles its own exit on click
        if app.mostrar_dash:
            app.mostrar_dash = False
            app.modo = "LIVRE"
            return

        if app.game_over:
            # Botões de Game Over centralizados
            margin_y = 150
            btn_y = app.H - margin_y - 80
            if btn_y < y < btn_y+45:
                if app.W//2-140 < x < app.W//2-10:
                    set_mode(app, "DESAFIO")
                elif app.W//2+10 < x < app.W//2+140:
                    set_mode(app, "TUTORIAL")
            return

        # Top Menu Buttons
        if 15 < y < 60:
            total_menu_width = 6 * 104 + 95 # 7 buttons now
            start_x = (app.W - total_menu_width) // 2
            for i in range(7):
                bx1 = start_x + i * 104
                bx2 = bx1 + 95
                if bx1 < x < bx2:
                    if i == 0: set_mode(app, "LIVRE")
                    elif i == 1: set_mode(app, "TUTORIAL")
                    elif i == 2: set_mode(app, "DESAFIO")
                    elif i == 3:
                        app.aba_medalhas = not app.aba_medalhas
                        app.mostrar_dash = False
                    elif i == 4: # LANG
                        cycle_lang()
                    elif i == 5: # SOM
                        app.voice.active = not app.voice.active
                    elif i == 6: # SAIR
                        app.cap.release()
                        cv2.destroyAllWindows()
                        os._exit(0)
                    return

        # Medalhas pagination
        if app.aba_medalhas:
            if app.H//2 - 40 < y < app.H//2 + 40:
                if 20 < x < 100:
                    app.medalhas_page = max(0, app.medalhas_page - 1)
                    return
                elif app.W - 100 < x < app.W - 20:
                    max_page = (len(CONQUISTAS) - 1) // 8
                    app.medalhas_page = min(max_page, app.medalhas_page + 1)
                    return

        # Restart Tutorial (Bottom HUD)
        if app.modo == "TUTORIAL" and not app.aba_medalhas and not app.mostrar_dash:
             y1 = app.H - 90 # hud_h is 70, offset 20
             if (195 < x < 260) and (y1 + 35 < y < y1 + 60):
                 app.progresso_tutorial = 1
                 app.numero_alvo = 1
                 print("[HandBits] Tutorial Reiniciado!")
                 app.voice.falar(t("voice_restart"))
                 salvar_dados(app.melhor_tempo, app.progresso_tutorial, app.conquistas_destravadas)
                 return
