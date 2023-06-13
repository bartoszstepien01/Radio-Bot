
# Radio Bot

A simple Discord bot which plays radio stations on voice channels


## Commands

This bot supports Discord slash commands

|Command|Description|
|---|---|
|```/join```|Joins the current voice channel|
|```/leave```|Leaves the current voice channel|
|```/play [radio station]```|Plays the given radio station. Replace ```[radio station]``` with a name of desired radio station|
|```/stop```|Stops the currently playing radio station|
|```/pause```|Pauses the currently playing radio station|
|```/resume```|Resumes the paused radio station|
|```/about```|Shows info about the bot|

## Environment Variables

|Variable|Description|
|---|---|
|LAVALINK_HOST|Lavalink server host|
|LAVALINK_PORT|Lavalink server port|
|LAVALINK_URI|Lavalink server URI|
|LAVALINK_IDENTIFIER|Lavalink server identifier|
|LAVALINK_PASSWORD|Lavalink server password|
|DISCORD_TOKEN|Your Discord token|

## Installation

Before running this application you have to run a Lavalink server. More info [here](https://github.com/lavalink-devs/Lavalink)

```bash
git clone https://github.com/bartoszstepien01/Radio-Bot
cd Radio-Bot
pip install -r requirements.txt
python main.py
```
    
## License

[MIT](https://choosealicense.com/licenses/mit/)

