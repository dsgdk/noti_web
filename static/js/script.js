// Перевірте, чи URL звуку вірний
const alertSoundUrl = window.alertSoundUrl || '/static/sounds/alert.mp3';
const alertSound = new Audio(alertSoundUrl);

// Підключення до SocketIO
const socket = io();

// Обробка повідомлень від сервера
socket.on('response', function(data) {
    const textDisplay = document.getElementById('text-display');
    textDisplay.innerText = data.data;
    
    // Перевірка, чи звук можна відтворити
    alertSound.play().catch(error => {
        console.error('Error playing sound:', error);
    });
});

// Обробка натискання кнопки "Очистити"
document.getElementById('clear-button').addEventListener('click', function() {
    document.getElementById('text-display').innerText = '';
});

// Обробка натискання кнопки "Стоп"
document.getElementById('stop-button').addEventListener('click', function() {
    alertSound.pause(); // Зупинка звуку
    alertSound.currentTime = 0; // Перемотування на початок
});
