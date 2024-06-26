# +----------------------------------+ MODULES +----------------------------------+

import discord
import datetime
from pathlib import Path
import os
import logging
import openai
import requests


from datetime import datetime
from dotenv import load_dotenv
from discord import Member
from discord import File
from discord import app_commands
from discord.ext import commands
from pyowm import OWM
from bs4 import BeautifulSoup

# +----------------------------------+ SETTINGS +----------------------------------+

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all(), case_insensitive=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    filename="log.txt"
)

cwd = Path(__file__).parents[0]
cwd = str(cwd)
time_now = datetime.now()

load_dotenv()

bot.config_token = os.getenv('TOKEN')
owm_key = os.getenv('OWM_KEY')
openai_key = os.getenv('OPENAI_KEY')
vers_id = os.getenv('ID')
version = os.getenv('VERSION')

bot.remove_command('help')
bot.remove_command('weather')
bot.remove_command('timer')

owm = OWM(owm_key)
mgr = owm.weather_manager()

# +------------------------------------+ STATUS +----------------------------------+

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    os.system("clear")
    stats = f"""
        •—————————————————————————————————————•
           Bot Name: {bot.user.name}
           Bot Path: {cwd}
           Ping (ms): {bot.latency}
           Version ID: {vers_id}
           Commands: {len(synced)}
           Bot by sud3v_1s_h3r3
        •—————————————————————————————————————•
    """
    print(stats)
    await bot.change_presence(activity=discord.Game(name=f"{version} | /help \n https://theprometey.xyz/discord-bot"))

# +------------------------------------+ STATUS +----------------------------------+

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission to use this command!**')
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send(' :no_entry_sign:  `|`  **Sorry you dont have permission for a bot!**')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(' :name_badge:  `|`  **This member does not exist.**')

# +------------------------------------+ COMMANDS +----------------------------------+

@bot.tree.command(name='github', description='Get the latest GitHub news')
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Retrieving the latest GitHub news...", colour=discord.Colour.from_rgb(0, 61, 125)))
    response = requests.get('https://github.com/about/press?page=1')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h2.f3-mktg.text-normal')
    news_articles = [p.get_text().replace("â\x80\x99s", "'").replace("â", " ") for p in news_articles if p.get_text() != 'Sorry']    
    news_articles_md = '\n'.join([f'- {article}' for article in news_articles])
    news_articles = news_articles[:15]
    if news_articles_md:
        embed = discord.Embed(title="Here are the latest GitHub news headlines:",description=f"{news_articles_md}", colour=discord.Colour.from_rgb(0, 61, 125))
        embed.set_thumbnail(
			url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/2048px-Octicons-mark-github.svg.png"
			)
        embed.set_footer(
			text="GitHub News: https://github.com/about/press",
			icon_url="https://avatars.githubusercontent.com/u/109563195?s=400&u=51dcd9720783d251feccdb16a451813b04e30597&v=4"
		)
        embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/github.jpg?raw=true')
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Sorry, there was an error retrieving the latest GitHub news. Please try again later.')

@bot.tree.command(name='appledev', description='Get the latest Apple Developer news')
async def appledev(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="Retrieving the latest Apple Developer news...", colour=discord.Colour.from_rgb(0, 61, 125)))
    response = requests.get('https://developer.apple.com/news/')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h2')
    response = requests.get('https://developer.apple.com/news/')
    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.select('h2')
    news_articles = [p.get_text().replace("â\x80\x99s", "'").replace("â", " ") for p in news_articles if p.get_text() != 'News and Updates'][:15][1:]
    news_articles_md = '\n'.join([f'- {article}' for article in news_articles])
    if news_articles_md:
        embed = discord.Embed(title="Here are the latest Apple Developer news headlines:",description=f"{news_articles_md}", colour=discord.Colour.from_rgb(0, 61, 125))
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_first_logo.png")
        embed.set_footer(
			text="Apple Developer News: https://developer.apple.com/news/",
			icon_url="https://avatars.githubusercontent.com/u/109563195?s=400&u=51dcd9720783d251feccdb16a451813b04e30597&v=4"
		)
        embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/appledev.jpg?raw=true')
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send('Sorry, there was an error retrieving the latest Apple Developer news. Please try again later.')
	
