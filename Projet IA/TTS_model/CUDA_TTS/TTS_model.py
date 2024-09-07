import time

import torch
from TTS.api import TTS  # Assurez-vous que l'importation est correcte selon votre structure de dossier
import os
import queue
import threading
import sounddevice as sd
import soundfile as sf

class TTS_model:
    def __init__(self, paused=True):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}\n")

        self.current_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.current_directory = self.current_directory.replace("\\", "/")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to(self.device)
        self.wav_path = os.path.join(self.current_directory, "data/input/tts/wavs/voice.wav")
        print(self.wav_path)
        self.gen_queue = queue.Queue()
        self.play_queue = queue.Queue()
        self.gen_thread = threading.Thread(target=self._gen_worker)
        self.play_thread = threading.Thread(target=self._play_worker)
        self.num = 0
        self.event = threading.Event()
        self.paused = paused
        if not paused:
            self.event.set()
        self.gen_thread.start()
        self.play_thread.start()

    def _gen_worker(self):
        while True:
            text = self.gen_queue.get()
            if text is None:
                break
            self.event.wait()  # Attendre le signal pour continuer
            output_path = os.path.join(self.current_directory, f"data/output/tts/wavs/output{self.num}.wav")
            self.tts.tts_to_file(text, speaker_wav=self.wav_path, language="fr", file_path=output_path)
            self.play_queue.put(output_path)
            self.gen_queue.task_done()
            self.num += 1

    def _play_worker(self):
        while True:
            file_path = self.play_queue.get()
            if file_path is None:
                break
            self.event.wait()  # Attendre le signal pour continuer
            data, samplerate = sf.read(file_path)
            if data.size > 0:
                sd.play(data, samplerate)
                sd.wait()
            self.play_queue.task_done()

    def speak(self, text):
        self.gen_queue.put(text)

    def wait(self):
        if self.paused:
            self.event.set()  # Débloquer les threads
        self.gen_queue.join()
        self.play_queue.join()
        if self.paused:
            self.event.clear()  # Revenir à l'état de pause après le traitement

    def shutdown(self):
        self.gen_queue.put(None)
        self.play_queue.put(None)
        self.gen_thread.join()
        self.play_thread.join()

if __name__ == "__main__":
    # Initialisation avec démarrage immédiat des threads sans pause
    tts_model_no_pause = TTS_model(paused=True)
    print("message sans pause")
    tts_model_no_pause.speak("Message sans pause.")
    print("2222222")
    tts_model_no_pause.wait()
    tts_model_no_pause.speak("Message sans pause.")
    print("pause.")
    time.sleep(5)
    print("test")
    tts_model_no_pause.speak("Message sans pause.")
    print("test2")
    tts_model_no_pause.wait()
    tts_model_no_pause.shutdown()
    print("Tous les messages ont été traités et les threads sont fermés pour le mode sans pause.")
