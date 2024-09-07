import importlib
import traceback


class TTS:

    def __init__(self, type):
        self.type = type
        self.module = None
        self.module_instance = None

    def init(self):
        try:
            self.module = importlib.import_module(f"TTS_model.{self.type}_TTS.TTS_model")
            self.module_instance = self.module.TTS_model()
        except ModuleNotFoundError as e:
            print(f"Erreur: Module non trouvé! Type: {type(e).__name__}, Message: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"Une exception s'est produite. Type: {type(e).__name__}, Message: {e}")
            traceback.print_exc()

    def speak(self, text):
        if(isinstance(text, str)):
            if(len(text) > 2):
                if self.module_instance:
                    self.module_instance.speak(text)
                else:
                    print("Le module n'a pas été initialisé correctement.")

    def wait(self):
        if self.module_instance:
            self.module_instance.wait()
        else:
            print("Le module n'a pas été initialisé correctement.")

    def shutdown(self):
        if self.module_instance:
            self.module_instance.shutdown()
        else:
            print("Le module n'a pas été initialisé correctement.")

    def __str__(self):
        return f"LLM(type={self.type}, module={self.module})"
