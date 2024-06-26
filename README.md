# Prometey Discord Bot

This README.md file provides documentation for the Prometey Discord Bot project. It includes information about the modules used, settings, status events, command events, and available commands.

## Table of Contents

- [Modules](#modules)
- [Settings](#settings)
- [Status Events](#status-events)
- [Commnand Events](#command-events)
- [Commands](#commands)

## Modules

The following modules are imported in the Prometey Discord Bot project:

* `typing.Optional`: Used for type hints.
* `discord`: Provides functionality for creating Discord bots.
* `datetime`, `asyncio`, `random`, `time`: Modules for working with dates, asynchronous programming, generating random numbers, and managing time.
* `pathlib.Path`: Allows working with file paths.
* `json`: Enables working with JSON files.
* `contextlib`, `io`, `textwrap`, `os`: Modules for various utility functions.
* `logging`: Provides logging capabilities.
* `openai`: Module for integrating with the OpenAI API.
* `requests`: Library for making HTTP requests.
* `pyowm`: Python wrapper for the OpenWeatherMap API.
* `bs4.BeautifulSoup`: Library for parsing HTML and XML documents.

## First Steps
You should use `.env` file to configure your bot data like this:

```
TOKEN="your_bot_token_here"
OWM_KEY="your_owm_api_key_here"
OPENAI_KEY="your_openai_api_key_here"
ID="1.0.0 Pre-Beta"
VERSION="Snake"
```

And after this changes yopu can easily run your bot.

## Settings

The following settings are defined in the Prometey Discord Bot project:

* `bot`: An instance of the commands.Bot class, representing the Discord bot.
* `logging.basicConfig`: Configures the logging module.
* `cwd`: The current working directory of the script.
* `time_now`: The current date and time.
* `SECRET_FILE`: A JSON file containing secret keys and tokens.
* `bot.config_token`: The token for authenticating the bot with Discord.
* `bot.remove_command`: Removes default command handlers from the bot.
* `owm_key`: The API key for accessing the OpenWeatherMap API.
* `openai_key`: The API key for accessing the OpenAI API.
* `owm`: An instance of the pyowm.OWM class for interacting with the OpenWeatherMap API.
* `mgr`: The weather manager object for the OpenWeatherMap API.
* `vers_id`: The version ID of the bot.
* `version`: The version number of the bot.

## Status Events

The following status events are defined in the Prometey Discord Bot project:

* `on_ready`: Called when the bot has successfully connected to Discord. Sets the bot's presence and prints status information.

## Command Events

The following command events are defined in the Prometey Discord Bot project:

* `on_command_error`: Called when a command encounters an error. Handles different types of errors and sends appropriate error messages.

## Commands

The Prometey Discord Bot project defines the following commands:

* `/formula1`: Retrieves the latest Formula 1 news from a website.
* `/github`: Retrieves the latest GitHub news from a website.
* `/appledev`: Retrieves the latest Apple Developer news from a website.
* `/gpt`: Allows users to ask questions to the ChatGPT model.
* `/weather`: Retrieves weather information for a specific city.
* `/botvers`: Displays the current version of the bot.
* `/help`: Displays the help menu with a list of available commands.
* `/bug`: Sends a bug report to the developers.
* `/feedback`: Sends feedback to the developers.
* `/idea`: Submits an idea to the developers.
