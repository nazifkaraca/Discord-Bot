<h1 align="center">Discord-Bot</h1> 

<div align="center">
  <img src="https://github.com/user-attachments/assets/98baefec-9253-41b2-bcff-3dfddd945e51" 
       height="350px" 
       width="550px" 
       style="border-radius: 50%; max-width: 50%;">
</div>


A simple, customizable Discord bot built using Python, designed to automate moderation tasks and add fun features to your server. This project is beginner-friendly and is a great starting point for anyone interested in learning how to integrate with the Discord API and hosting in AWS for free.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Commands](#example-commands)
- [Contributing](#contributing)

## Features

- **Automated Moderation**: Mute, kick, or ban users based on server rules.
- **Custom Commands**: Add personalized commands for users to interact with.
- **Fun Commands**: Enhance engagement with commands like jokes, memes, and trivia.
- **Welcome Messages**: Automatically greet new members with customizable messages.
- **Easy Setup**: Simple configuration via environment variables and a few customizable settings.
  
## Installation

### Prerequisites

To run the bot, you'll need the following:

- [Python 3.8+](https://www.python.org/)
- [Discord Developer Portal Account](https://discord.com/developers/applications)

### Step-by-Step Guide

1. Clone the repository:
    ```bash
    git clone https://github.com/<your-username>/discord-bot.git
    cd discord-bot
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables (e.g., using `.env`):
    ```env
    DISCORD_TOKEN = <your-bot-token>
    GUILD_ID = <your-channel-id>
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

### Dependencies

- [discord.py](https://discordpy.readthedocs.io/en/stable/): Used for interacting with the Discord API.
- Other dependencies can be found in the `requirements.txt` file.

## Configuration

The bot is configured using environment variables. Make sure to add a `.env` file or set the following in your environment:

```env
DISCORD_TOKEN = <Your Discord Bot Token>
GUILD_ID = <Channel ID>
```

## Usage

Once the bot is running, you can invite it to your Discord server using the following OAuth2 link:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications), select your application, and navigate to the OAuth2 tab.
2. Under "OAuth2 URL Generator," select the `bot` scope and appropriate permissions.
3. Copy the generated URL and use it to invite the bot to your server.

## Example Commands

Here are some example commands the bot supports:

- `/gel`: Joins the voice channel.
- `/git`: Leaves the voice channel.
- `/oynat`: Play a requested song
- `/liste`: Shows playlist.
- `/geç`: Skips next song if exists.

## Contributing

Contributions are welcome! If you would like to contribute:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add some feature"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch-name
    ```
5. Open a pull request.

Please open an issue or submit a pull request if you have ideas for improvements or new features.

