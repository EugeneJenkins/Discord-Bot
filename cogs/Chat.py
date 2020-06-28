import discord
from discord.ext import commands

handle = open("badwords.txt", "r",encoding='utf8')
ban_msg = handle.read()
handle.close()

class Chat(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('Pornhub.com'))
        print("Bot is Online.")

    @commands.Cog.listener()
    async def on_message(self,msg):
        if msg.content.lower() in ban_msg:
            await msg.delete()

   
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error,commands.CommandNotFound):
            await ctx.send('Такой команды не существует')
        # if isinstance(error, commands.MissingRequiredArgument):
        #         await ctx.send("Вы забыли ввести данные, попробуйте еще раз")
        # if isinstance(error, commands.MissingPermissions):
        #         await ctx.send(f"{ctx.author.name}, у вас нет прав на эту команду")


    # @commands.command(pass_context=True)
    # async def join(self,ctx):
    #     channel = ctx.message.author.voice.voice_channel
    #     await self.bot.join_voice_channel(channel)
    
    # @commands.command()
    # async def leave(self,ctx):
    #     server = ctx.message.server
    #     voice_client = self.bot.voice_client_in(server)
    #     await voice_client.disconnect()
    
    #comands
    @commands.command()
    async def ping(self,ctx):
        """Показать Пинг"""
        await ctx.send(f'Ping - {round(self.bot.latency * 1000)}ms')

    @commands.command()
    # @commands.has_permissions(manage_messages=True)
    async def clear(self,ctx,amount:int):
        """Очистить чат !clear кол-во сообщений"""
        await ctx.channel.purge(limit=amount+1)

    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send('Пожалуйста введите количество сообщений для удаления')

def setup(bot):
    bot.add_cog(Chat(bot))