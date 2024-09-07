import ollama
import pyttsx3

# Initialisation du moteur tts
engine = pyttsx3.init()

# Lister les voix disponibles
voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} ({voice.id}) - {voice.languages}")

# Choisir une voix spécifique (par exemple, une voix récemment ajoutée)
# Changez l'index pour la voix que vous avez ajoutée
voice_index = 1  # Remplacez par l'index de la voix souhaitée
engine.setProperty('voice', voices[voice_index].id)

# Changer la vitesse
rate = engine.getProperty('rate')
print(f"Default speaking rate: {rate}")
engine.setProperty('rate', 150)  # Ajustez la vitesse (150 mots par minute est plus lent)

# Obtenir la réponse de l'API ollama_LLM
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

# Utilisation du moteur tts pour lire la réponse complète
engine.say(full_response)
engine.runAndWait()
