import logging
import openai

import config

openai.api_key = config.AI_API_TOKEN


# направляем запрос ИИ через АПИ и получаем ответ
async def get_response(message):
    try:
        response = await openai.Completion.acreate(
            engine="text-davinci-003",
            prompt='"""\n{}\n"""'.format(message),
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0)
        logging.info(f'NEW AI QUERY : {message}\n AI ANSWER :'
                     f' {response["choices"][0]["text"]}')
        return response['choices'][0]['text']
    except Exception as error:
        logging.info(f'{error}')