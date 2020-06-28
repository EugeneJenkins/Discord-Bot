import discord
from discord.ext import commands

class Role(commands.Cog):

    # self.playerCount=0
    def __init__(self,bot):
        self.bot = bot
        self.playerCount=0
         #Иницализая кол-во играков 
    #автоматическая выдача игракам роль 

    @commands.Cog.listener()
    async def on_member_join(self,member):
        role = discord.utils.get(member.guild.roles, name="Viewer")
        await member.add_roles(role)

    @commands.command()
    async def showman(self,member):
        """
        Получить роль ведущего / Удалить роль
        """
        user = member.message.author
        role = discord.utils.get(member.guild.roles, name="ShowMan")

        #Если у этого пользователя уже есть эта роль, удаляем
        if self.checkRole(user.roles,'ShowMan'):
            await user.remove_roles(role)
            await member.send(f"{user.name}, вы больше не ведущий")
            return 0

        await user.add_roles(role)
        await member.send(f"{user.name}, теперь вы ведущий")

    def checkRole(self,role,find):

        for name in role:
            if find==name.name:
                print(find)
                return 1
        return 0

    @commands.command()
    async def player(self,member):
        """
        Получить роль игрока / Удалить роль
        """
        user = member.message.author
        role = discord.utils.get(member.guild.roles, name="Player")
        userName = member.message.author.name

        if self.checkRole(user.roles,'Player'):
            self.playerCount=self.playerCount-1
            await member.message.author.edit(nick=userName)
            await user.remove_roles(role)
            await member.send(f"{user.name}, вы больше не игрок")
            return


        self.playerCount = self.playerCount+1  #Увеличиваем кол-во играков 
        print( self.playerCount)
        await member.message.author.edit(nick=f"{self.playerCount} | "+userName)
        await user.add_roles(role)
        await member.send(f"{user.name}, теперь вы игрок")


    # @commands.command(pass_context=True)
    # async def mute(self,ctx,mention:discord.Member):
    #     role = discord.Member.roles
    #     await mention.edit(mute=1,deafen=1)

    # @commands.command(pass_context=True)
    # async def msg(self,ctx,mention:discord.Member,text):
    #     await mention.send(text)


    # @commands.command(pass_context=True)
    # async def chnick(self,ctx, nick):
    #     await ctx.message.author.edit(nick=nick)


def setup(bot):
    bot.add_cog(Role(bot))