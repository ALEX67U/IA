import torch
from TTS.api import TTS
import os



# Check if CUDA is available and select device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}\n")

# Print available tts models
view_models = input("View models? [y/n]\n")
if view_models == "y":
    tts_manager = TTS().list_models()
    all_models = tts_manager.list_models()
    print("tts models:\n", all_models, "\n", sep="")

# Prompt model selection
model_name = "tts_models/multilingual/multi-dataset/your_tts"  # Pre-select the multilingual model

# Initialize the tts with the selected model
tts = TTS(model_name, progress_bar=True).to(device)  # Move tts model to the selected device

# Define the path to the speaker audio file
speaker_wav_path = "data/input/tts/wavs/waifu.wav"
if not os.path.exists(speaker_wav_path):
    print(f"Error: The file '{speaker_wav_path}' does not exist.")
    quit()

# Synthesize and save the output with adjusted speed
tts.tts_to_file("les chemins relatifs et le fonctionnement des files d'attente correspondent à la structure réelle de votre projet.",
                speaker_wav=speaker_wav_path, language="fr-fr", file_path="data/output/tts/wavs/output.wav")
