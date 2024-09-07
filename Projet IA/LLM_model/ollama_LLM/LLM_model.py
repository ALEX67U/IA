import ollama
import re

class LLM_model:

    def __init__(self, model):
        self.model = model
        self.stream = None

    def get_stream(self):
        return self.stream

    def question(self, content):
        self.stream = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': content}],
            stream=True,
        )

    def __str__(self):
        return f"LLM(model={self.model}, stream={self.stream})"