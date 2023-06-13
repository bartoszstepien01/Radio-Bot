import os
import discord
import wavelink
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import radio

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(client)
wavelink_client = wavelink.Client(bot=client)

async def start_nodes():
    await client.wait_until_ready()

    await wavelink_client.initiate_node(
        host=os.getenv("LAVALINK_HOST"), 
        port=int(os.getenv("LAVALINK_PORT")), 
        rest_uri=os.getenv("LAVALINK_URI"), 
        password=os.getenv("LAVALINK_PASSWORD"), 
        identifier=os.getenv("LAVALINK_IDENTIFIER"), 
        region='europe')

client.loop.create_task(start_nodes())

@slash.slash(name="join", description="Joins the current voice channel")
async def join(ctx):
    voice = ctx.author.voice
    if not voice:
        await ctx.send("This command only works when you're in a voice channel.")
        return
        
    channel = voice.channel

    player = wavelink_client.get_player(ctx.guild_id)
    await player.connect(channel.id)
    await ctx.send("Joined the voice channel!")

@slash.slash(name="leave", description="Leaves the current voice channel")
async def leave(ctx):
    player = wavelink_client.get_player(ctx.guild_id)
    if not player.is_connected:
        await ctx.send("This command only works when the bot has joined a voice channel.")
        return

    await player.disconnect()

    await ctx.send("Left the voice channel!")

@slash.slash(name="play", description="Plays the given radio station", options=[create_option(name="radio_station", description="Name of the radio station", option_type=3, required=True)])
async def play(ctx, radio_station):
    player = wavelink_client.get_player(ctx.guild_id)
    if not player.is_connected:
        await ctx.send("This commands only works when the bot has joined a voice channel.")
        return

    await ctx.defer()

    station = radio.search(radio_station)
    if not station:
        await ctx.send("Radio station not found.")
        return

    streams = radio.streams(station["id"])

    if player.is_playing: await player.stop()
    tracks = await wavelink_client.get_tracks(streams[0])
    await player.play(tracks[0])

    await ctx.send("Radio's playing!")

@slash.slash(name="stop", description="Stops the currently playing radio station")
async def stop(ctx):
    player = wavelink_client.get_player(ctx.guild_id)
    if not player.is_playing: 
        await ctx.send("This command only works when the radio is playing.")
        return

    await player.stop()

    await ctx.send("Radio stopped!")

@slash.slash(name="pause", description="Pauses the currently playing radio station")
async def pause(ctx):
    player = wavelink_client.get_player(ctx.guild_id)
    if not player.is_playing:
        await ctx.send("This command only works when the radio is playing.")
        return

    await player.set_pause(True)

    await ctx.send("Radio paused!")

@slash.slash(name="resume", description="Resumes the paused radio station")
async def resume(ctx):
    player = wavelink_client.get_player(ctx.guild_id)
    if not player.is_paused: 
        await ctx.send("This commands only works when the radio is paused.")
        return

    await player.set_pause(False)

    await ctx.send("Radio resumed!")

@slash.slash(name="about", description="Shows info about the bot")
async def about(ctx):
    await ctx.send("Radio Bot by Bartosz Stępień")

client.run(
    os.getenv("DISCORD_TOKEN")
)