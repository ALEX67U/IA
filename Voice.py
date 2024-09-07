import ollama
from gtts import gTTS
from playsound import playsound
import os

stream = ollama.chat(
    model='mistral',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

full_response = ""
for chunk in stream:
    content = chunk['message']['content']
    print(content, end='', flush=True)
    full_response += content

# Utilisation de gTTS pour convertir le texte en parole
tts = gTTS(text=full_response, lang='en')
tts.save("response.mp3")

# Lecture du fichier audio généré
playsound("response.mp3")

# Nettoyage du fichier audio après utilisation
os.remove("response.mp3")