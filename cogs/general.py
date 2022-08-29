import discord
import asyncio
from discord.ext.commands import Cog, has_permissions, has_role
from discord.commands import slash_command, Option
from discord.ui import Button, Select, View
from discord.utils import get

from etc.config import BotColor, BotVer
from etc.session_option import PROFESSOR_ROLE, SUBJECT, PROFESSOR_INTRODUCTION, update_log_channel

import itertools

class General(Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @slash_command(name='학번')
    async def my_id(self, ctx):
        """자신의 학번(디스코드 id)를 알려줍니다."""

        my_id_embed = discord.Embed(title='학번', description=f'{ctx.author.mention}님의 학번은 **{ctx.author.id}**입니다.', color=BotColor)
        my_id_embed.set_footer(text=BotVer)
        
        await ctx.respond(embed=my_id_embed)
        
    @slash_command(name='교수소개')
    async def introduce(self, ctx, subject: Option(str, '과목', choices=PROFESSOR_ROLE, required=False, default=None)):
        """과목별 교수님의 한 줄 소개를 보여줍니다."""
        
        professor = get(ctx.guild.roles, name='교수님' if subject == None else subject).members
        
        introduce_embed = discord.Embed(title='교수 소개', description=f'{"모든 교수님" if subject == None else subject}들의 한 줄 소개입니다.', color=BotColor)
        for member in professor:
            introduce_embed.add_field(name=member.name, value=PROFESSOR_INTRODUCTION[member.id], inline=False)
        introduce_embed.set_footer(text=BotVer)
        
        await ctx.respond(embed=introduce_embed)
        
    @slash_command(name='수강신청')
    async def register(self, ctx, subject: Option(str, '과목', choices=SUBJECT, required=True)):
        """수강신청을 도와줍니다."""
        
        if ctx.channel.name == '🃏수강신청':
            student_role = get(ctx.guild.roles, name='수강자')
            subject_role = get(ctx.guild.roles, name=f'{subject} 수강자')
            
            await ctx.author.add_roles(student_role, subject_role)
            await ctx.respond(f'{subject} 과목 강의를 신청하였습니다.')
            
            await update_log_channel(ctx, '수강자')
            
        else:
            await ctx.delete()
            
    @slash_command(name='테스트')
    async def test(self, ctx):
        """테스트입니다."""
        
        messages = [message async for message in ctx.channel.history()]
        for i in messages:
            await i.edit(embed=discord.Embed(title='asdf'))
                
        await ctx.delete()
        
def setup(bot):
    bot.add_cog(General(bot))