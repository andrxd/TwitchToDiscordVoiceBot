# TwitchToDiscordVoiceBot

## Twitch Discord Bot

This project is a Twitch and Discord bot that connects to a Twitch channel, listens to messages, converts them to speech using Google Text-to-Speech (gTTS), and plays the generated audio in a Discord voice channel. The bot supports basic commands to join and leave voice channels in Discord.

### Prerequisites

Before you start, ensure you have the following installed on your machine:

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/andrxd/TwitchToDiscordVoiceBot.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd TwitchToDiscordVoiceBot
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `.env` file in the project directory:

    ```env
    TWITCH_TOKEN=your_twitch_token
    DISCORD_TOKEN=your_discord_token
    CHANNEL_NAME=your_twitch_channel_name
    ```

   Replace `your_twitch_token`, `your_discord_token`, and `your_twitch_channel_name` with your actual Twitch and Discord bot tokens and your desired Twitch channel name.

### Usage

1. **Run the bot:**

    ```bash
    python twitch_discord_bot.py
    ```

   The bot will connect to both Twitch and Discord.

2. **In Discord, use the following commands:**

    - `!join`: Bot joins the voice channel of the user who issued the command.
    - `!leave`: Bot leaves the voice channel.

### Notes

- Ensure that the bot has the necessary permissions to join and leave voice channels in Discord.
- Make sure that your Discord bot is added to the server where you want it to operate.
- The bot will automatically play the speech audio when a message is sent in the connected Twitch channel.

### Dependencies

- [discord.py](https://discordpy.readthedocs.io/) (Discord API wrapper)
- [gtts](https://pypi.org/project/gTTS/) (Google Text-to-Speech API wrapper)
- [twitchio](https://github.com/TwitchIO/TwitchIO) (Twitch API wrapper)
- [python-dotenv](https://pypi.org/project/python-dotenv/) (Reads the key-value pair from a .env file)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
