# pyrefly: ignore [missing-import]
import cv2
import time
import random
import os
# pyrefly: ignore [missing-import]
import numpy as np
from config.settings import *
from config.colors import *
from config.medals import *
from storage.data_handler import carregar_dados, salvar_dados
from ui.drawing_utils import ParticleSystem, pre_process_hand_guide, draw_rounded_rect
from ui.top_navigation import draw_top_menu
from ui.hud import draw_hud
from ui.hand_guide_panel import draw_hand_guide_widget
from ui.popups import draw_achievement_popup
from ui.dashboard import draw_dashboard
from ui.medals_gallery import desenhar_vitrine_medalhas
from ui.game_over import draw_game_over
from tracking.hand_detector import HandTracker
from audio.sound_manager import VoiceFeedback
from utils.locales import t, cycle_lang, get_current_lang
from core.events import handle_mouse_click
from core.game_logic import check_game_logic

class BinaryHandApp:
    def __init__(self):
        # Configuration and state
        self.modo = "LIVRE"
        self.melhor_tempo, self.progresso_tutorial, self.conquistas_destravadas = carregar_dados()
        
        # Game State
        self.numero_alvo = 1
        self.sucesso_frames = 0
        self.flash_timer = 0
        self.flash_erro_timer = 0
        self.aba_medalhas = False
        self.mostrar_dash = False
        self.acertos = 0
        self.erros = 0
        self.tempo_inicio = 0
        self.tempo_round = 0
        self.desafio_tempos = []
        self.popup_timer = 0
        self.popup_nome = ""
        self.game_over = False
        self.ultimo_valor_falado = -1
        self.frames_estabilidade_livre = 0
        self.frames_erro_tutorial = 0
        self.medalhas_page = 0

        # Modules
        self.particles = ParticleSystem()
        self.tracker = HandTracker()
        self.voice = VoiceFeedback()
        
        # Resources
        self.mao_tutorial = pre_process_hand_guide("guia.png")
        
        # Display setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.camera_failed = not self.cap.isOpened()
        
        # Enforce canvas size
        self.W = 960
        self.H = 720
        cv2.namedWindow("HandBits")
        cv2.setMouseCallback("HandBits", self._handle_mouse_click)

    def _handle_mouse_click(self, event, x, y, flags, param):
        handle_mouse_click(self, event, x, y, flags, param)



    def _draw_ui(self, frame, total_val):
        """Draws all UI elements (buttons, HUD, progress, popups)."""
        # 1. Particles update
        self.particles.update(frame)
        
        # 2. Tutorial progress bar (top edge)
        prog_w = int(self.W * (self.progresso_tutorial / 1023))
        cv2.rectangle(frame, (0, 0), (prog_w, 8), COLOR_CYAN, -1)
        
        # 3. Top Menu & Mode Buttons
        draw_top_menu(frame, self.W, self.H, self.modo, self.aba_medalhas, self.voice.active)

        # 4. HUD
        draw_hud(frame, self.W, self.H, self.modo, total_val, self.numero_alvo, self.acertos, self.erros, self.tempo_inicio, self.tempo_round, self.melhor_tempo)
        
        # 5. Dashboard overlay
        if self.mostrar_dash:
            draw_dashboard(frame, self.W, self.H, self.desafio_tempos)
        
        # 6. Medal Gallery overlay
        if self.aba_medalhas:
            desenhar_vitrine_medalhas(frame, self.W, self.H, self.conquistas_destravadas, self.medalhas_page)
            
        # 7. Achievement Popup
        if self.popup_timer > 0:
            draw_achievement_popup(frame, self.W, self.H, self.popup_timer, self.popup_nome)
            self.popup_timer -= 1
            
        # 8. Success / Error Flashes
        if self.flash_timer > 0:
            overlay_f = frame.copy()
            cv2.rectangle(overlay_f, (0, 0), (self.W, self.H), COLOR_GREEN, -1)
            cv2.addWeighted(overlay_f, self.flash_timer / 60.0, frame, 1 - self.flash_timer / 60.0, 0, frame)
            self.flash_timer -= 1
            
        if self.flash_erro_timer > 0:
            overlay_e = frame.copy()
            cv2.rectangle(overlay_e, (0, 0), (self.W, self.H), COLOR_RED, -1)
            cv2.addWeighted(overlay_e, self.flash_erro_timer / 30.0, frame, 1 - self.flash_erro_timer / 30.0, 0, frame)
            self.flash_erro_timer -= 1

        # 9. Tutorial Hand Guide
        if self.modo == "TUTORIAL" and not self.aba_medalhas and not self.mostrar_dash and not self.game_over:
            draw_hand_guide_widget(frame, self.W, self.H, self.mao_tutorial, self.numero_alvo)

        # 10. Game Over Screen
        if self.game_over:
            draw_game_over(frame, self.W, self.H, self.melhor_tempo)



    def run(self):
        while True:
            if not self.camera_failed:
                ret, frame = self.cap.read()
                if not ret: 
                    self.camera_failed = True
            
            if self.camera_failed:
                frame = np.zeros((self.H, self.W, 3), dtype=np.uint8)
                cv2.putText(frame, "ERRO DA CAMERA / CAMERA ERROR", (50, self.H//2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_RED, 2, cv2.LINE_AA)
                cv2.putText(frame, "Nenhuma camera encontrada ou permissao negada.", (50, self.H//2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 1, cv2.LINE_AA)
                cv2.putText(frame, "Pressione 'Q' para sair.", (50, self.H//2 + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 1, cv2.LINE_AA)
            else:
                frame = cv2.flip(frame, 1)
                frame = cv2.resize(frame, (self.W, self.H))
                
                total_val, _ = self.tracker.process(frame)
                
                check_game_logic(self, total_val)
                self._draw_ui(frame, total_val)
                
            cv2.imshow('HandBits', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
                
        self.cap.release()
        cv2.destroyAllWindows()
