import time
import random
from config.medals import CONQUISTAS
from config.colors import COLOR_GREEN, COLOR_RED
from storage.data_handler import salvar_dados
from utils.locales import t
from audio.sound_manager import obter_instrucao_voz

def set_mode(app, mode):
    """Switches game mode and resets relevant timers."""
    app.modo = mode
    app.aba_medalhas = False
    app.medalhas_page = 0
    app.mostrar_dash = False
    app.tempo_round = time.time()
    app.tempo_inicio = time.time()
    app.sucesso_frames = 0
    app.game_over = False
    
    if mode == "TUTORIAL":
        if app.progresso_tutorial >= 1024:
            app.voice.falar(t("voice_completed"))
            app.numero_alvo = 1023
        elif app.progresso_tutorial <= 1:
            app.numero_alvo = 1
            app.voice.falar(t("voice_welcome"))
        else:
            app.numero_alvo = app.progresso_tutorial
            app.voice.falar(obter_instrucao_voz(app.numero_alvo, inicio=True))
    elif mode == "DESAFIO":
        app.numero_alvo = random.randint(1, 1023)
        app.acertos = 0
        app.erros = 0
        app.desafio_tempos = []
        app.voice.falar(f"Iniciando Desafio. Mostre o {app.numero_alvo}")
    elif mode == "LIVRE":
        app.voice.falar("Modo Livre ativado")
        app.ultimo_valor_falado = -1
        app.frames_estabilidade_livre = 0

def check_game_logic(app, current_val):
    """Update logic for Tutorial and Challenge modes."""
    if app.aba_medalhas or app.mostrar_dash or app.game_over:
        return

    if app.modo == "LIVRE":
        if current_val != 0 and current_val == app.ultimo_valor_falado:
            app.frames_estabilidade_livre += 1
            if app.frames_estabilidade_livre == 20: # Falar após ~0.6s estável
                app.voice.falar(str(current_val))
        elif current_val != app.ultimo_valor_falado:
            app.ultimo_valor_falado = current_val
            app.frames_estabilidade_livre = 0
        return

    if current_val == app.numero_alvo:
        app.sucesso_frames += 1
        if app.sucesso_frames >= 12:
            # Target achieved
            t_f = time.time() - app.tempo_round
            app.voice.play_sound("success")
            app.voice.falar(t("v_correct").format(numero=app.numero_alvo))
            app.particles.spawn(app.W // 2, app.H // 2, COLOR_GREEN)
            app.flash_timer = 15
            
            if app.modo == "TUTORIAL":
                if app.numero_alvo == 1023:
                    app.progresso_tutorial = 1024 # Flag de conclusão
                    app.voice.falar(t("v_congratulations"))
                    app.aba_medalhas = True
                    app.modo = "LIVRE"
                else:
                    app.progresso_tutorial = max(app.progresso_tutorial, app.numero_alvo + 1)
                    app.numero_alvo += 1
                    app.voice.falar(obter_instrucao_voz(app.numero_alvo, inicio=False))
                
                check_and_unlock_medals(app, "VAL", app.progresso_tutorial)
                app.frames_erro_tutorial = 0
                salvar_dados(app.melhor_tempo, app.progresso_tutorial, app.conquistas_destravadas)
                print(f"[HandBits] Progresso Tutorial Salvo: {app.progresso_tutorial}")
            
            elif app.modo == "DESAFIO":
                app.desafio_tempos.append((app.numero_alvo, t_f))
                app.acertos += 1
                if app.acertos >= 5:
                    total_time = sum(t for _, t in app.desafio_tempos)
                    if total_time < app.melhor_tempo:
                        app.melhor_tempo = total_time
                    check_and_unlock_medals(app, "TEMPO", total_time)
                    salvar_dados(app.melhor_tempo, app.progresso_tutorial, app.conquistas_destravadas)
                    app.mostrar_dash = True
                    app.voice.falar(t("v_challenge_done"))
                else:
                    app.numero_alvo = random.randint(1, 1023)
                    app.voice.falar(t("v_next").format(numero=app.numero_alvo))
            
            app.tempo_round = time.time()
            app.sucesso_frames = 0

    elif current_val != 0:
        if app.modo == "DESAFIO":
            if random.random() < 0.05:
                app.flash_erro_timer = 5
                app.erros += 1
                app.voice.play_sound("error")
                app.voice.falar(t("v_wrong"))
                app.particles.spawn(random.randint(0, app.W), random.randint(0, app.H), COLOR_RED)
                if app.erros >= 5:
                    app.game_over = True
                    app.voice.falar(t("v_game_over"))
        elif app.modo == "TUTORIAL":
            app.frames_erro_tutorial += 1
            if app.frames_erro_tutorial == 60: # 2 segundos ouvindo o erro
                app.voice.falar("Ainda não. Preste atenção no guia visual abaixo para ver os dedos certos.")
                app.frames_erro_tutorial = 0
    else:
        app.sucesso_frames = 0
        app.frames_erro_tutorial = 0

def check_and_unlock_medals(app, type_str, value):
    """Unlock medals based on progression or time."""
    for cid, nome, alvo, cor, ttype in CONQUISTAS:
        if cid not in app.conquistas_destravadas and ttype == type_str:
            unlocked = (ttype == "VAL" and value >= alvo) or (ttype == "TEMPO" and value <= alvo)
            if unlocked:
                app.conquistas_destravadas.add(cid)
                app.popup_timer = 60
                app.popup_nome = nome
                app.particles.spawn(app.W // 2, app.H // 2, cor)
                salvar_dados(app.melhor_tempo, app.progresso_tutorial, app.conquistas_destravadas)
