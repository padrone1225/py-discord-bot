# bot.py
import os
import discord
import random
from dotenv import load_dotenv

# bot
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
# this command important, becaouse these commands are manage permission for bot.
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():

    # Get guild name
    # for guild in client.guilds:
    #     if guild.name == GUILD:
    #         break

    print(
        f'{client.user} is connected to the following guild:\n'
        # f'{guild.name}(id: {guild.id})'
    )

    # Get and print members in the Discord group.
    # members = '\n -'.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

# When new member join this group, the bot send 'Welcome' dm.


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to my Discord Server!')

# When member sendet '99!', the bot responding.


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💥 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool coool, '
            'no doubt no doubt no'
        )
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

# client.run(TOKEN)

bot = commands.Bot(intents=intents, command_prefix='!')


@bot.command(name='create-channel')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='999', help='Responds with a random quote from Broonklyn 999')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    # @bot.event
    # async def on_ready():
    #     print(f'{bot.user.name} has connected to Discord')
bot.run(TOKEN)
