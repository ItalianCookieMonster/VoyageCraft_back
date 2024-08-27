
from django.http import JsonResponse
from .utils import format_response
from .serializers import ChatbotSerializer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Crear y entrenar el chatbot
chatbot = ChatBot('TravelBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

def get_bot_response(request):
    user_message = request.GET.get('message')
    if user_message:
        bot_response = chatbot.get_response(user_message)
        formatted_response = format_response(bot_response.text)
        data = {'message': user_message, 'response': formatted_response}
        serializer = ChatbotSerializer(data=data)
        if serializer.is_valid():
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'response': 'Sorry, I didn\'t understand that.'})
