import socketio
import time
import threading

sio = socketio.Client()

def background_connect():
    """
    Фонова функція, яка постійно намагається підключитися до сервера.
    """
    while True:
        try:
            sio.connect('http://192.168.1.107:5000')
            print("Підключення встановлено")
            break
        except Exception as e:
            print(f"Не вдалося підключитися до сервера. Повторна спроба через 5 секунд... {e}")
            time.sleep(5)

def send_message(message):
    """
    Функція для відправлення повідомлення на сервер.
    
    Parameters:
    message (str): Повідомлення, яке потрібно надіслати.
    """
    if sio.connected:
        sio.emit('message', message)
    else:
        print("Не вдалося надіслати повідомлення. Підключення до сервера відсутнє.")

# Запуск підключення у фоновому режимі
threading.Thread(target=background_connect, daemon=True).start()
