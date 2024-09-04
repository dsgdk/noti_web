# MIT License
# 
# Copyright (c) 2024 dsgdk
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

import re
from telethon import TelegramClient, events
from socket_module import send_message
import configparser
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Завантаження конфігурації
config = configparser.ConfigParser()
config.read('config.ini')

api_id = config.get('telegram', 'api_id')
api_hash = config.get('telegram', 'api_hash')
channels = config.get('channels', 'channels').split(', ')
keywords = config.get('keywords', 'keywords').split(', ')
my_channel = config.get('personal_channel', 'my_channel')
my_channel_link = config.get('personal_channel', 'my_channel')

# Слова, що можуть вказувати на небезпеку
danger_keywords = config.get('danger_keywords', 'keywords').split(', ')

# Слова, що можуть вказувати на новини чи зведення
news_keywords = config.get('news_keywords', 'keywords').split(', ')

client = TelegramClient('session_name', api_id, api_hash)

def is_relevant(message):
    message_lower = message.lower()

    # Перевірка наявності ключових слів для населеного пункту
    relevant_location = any(keyword.lower() in message_lower for keyword in keywords)
    
    # Перевірка наявності слів, що вказують на небезпеку
    danger_detected = any(danger in message_lower for danger in danger_keywords)
    
    # Перевірка наявності слів, що вказують на новини чи зведення
    is_news = any(news.lower() in message_lower for news in news_keywords)
    
    # Додаткова перевірка на релевантність: повідомлення не має бути зведенням
    if is_news:
        return False

    # Повідомлення вважається релевантним лише якщо воно містить ключові слова для населеного пункту та слова, що вказують на небезпеку
    return relevant_location and danger_detected

def generate_alert_message(channel_name, message_text, channel_username=None):
    message_lower = message_text.lower()
    alert_message = ""

    # Перевірка на КАБ
    if any(kw in message_lower for kw in ["каб", "каб-и", "каби"]):
        alert_message = f"Увага! КАБ курсом на Глухів!\n"
        send_message('Увага! КАБ курсом на Глухів')
    # Перевірка на балістику
    elif any(kw in message_lower for kw in ["балістика", "балістичне", "балістики", "балістичного", "балістична"]):
        alert_message = f"Увага! Загроза балістики для Глухова!\n"
        send_message('Увага! Загроза балістики для Глухова!')
    # Перевірка на шахед
    elif any(kw in message_lower for kw in ["шахед", "шахеди", "шахедами", "шахедів"]):
        alert_message = f"Увага! Загроза шахедів для Глухова!\n"

    if alert_message:
        if channel_username:
            alert_message += f'Джерело: [{channel_name}](https://t.me/{channel_username})\n\n'
        else:
            alert_message += f'Джерело: {channel_name}\n\n'
        alert_message += f'[Підписатися на нас](https://t.me/{my_channel_link})'
    
    return alert_message

async def send_to_channel(text):
    """Надсилає повідомлення до вашого особистого каналу."""
    try:
        await client.send_message(my_channel, text, link_preview=False)
        logger.info(f"Message sent to channel: {text}")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

async def start_telegram_client():
    """Запуск Telegram клієнта та обробка нових повідомлень."""
    await client.start()

    @client.on(events.NewMessage)
    async def handler(event):
        if event.chat.username in channels:
            if is_relevant(event.raw_text):
                channel_name = event.chat.title or event.chat.username
                channel_username = event.chat.username
                message_text = event.raw_text
                logger.info(f"Relevant message found: {channel_name}, {message_text}")
                
                # Формування повідомлення про небезпеку
                alert_message = generate_alert_message(channel_name, message_text, channel_username)
                
                if alert_message:
                    # Надсилаємо згенероване повідомлення до особистого каналу
                    await send_to_channel(alert_message)

    await client.run_until_disconnected()

# Запуск Telegram клієнта
if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(start_telegram_client())
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
