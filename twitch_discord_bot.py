import time

import discord
from discord import FFmpegPCMAudio,app_commands
from discord.ext import commands
import asyncio
from gtts import gTTS
from twitchio.ext import commands as commandsTwitch
import os
from dotenv import load_dotenv

load_dotenv()
import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
# Define constants
TWITCH_TOKEN = os.getenv("TWITCH_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE")
IGNORED_TWITCH_USERS = os.getenv("IGNORED_TWITCH_USERS", "").split(',')

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Set up Twitch bot
class TwitchBot(commandsTwitch.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_TOKEN, prefix='?', initial_channels=['andre_e', 'mrlopesbrazil'])

    async def event_ready(self):
        print(f'Logged in Twitch as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        print(message.content)
        await phrase_queue.put(message)
        await self.handle_commands(message)


# Initialize global variables
phrase_queue = asyncio.Queue()
bot_in_voice_channel = False
context_global = None
last_author = None
selected_twitch_channel = None


# Discord bot commands
#@bot.command(name='join')
@bot.tree.command(name='join')
async def join(interaction: discord.Interaction, twitch_channel: str):
    global bot_in_voice_channel
    global context_global
    global selected_twitch_channel

    if bot_in_voice_channel:
        await interaction.response.send_message('Bot is already in a voice channel.')
    else:
        voice_channel = interaction.user.voice.channel
        if voice_channel:
            await voice_channel.connect()
            bot_in_voice_channel = True
            selected_twitch_channel = twitch_channel
            context_global = interaction
            await interaction.response.send_message(f'Bot joined {voice_channel}.')
        else:
            await interaction.response.send_message('You must be in a voice channel to use this command.')


@bot.tree.command(name='leave')
async def leave(ctx):
    global bot_in_voice_channel

    if bot_in_voice_channel:
        for vc in bot.voice_clients:
            await vc.disconnect()
        bot_in_voice_channel = False
        await ctx.send('Bot left the voice channel.')
    else:
        await ctx.send('Bot is not in a voice channel.')


# Discord bot event
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
    except Exception as e:
        print(e)

    print(f'Logged in Discord as {bot.user.name} ({bot.user.id})')
    await start_repeat_task()


# Task to repeat phrases
async def repeat_phrases():
    while True:

        global last_author
        phrase = await phrase_queue.get()
        channel = bot.get_channel(context_global.channel.id)

        while context_global.client.voice_clients[0].is_playing():
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

        if not (phrase.author.name == selected_twitch_channel or IGNORED_TWITCH_USERS.__contains__(phrase.author.name)) and phrase.channel.name == selected_twitch_channel :

            print(f'Bot entered voice channel: {channel}')
            if last_author == phrase.author.name:
                author_said = phrase.content
            else:
                last_author = phrase.author.name
                author_said = phrase.author.name + " disse: " + phrase.content

            tts = gTTS(text=author_said, lang=VOICE_LANGUAGE)
            tts.save("output.mp3")

            if not context_global.client.voice_clients[0].is_playing():
                context_global.client.voice_clients[0].play(FFmpegPCMAudio("output.mp3"), after=lambda e: print('done', e))


async def start_repeat_task():
    await bot.wait_until_ready()
    bot.loop.create_task(repeat_phrases())


# Main function
async def main():
    twitch_bot = TwitchBot()
    twitch_task = asyncio.create_task(twitch_bot.start())
    discord_task = asyncio.create_task(bot.start(DISCORD_TOKEN))
    try:
        await asyncio.gather(twitch_task, discord_task)
    except KeyboardInterrupt:
        await bot.close()
        await twitch_bot.close()


# Run the main function if the script is executed
if __name__ == "__main__":
    asyncio.run(main())
