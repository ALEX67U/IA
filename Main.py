import subprocess

Error = False

def start_ollama_mistral():
    # Commande pour lancer Ollama avec Mistral
    command = "ollama_LLM run mistral"
    # Lancement du processus
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    return process

def communicate_with_process(process, input_text,Error):
    try:
        # Envoyer le texte d'entrée au processus
        stdout, stderr = process.communicate(input=input_text, timeout=60)
        if process.returncode != 0:
            Error = True
            print(f"Error: {stderr}")
        return stdout
    except subprocess.TimeoutExpired:
        process.kill()
        Error = True
        print("Process timeout expired")
        return None

# Lancer Ollama avec Mistral
process = start_ollama_mistral()

# Vérifier si le processus a démarré correctement
if process:
    print("Ollama avec Mistral a démarré avec succès.")

    # Communiquer avec le processus
    while not Error:
        input_text = input("Question: ")
        response = communicate_with_process(process, input_text,Error)
        print(f"Réponse: {response}")

else:
    print("Erreur lors du démarrage d'Ollama avec Mistral.")