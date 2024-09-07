import importlib
import traceback


class LLM:

    def __init__(self, type, model):
        self.type = type
        self.model = model
        self.module = None
        self.module_instance = None

    def init(self):
        try:
            self.module = importlib.import_module(f"LLM_model.{self.type}_LLM.LLM_model")
            self.module_instance = self.module.LLM_model(self.model)
        except ModuleNotFoundError as e:
            print(f"Erreur: Module non trouvé! Type: {type(e).__name__}, Message: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"Une exception s'est produite. Type: {type(e).__name__}, Message: {e}")
            traceback.print_exc()

    def question(self, content):
        if self.module_instance:
            self.module_instance.question(content)
        else:
            print("Le module n'a pas été initialisé correctement.")

    def get_stream(self):
        if self.module_instance:
            return self.module_instance.get_stream()
        else:
            print("Le module n'a pas été initialisé correctement.")
            return None

    def __str__(self):
        return f"LLM(type={self.type}, model={self.model}, module={self.module})"
