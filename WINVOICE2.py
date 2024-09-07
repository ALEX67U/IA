from TTS.api import TTS

# Créer une instance de tts avec le modèle spécifique
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

# Texte à synthétiser
text = "Hello, how are you today?"

# Synthèse vocale
audio_path = "output.wav"
tts.tts_to_file(text=text, file_path=audio_path)

print(f"Audio généré et sauvegardé à {audio_path}")
