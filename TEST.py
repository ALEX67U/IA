import pyttsx3
import queue
import threading
import time

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.queue = queue.Queue()
        self.event = threading.Event()
        self.worker_thread = threading.Thread(target=self._worker)
        self.worker_thread.start()

    def _worker(self):
        while True:
            text = self.queue.get()
            if text is None:
                break
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
            self.event.set()

    def speak(self, text):
        self.queue.put(text)

    def wait_for_empty_queue(self):
        while not self.queue.empty():
            self.event.wait(timeout=1.0)

    def shutdown(self):
        self.queue.put(None)
        self.worker_thread.join()

if __name__ == "__main__":
    tts = TTS()

    tts.speak("Premier message à dire.")
    tts.speak("Deuxième message à dire.")
    tts.speak("Troisième message à dire.")

    tts.wait_for_empty_queue()

    tts.shutdown()
