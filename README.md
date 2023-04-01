# huggy-discord-bot
![version](https://img.shields.io/github/v/tag/AuLaSW/huggy-discord-bot?color=brightgreen&label=version)
![last commit](https://img.shields.io/github/last-commit/AuLaSW/huggy-discord-bot)

*A discord bot for giving out hugs.*

This bot remembers hugs on a guild-by-guild basis, so if you have the bot connected to multiple servers (guilds), then it will tell you how many hugs you have in ther server where you called the command (Say, in server `A` you have 10 hugs and in server `B` you have 7 hugs. If you get a hug in server `A` it doesn't affect the hugs in server `B` and vice-versa. The data is guild-aware and you won't get crossover).

## Setup

### Installation

Install from this GitHub page, either through cloning the repository or downloading the latest release on the right. Then, setup the virtual environment (I used `venv` as an example folder, use whatever you want) and run it:

```console
python -m venv venv && ./venv/Scripts/activate
```

Then, install the [requirements](requirements.txt):

```console
pip install -r requirements.txt
```

### Connection to Discord

Next, set up your environment variables in a `.env` file. The program looks for `DISCORD_TOKEN` to retrieve the token for your bot. ([Here are instructions on how to get a token for your bot](https://discord.com/developers/docs/getting-started#step-1-creating-an-app)):

```env
# .env file

DISCORD_TOKEN={insert-token-here}
```

*See the [roadmap](#roadmap) for potential future environment variables.*

You will need to connect your bot to guilds (servers), which you can do with [OAuth2](https://discord.com/developers/docs/getting-started#step-1-creating-an-app), where you will select `Bot` and fill out the permissions. For this bot, you only need the following permissions:

- `Read Messages/View Channels`
- `Send Messages`
- `Slash Commands`

You will also need to make sure the following are selected underneath your bot permission gateway intents:

![image](https://user-images.githubusercontent.com/59460358/229298600-fe7f530d-0e42-47b8-83c4-9b549fed2310.png)

### Running

Now you can run the discord bot with the command:

```console
python huggy.py
```

This will connect to your server. You must have a text channel called `#bot-commands`. The bot listens for commands in this channel and responds to them here.

## Roadmap

- [ ] Add support for multiple channels in `.env` under the `CHANNELS` variable.
- [ ] Add support for guilds in `.env` under the `GUILDS` variable.
  - This would be used to limit the bot to specific guilds.
- [ ] Add support for `/restart` and `/update` admin commands.
  - Useful when pushing updates to the server and forcing it to update; or, restart if it is not working correctly.
  - `/update` would only work for the owner of the bot.
- [ ] Add better style/add embedding for returned commands.
  - Embed the hugboard to look better, at a minimum.
- [ ] Add API to call and create bot externally in other applications.
- [ ] Get `.gifs` instead of `.mp4` files to use for the hug visuals.
- [ ] Move from SQLite3 to another database solution (Postgres, potentially).

## Contributing

If you would like to contribute to this project, please fork the repository and make a pull request.

## License

This project is subject to the most restrictive license of any dependency used within it. In cases where dependency licenses allow, the project will be licensed under GPLv3.
