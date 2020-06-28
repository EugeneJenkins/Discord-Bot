import discord
from discord.ext import commands
from discord import utils
from discord.utils import get
import os
import youtube_dl

TOKEN='NzE3MDU4NjM2OTI4Nzc4MjQw.XtUzHQ.H5vQenAfr59ekCvuwl6zhkhOg8w'
bot = commands.Bot(command_prefix='!')


POST_ID=0

ROLES={
    '': 717080153208913971, #ShowMane role
    '': 717080467865731233, #Player
    '': 717080976991453314, #Viewer
}

EXCROLES=()

MAX_ROLES_PER_USER=2