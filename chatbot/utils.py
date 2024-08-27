def format_response(response_text):
    """
    Formatea la respuesta del bot para que sea enviada como JSON.
    :param response_text: Texto de la respuesta generada por el bot.
    :return: Diccionario con el formato de respuesta.
    """
    return {
        'response': response_text
    }
