import re

from src.controller.LLM_system import LLM
from src.controller.TTS_system import TTS

print("Initialisation")

IA = LLM("ollama", "mistral")
tts = TTS("CUDA")
tts.init()
IA.init()

print(IA)
print(tts)

msg = ""
while msg != "quit":
    msg = input("\nQuel est votre question : ")
    if msg != "quit":
        IA.question(msg)
        stream = IA.get_stream()

        if stream != None:
            segment_accumulator = ''
            for chunk in stream:

                msg_content = chunk['message']['content']
                segments = msg_content

                for segment in segments:
                    print(segment, end='', flush=True)
                    segment_accumulator += segment
                    if segment in ',.!?;:\n':
                        tts.speak(segment_accumulator)
                        segment_accumulator = ''

            if segment_accumulator:
                tts.speak(segment_accumulator)

            tts.wait()

tts.shutdown()