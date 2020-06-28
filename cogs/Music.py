import discord
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get
from yandex_music import Client

class Music(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.que = []


    @commands.command(pass_context=True)
    async def join(self,ctx):
        """
        Подключение к голосовому каналу
        """
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice is not None:
            return await voice.move_to(channel)
        else:
            await channel.connect()
            await ctx.send("Бот подключился")

    @commands.command(pass_context=True)
    async def leave(self,ctx):
        """
        Отключение от голосового канала 
        """
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Бот отключился от канала {channel}")
            await ctx.send("Бот отключился")
        else:
            print("Бот не в голосе")
            await ctx.send("Ты че додик? Я даже не в голосе!")
            

    @commands.command(pass_context=True)
    async def play(self,ctx, *, args):
        """
        Воспроизведение песни !play youtube-url
        """
        def check_queue():
            global args
            args = self.que.pop(0)
            if args.startswith('https://www.youtube.com/'):
                song_there = os.path.isfile('song.mp3')
                try:
                    if song_there:
                        os.remove('song.mp3')
                        print('[log] Старый файл удален')
                except PermissionError:
                    print('[log] Не удалось удалить файл')
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print('[log] Загружаю музыку...')
                    ydl.download([args])
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        print(f'[log] Переименовываю файл: {file}')
                        os.rename(file, 'song.mp3')
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='song.mp3'),
                        after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.10
            else:
                song_there = os.path.isfile('song.mp3')
                try:
                    if song_there:
                        os.remove('song.mp3')
                        print('[log] Старый файл удален')
                except PermissionError:
                    print('[log] Не удалось удалить файл')
                res = client.search(args).best.result
                track_id = res.id
                track = client.tracks([track_id])[0]
                print('[log] Загружаю музыку...')
                track.download(filename='song.mp3', codec='mp3', bitrate_in_kbps=192)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='song.mp3'),
                        after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.10
            return

        if args.startswith('https://www.youtube.com/'):
            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
            ydl.add_default_info_extractors()
            result = ydl.extract_info(args, download=False)
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
                for format in video['formats']:
                    if format['ext'] == 'm4a':
                        audio_url = format['url']
                        print(audio_url)
                voice = get(self.bot.voice_clients, guild=ctx.guild)
                voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=audio_url), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.10
        else:
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
                    print('[log] Старый файл удален')
            except PermissionError:
                print('[log] Не удалось удалить файл')
            res = client.search(args).best.result
            track_id = res.id
            track = client.tracks([track_id])[0]
            print('[log] Загружаю музыку...')
            track.download(filename='song.mp3', codec='mp3', bitrate_in_kbps=192)
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source='song.mp3'),
                    after=lambda e: check_queue())
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.10


    @commands.command(pass_context=True)
    async def queue(self,ctx, *, args):
        """
        Добавить музыку в очередь !queue url
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            self.que.append(args)
            await ctx.send('Песня добавлена в очередь')
            print(self.que)
        else:
            pass


    @commands.command(pass_context=True)
    async def pause(self,ctx):
        """
        Поставить музыку на паузу 
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Музыка на паузе")
            voice.pause()
            await ctx.send("Музыка на паузе")
        else:
            print("Ты че епта я даже не играю музыку")
            await ctx.send("Ты че епта я даже не играю музыку")


    @commands.command(pass_context=True)
    async def resume(self,ctx):
        """
        Возобновление музыки
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            print("Музыка возобновлена")
            voice.resume()
            await ctx.send("Продолжаем петь")
        else:
            print("музыка не на паузе")
            await ctx.send("музыка не на паузе")


    @commands.command(pass_context=True)
    async def stop(self,ctx):
        """
        Остановить музыку 
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Музыка остановлена")
            voice.stop()
            await ctx.send("Музыка остановлена")
        else:
            print("нет играющей музыки")
            await ctx.send("нет играющей музыки")


    @commands.command(pass_context=True)
    async def volume(self,ctx, volume: int):
        """
        Установки громкости звука в процентах(1 - 100)
        """
        if ctx.voice_client is None:
            return await ctx.send("Я не подключен к голосу")
        print(volume/100)
        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Громкость изменена на {volume}%")


    @commands.command(pass_context=True)
    async def next(self,ctx):
        """
        Воспроизведение Следующей Песни
        """
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print("Воспроизведение Следующей Песни")
            voice.stop()
            await ctx.send("Следующая песня")
        else:
            print("Не удалось воспроизвести музыку")
            await ctx.send("Не удалось воспроизвести музыку")       

def setup(bot):
    bot.add_cog(Music(bot))