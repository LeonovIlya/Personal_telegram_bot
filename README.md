Небольшой личный бот.

Функции:
- текущий прогноз погоды по геолоке
- чат с ИИ chatGPT
- голосовая записная книжка
- напоминания

При первом обращении к боту происходит проверка на доступ к нему. 

### Прогноз погоды
Бот запрашивает геолокацию пользователя, из геолокации получает широту и долготу, оправляет запрос к api [openweathermap](https://openweathermap.org/api),
получает ответ, парсит его и возвращает пользователю сообщение.

### ИИ
Простой текстовый запрос к api [openai](https://platform.openai.com/docs/introduction).

### Записная книжка
Простая голосовая записная книжка для пользователя. Записи хранятся в текстовом файле.
Распознавание голоса через модуль [vosk](https://alphacephei.com/vosk/). Также необходимо установить [ffmpeg](https://ffmpeg.org/).
Можно удалить запись сказав "Удалить [номер_записи]"

### Напоминания
Пользователь устанавливает напоминания самому себе, отправляя боту сообщение с датой и временем. Напоминания хранятся в 
СУБД [PostgreSQL](https://www.postgresql.org/), в качестве ORM - [SQLAlchemy](https://www.sqlalchemy.org/).
Бот парсит сообщение с помощью [rutimeparser](https://pypi.org/project/rutimeparser/), отделяя само напоминание
и дату с временем. В назначенное время и дату бот присылает напоминание, которое можно подтвердить или отложить
на 15 минут/1 час.