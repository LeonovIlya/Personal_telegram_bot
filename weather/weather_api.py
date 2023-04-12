import json
import logging
from aiohttp import ClientSession
from dataclasses import dataclass
from datetime import datetime as dt

import config


# получаем json через get запрос к api по токену
async def get_json(lat: int, lon: int) -> str:
    async with ClientSession() as session:
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'lat': lat, 'lon': lon, 'appid': config.WEATHER_API_TOKEN,
                  'units': 'metric', 'lang': 'ru'}
        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            try:
                return json.dumps(weather_json)
            except Exception as error:
                logging.info(f'{error}')


# получаем ответ на запрос, парсим, возвращаем текст
async def get_weather(lat: int, lon: int) -> str:
    response = await get_json(lat, lon)
    wthr = parse_response(response)
    return f'📍: {wthr.location}, {wthr.description}\n' \
           f'🌡: {wthr.temperature}°C, ощущается как' \
           f' {wthr.temperature_feeling}°C\n'\
           f'💨: {wthr.wind_speed} м/с\n' \
           f'🌅: {wthr.sunrise.strftime("%H:%M")}\n' \
           f'🌇: {wthr.sunset.strftime("%H:%M")}\n'


# создаем класс weather
@dataclass()
class Weather:
    location: str
    temperature: float
    temperature_feeling: float
    description: str
    wind_speed: float
    sunrise: dt
    sunset: dt


# парсим полученный ответ на запрос
def parse_response(response: str) -> Weather:
    openweather_dict = json.loads(response)
    return Weather(
        location=openweather_dict['name'],
        temperature=openweather_dict['main']['temp'],
        temperature_feeling=openweather_dict['main']['feels_like'],
        description=str(openweather_dict['weather'][0]['description']).capitalize(),
        sunrise=datetime.fromtimestamp(openweather_dict['sys']['sunrise']),
        sunset=datetime.fromtimestamp(openweather_dict['sys']['sunset']),
        wind_speed=openweather_dict['wind']['speed'])
