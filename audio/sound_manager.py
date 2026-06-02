import threading
import os
from utils.locales import t

def obter_instrucao_voz(numero, inicio=False):
    valores = [
        (1, "v_thumb_r"),
        (2, "v_index_r"),
        (4, "v_middle_r"),
        (8, "v_ring_r"),
        (16, "v_pinky_r"),
        (32, "v_thumb_l"),
        (64, "v_index_l"),
        (128, "v_middle_l"),
        (256, "v_ring_l"),
        (512, "v_pinky_l")
    ]
    
    dedos_usados = []
    valores_usados = []
    for val, nome_key in valores:
        if numero & val:
            dedos_usados.append(t(nome_key))
            valores_usados.append(str(val))
            
    if len(dedos_usados) == 1:
        explicacao = t("v_form_one").format(numero=numero, dedo=dedos_usados[0], valor=valores_usados[0])
    elif len(dedos_usados) == 10:
        explicacao = t("v_form_all").format(numero=numero)
    else:
        partes = [f"o {d} que vale {v}" for d, v in zip(dedos_usados, valores_usados)]
        if len(partes) > 1:
            lista_dedos = t("v_and").join([", ".join(partes[:-1]), partes[-1]])
            soma_str = t("v_plus").join(valores_usados)
            explicacao = t("v_form").format(numero=numero, dedos=lista_dedos, soma=soma_str)
        else:
            explicacao = t("v_form_one").format(numero=numero, dedo=dedos_usados[0], valor=valores_usados[0])

    if inicio:
        return f"{explicacao} {t('v_guide')}"
    else:
        return explicacao

class VoiceFeedback:
    def __init__(self, active=True):
        self.active = active

    def falar(self, texto):
        """Sends text to system speech engine."""
        if self.active:
            lang = t("spd_say_lang")
            voice = t("spd_say_voice")
            def run(): 
                # spd-say with slower rate, lower pitch and localized voice type for better clarity
                os.system(f"spd-say -l {lang} -r -25 -p -15 -t {voice} '{texto}' > /dev/null 2>&1")
            threading.Thread(target=run).start()

    def play_sound(self, sound_type):
        """Plays a distinct sound effect using system tools."""
        if self.active:
            def run_sound():
                if sound_type == "success":
                    os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga > /dev/null 2>&1")
                elif sound_type == "error":
                    os.system("paplay /usr/share/sounds/freedesktop/stereo/suspend-error.oga > /dev/null 2>&1")
            threading.Thread(target=run_sound).start()
