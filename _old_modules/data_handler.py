import os
import base64
import sys

# Detect if running as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SAVE_FILE = os.path.join(BASE_DIR, "handbits_profile.dat")
CRYPT_KEY = "HANDBITS_SECURE_2026_#"

def _crypt(data_str):
    """Simple XOR cipher to prevent manual editing."""
    return "".join(chr(ord(c) ^ ord(k)) for c, k in zip(data_str, CRYPT_KEY * (len(data_str) // len(CRYPT_KEY) + 1)))

def carregar_dados():
    """Returns (melhor_tempo, progresso_tutorial, conquistas_destravadas)"""
    melhor_tempo = 999.0
    progresso_tutorial = 0
    conquistas_destravadas = set()

    # MIGRATION: Se o save antigo existir, converte para o novo binário
    OLD_SAVE = os.path.join(BASE_DIR, "save.dat")
    if os.path.exists(OLD_SAVE):
        try:
            with open(OLD_SAVE, "rb") as f:
                data = base64.b64decode(f.read()).decode("utf-8")
                lines = data.split("\n")
                if len(lines) >= 2:
                    melhor_tempo = float(lines[0].strip())
                    progresso_tutorial = int(lines[1].strip())
                    if len(lines) >= 3:
                        conquistas_str = lines[2].strip()
                        if conquistas_str:
                            conquistas_destravadas = set(conquistas_str.split(","))
            salvar_dados(melhor_tempo, progresso_tutorial, conquistas_destravadas)
            os.remove(OLD_SAVE)
            print("[Sistema] Save antigo migrado para novo formato criptografado.")
            return melhor_tempo, progresso_tutorial, conquistas_destravadas
        except: pass

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "rb") as f:
                decoded_base64 = base64.b64decode(f.read()).decode("utf-8")
                decrypted = _crypt(decoded_base64)
                lines = decrypted.split("\n")
                
                # Check integrity block
                if len(lines) >= 4 and lines[3] == "HANDBITS_VERIFIED":
                    melhor_tempo = float(lines[0].strip())
                    progresso_tutorial = int(lines[1].strip())
                    conquistas_str = lines[2].strip()
                    if conquistas_str:
                        conquistas_destravadas = set(conquistas_str.split(","))
                    print(f"[Sistema] Dados carregados com segurança de: {SAVE_FILE}")
                else:
                    print("[Erro] Save corrompido ou editado manualmente!")
        except Exception as e: 
            print(f"[Erro] Falha ao carregar save criptografado: {e}")
            
    return melhor_tempo, progresso_tutorial, conquistas_destravadas

def salvar_dados(melhor_tempo, progresso_tutorial, conquistas_destravadas):
    """Saves the current progression state using strong obfuscation/encryption."""
    try:
        raw_data = f"{melhor_tempo}\n{progresso_tutorial}\n{','.join(list(conquistas_destravadas))}\nHANDBITS_VERIFIED"
        encrypted = _crypt(raw_data)
        encoded_data = base64.b64encode(encrypted.encode("utf-8"))
        with open(SAVE_FILE, "wb") as f:
            f.write(encoded_data)
    except Exception as e: 
        print(f"[Erro] Falha ao salvar: {e}")
