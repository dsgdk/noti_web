
# Telegram Keyword Monitor v3

**Telegram Keyword Monitor v3** is the third version of the application for monitoring Telegram channels for messages with specific keywords. In this version, a local web application is used instead of a desktop interface. The project was created to monitor potential missile threats to my city.

## Features

- **Keyword Monitoring**: Monitors multiple Telegram channels for predefined keywords.
- **Graphical Web Interface**: Launches a local web application where threat messages are displayed and a sound alert is triggered.
- **Customizable**: Easily add channels, keywords, and change the alert sound using a configuration file.

## Requirements

- Python 3.7+
- [Telethon](https://github.com/LonamiWebs/Telethon)
- Flask
- HTML/CSS

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dsgdk/noti_web.git
    cd noti_web
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure the application:

    - Edit the `config.ini` file to add your Telegram API credentials, channels to monitor, and keywords to search for.

4. Prepare the sound file:

    - Place your `.mp3` sound file in the `sounds` directory.

5. Run the web application:

    ```bash
    python server.py
    ```

6. Run the Telegram monitor:

    ```bash
    python app.py
    ```

## Configuration

Edit the `config.ini` (or `config-example.ini`) file to customize the application's settings:

```ini
[Telegram]
api_id = YOUR_API_ID
api_hash = YOUR_API_HASH

[personal_channel]
my_channel = your_channel

[channels]
channels = sumyregion, glukhovalarm, sumyinside, tkdanka

[keywords]
keywords = keyword1, keyword2, keyword3

[danger_keywords]
keywords = danger1, danger2, danger3

[news_keywords]
keywords = news1, news2, news3

[server]
ip_address = 0.0.0.0
port = 5000
```

## Usage

Edit the `config-example.ini` file. Run the `server.py` and `app.py` files, and navigate to the link provided in the terminal to access the application. Use the "Stop" button to stop the sound and the "Clear" button to clear the message output window.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.