@bot.tree.command(name="weather", description='Get weather news')
@app_commands.describe(city_name = "Enter City Name")
async def weather(interaction: discord.Integration, city_name: str):
    observation = mgr.weather_at_place(city_name)
    w = observation.weather
    embed = discord.Embed(title=f'Weather in {city_name}:', colour=discord.Colour.from_rgb(0, 61, 125))
    embed.add_field(name='Show Status:', value=w.detailed_status)
    embed.add_field(name='Wind Degree:', value=w.wind()['deg'])
    embed.add_field(name='Wind Speed:', value=w.wind()['speed'])
    embed.add_field(name='Teperature:', value=w.temperature('celsius')['temp'])
    embed.add_field(name='Max Teperature:', value=w.temperature('celsius')['temp_max'])
    embed.add_field(name='Min Teperature:', value=w.temperature('celsius')['temp_min'])
    embed.add_field(name='Feels Like:', value=w.temperature('celsius')['feels_like'])
    embed.add_field(name='Cloud Percent:', value=w.clouds)
    embed.add_field(name='Humidity:', value=w.humidity)
    embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/weather.jpg?raw=true')
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="botvers", description='Get Bot Version')
async def botvers(interaction: discord.Integration):
    embed = discord.Embed(title=f'Bot Version: {version}', colour=discord.Colour.from_rgb(0, 61, 125))
    embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/botvers.jpg?raw=true')
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description='Get Help Menu')
async def help(interaction: discord.Integration):
    embed = discord.Embed(title=f'Help Book', colour=discord.Colour.from_rgb(0, 61, 125))
    embed.add_field(name=f'/about', value='📓 Information')
    embed.add_field(name=f'/updates', value='📓 Information')
    embed.add_field(name=f'/botvers', value='📓 Information')
    embed.add_field(name=f'/weather', value='✌️ For Users')
    embed.add_field(name=f'/appledev', value='✌️ For Users')
    embed.add_field(name=f'/github', value='✌️ For Users')
    embed.add_field(name=f'/bug (your error)', value='🛠️ Developers Support')
    embed.add_field(name=f'/idea (your idea)', value='🛠️ Developers Support')
    embed.add_field(name=f'/feedback (your feedback)', value='🛠️ Developers Support')
    embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/botbanner.jpg?raw=true')
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bug", description='Send Bot Bug to developers')
@app_commands.describe(message = "Enter Your Error Message")
async def bug(interaction: discord.Integration, message: str):
    if message != '':
        await interaction.response.send_message("Sended!")
        chan = bot.get_channel(1247948661401587794)
        emb = discord.Embed(title='Found a bug in the bot!', colour=discord.Colour.from_rgb(0, 61, 125))
        emb.add_field(name='Description:', value=message)
        emb.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/bug.jpg?raw=true')
        await chan.send(embed=emb)

@bot.tree.command(name="feedback", description='Send Bot Feedback to developers')
@app_commands.describe(message = "Enter Your Feedback")
async def feedback(interaction: discord.Integration, message: str):
    if message != '':
        await interaction.response.send_message("Sended!")
        chan = bot.get_channel(1247948617101086750)
        embed = discord.Embed(title='Bot feedback!', colour=discord.Colour.from_rgb(0, 61, 125))
        embed.add_field(name='Description + rating:', value=message)
        embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/feedback.jpg?raw=true')
        await chan.send(embed=embed)

@bot.tree.command(name="idea", description='Send Bot Idea to developers')
@app_commands.describe(message = "Enter Your Idea")
async def idea(interaction: discord.Integration, message: str):
    if message is None:
        embed = discord.Embed(title="Err", description=f"Enter your idea `/idea <idea>`",color=discord.Color.red())
        embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/idea.jpg?raw=true')
        await interaction.response.send_message(embed=embed)
    else:
        channel = await bot.fetch_channel(1247948644481634336)
        embed = discord.Embed(title="New Idea!",description=f"**Content:**\n{message}", colour=discord.Colour.from_rgb(0, 61, 125))
        embed.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/idea.jpg?raw=true')
        msg = await channel.send(embed=embed)
        embed2 = discord.Embed(title="Sucs!",description=f"Idea was **successfully** submitted\n**Content:\n{message}**", colour=discord.Colour.from_rgb(0, 61, 125))
        embed2.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/idea.jpg?raw=true')
        await interaction.response.send_message(embed=embed2)

@bot.tree.command(name="about", description='Get Bot Information')
async def about(interaction: discord.Integration):
    members = len(set(bot.get_all_members()))
    emb = discord.Embed(title='Bot Information.', colour=discord.Colour.from_rgb(0, 61, 125))
    emb.add_field(name='🔗 ADD ME', value='https://theprometey.xyz/add-discord-bot')
    emb.add_field(name='🔗 WEBSITE', value='https://theprometey.xyz/discord-bot (Beta)')
    emb.add_field(name='🔗 SERVER', value='https://theprometey.xyz/discord')
    emb.add_field(name='✌ SERVERS', value=f'{len(bot.guilds)}')
    emb.add_field(name='✌ PARTICIPANS', value=f"{members}")
    emb.add_field(name='👑 CREATOR', value='sud3v_1s_h3r3')
    emb.add_field(name='🔗 GITHUB', value='https://theprometey.xyz/github')
    emb.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/botbanner.jpg?raw=true')
    await interaction.response.send_message(embed=emb)

@bot.tree.command(name="updates", description='Get Bot Updates')
async def updates(interaction: discord.Integration):
    emb = discord.Embed(title='Bot updates.', description='Here my creator writes about my updates.', colour=discord.Colour.from_rgb(0, 61, 125))
    emb.add_field(name=f'{version}', value='https://theprometey.xyz/discord-bot/updates')
    emb.set_image(url='https://github.com/suleymanovdev/prometey-discord-bot/blob/main/img/updates.jpg?raw=true')
    await interaction.response.send_message(embed=emb)

# +------------------------------------+ BOT.RUN +----------------------------------+

bot.run(bot.config_token)
