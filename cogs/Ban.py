import discord
from discord.ext import commands

class Ban(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role("ShowMan","Admin")
    async def kick(self,ctx,member:discord.Member, * ,reason=None):
        """Кикнуть !kick @name причина """
        await member.kick(reason=reason)#Причина 
        await ctx.send(f'{member.mention} - кикнут')

    @commands.command()
    @commands.has_any_role("ShowMan","Admin")
    async def ban(self,ctx,member:discord.Member, * ,reason=None):
        """Отправить в бан !ban @name причина """
        await member.ban(reason=reason)#Причина 
        await ctx.send(f'{member.mention} - Забанен')


    #Разбан пользователя @Имя   
    @commands.command()
    @commands.has_any_role("ShowMan","Admin")
    async def unban(self,ctx, *, member ):
        """Разбанить !unban имя#число"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user= ban_entry.user

            if (user.name, user.discriminator)==(member_name,member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return


    #Узнать бан лист
    @commands.command()
    @commands.has_any_role("ShowMan","Admin")
    async def showbanlist(self,ctx):
        """Показать список забаненных"""
        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:
            user=ban_entry.user
            await ctx.send(f'На этом сервере забанен {user.name}#{user.discriminator}')


def setup(bot):
    bot.add_cog(Ban(bot))