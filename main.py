from config import *
from discord.ext import commands







for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(TOKEN)