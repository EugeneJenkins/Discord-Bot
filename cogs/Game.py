import discord
import random
from discord.ext import commands
import time

class Game(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.mafiaCount=0
        self.donCount=0
        self.redCount=0
        self.doctorCount=0
        self.sheriffCount=0
        self.game_role=[]
        self.role_player=[]
        self.killed=["1"]


    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def characters(self,ctx,mafia,don,sheriff,red,doctor):
        """
        Установка кол-ва перс.: Мафии, дона, комиссара, красных, доктора
        """
        self.mafiaCount=int(mafia)
        self.donCount=int(don)
        self.sheriffCount=int(sheriff)
        self.redCount=int(red)
        self.doctorCount=int(doctor)

        await ctx.send(f"**В игре будет**")
        time.sleep(1)

        if self.mafiaCount==1:
            await ctx.send(f"{self.mafiaCount} мафия")
        elif self.mafiaCount==2 or self.mafiaCount==3 or self.mafiaCount==4:
            await ctx.send(f"{self.mafiaCount} мафии")
        else: await ctx.send(f"{self.mafiaCount} мафий")

        time.sleep(1)

        if self.donCount==1:
            await ctx.send(f"{self.donCount} дон")
        elif self.donCount==2 or self.donCount==3 or self.donCount==4:
            await ctx.send(f"{self.donCount} дона")
        else: await ctx.send(f"{self.donCount} донов")

        time.sleep(1)

        if self.sheriffCount==1:
            await ctx.send(f"{self.sheriffCount} шериф")
        elif self.sheriffCount==2 or self.sheriffCount==3 or self.sheriffCount==4:
            await ctx.send(f"{self.sheriffCount} шерифа")
        else: await ctx.send(f"{self.sheriffCount} шерифов")

        time.sleep(1)

        if self.redCount==1:
            await ctx.send(f"{self.redCount} красный") 
        else: await ctx.send(f"{self.redCount} красных")
        
        time.sleep(1)

        if self.doctorCount==1:
            await ctx.send(f"{self.doctorCount} доктор")
        elif self.doctorCount==2 or self.doctorCount==3 or self.doctorCount==4:
            await ctx.send(f"{self.doctorCount} доктора")
        else: await ctx.send(f"{self.doctorCount} докторов")


    #Убиваем игрока
    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def kill(self,ctx,mention:discord.Member):
        """
        Убить игрока (Выкл микро)
        """
        await mention.edit(mute=1)
        self.killed.append(mention.id)
        await ctx.send(f"{mention.name} убит")


        #Рандом ролей
    def random_game_role(self):
        if self.mafiaCount!=0:
            for i in range(0,self.mafiaCount):
                self.game_role.append("Мафия")
        
        if self.donCount!=0:
            for i in range(0,self.donCount):
                self.game_role.append("Дон")

        if self.sheriffCount!=0:
            for i in range(0,self.sheriffCount):
                self.game_role.append("Шериф")

        if self.redCount!=0:
            for i in range(0,self.redCount):
                self.game_role.append("Красный")

        if self.doctorCount!=0:
            for i in range(0,self.doctorCount):
                self.game_role.append("Доктор")

    

    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def night(self,ctx):
        """
        Выключение всем игрокам микрофон
        """
        for player in self.role_player:
            test=ctx.guild.get_member(player)
            await test.edit(mute=1,deafen=0)
        await ctx.send("В игре наступила ночь.")
        # print(self.role_player)


    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def day(self,ctx):
        """
        Включаем всем игрокам микрофон(кроме мертвых) 
        """
        for player in self.role_player:
            test=ctx.guild.get_member(player)
            for killed in self.killed:
                if player==killed:
                    await test.edit(mute=1)
                else: await test.edit(mute=0)
        await ctx.send("В игре наступило утро")
    

    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def unmute(self,ctx):
        """
        Включаем всем игрокам микрофон
        """
        for player in self.role_player:
            test=ctx.guild.get_member(player)
            await test.edit(mute=0)
        await ctx.send("Все игроки воскрешены.")

    @commands.command(pass_context=True)
    @commands.has_any_role("ShowMan","Admin")
    async def start(self,ctx):
        """
        Включение всем игрокам микрофон
        """
        random.shuffle(self.game_role)
        game=self.game_role
        print(game)


        users=[]
        self.role_player=[] #Массив пользоватлей с ролью "Игрок"
        get_users=ctx.guild.members

        #Находим всем пользователей сервера 
        for id in get_users:
            users.append(id.id)

        #Находим пользователей с ролью "Player"
        for players in users:
            info=ctx.guild.get_member(players)
            for name in info.roles:
                if name.name=="Player":
                    self.role_player.append(players)
        
        #Получаем игровые роли
        if len(self.game_role)==0:
            self.random_game_role()
        else:
            self.game_role=[]
            self.random_game_role()

        #В списке играков выдаем игравую роль 
        i=0
        for player in self.role_player:
            test=ctx.guild.get_member(player)
            await test.send(f"Ваша роль -> {game[i]}")
            i=i+1

        await ctx.send("Все игроки получили свои роли.")

    @characters.error
    async def characters_error(self,ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send('Ошибка: введите кол-во всех игровых ролей.')

    @kill.error
    async def kill_error(self,ctx, error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send('Ошибка: выберите кого убить.')

        if isinstance(error,commands.MissingAnyRole):
            await ctx.send('У вас нет прав на эту команду.')
            

            

def setup(bot):
    bot.add_cog(Game(bot))