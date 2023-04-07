import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_TOKEN = os.getenv('WEATHER_API_TOKEN')
AI_API_TOKEN = os.getenv('AI_API_TOKEN')
ID_AUTH_USERS = os.getenv('ID_AUTH_USERS').split(',')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
