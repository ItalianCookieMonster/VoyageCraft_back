from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Crear un bot
chatbot = ChatBot('TravelBot')

# Entrenar el bot (si no lo has hecho previamente)
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Interactuar con el bot
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    response = chatbot.get_response(user_input)
    print(f"Bot: {response}")

