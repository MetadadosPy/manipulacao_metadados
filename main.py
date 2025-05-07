import whisper
import os
import json
import warnings

# Oculta aviso sobre FP16
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# Solicita o caminho do arquivo ao usuário
audio_path = input("Digite o caminho completo do arquivo .mp3: ").strip()

# Verifica se o arquivo existe
if not os.path.isfile(audio_path):
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
    exit(1)

# Carrega o modelo Whisper
print("Carregando o modelo Whisper...")
model = whisper.load_model("base")

# Transcreve o áudio
print("Transcrevendo o áudio...")
result = model.transcribe(audio_path, language="pt")

# Mostra no console
print("\nTranscrição completa:")
print(result["text"])

# Define nomes de saída com base no nome do arquivo
base_name = os.path.splitext(os.path.basename(audio_path))[0]
txt_filename = f"{base_name}.txt"
json_filename = f"{base_name}.json"

# Salva transcrição em TXT (somente texto)
with open(txt_filename, "w", encoding="utf-8") as txt_file:
    txt_file.write(result["text"])

# Salva resultado completo em JSON
with open(json_filename, "w", encoding="utf-8") as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=2)

print(f"\nTranscrição salva como:\n- {txt_filename}\n- {json_filename}")
# para usar , digite o caminho exato onde o audio se encontra e a extensao
