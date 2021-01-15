import discord
import time
from discord.ext import commands
from discord.utils import get
import asyncio
import random
import json
import os
import datetime
import aiohttp
import time
import math
import praw

PREFIX = (';')
bot = commands.Bot(command_prefix=PREFIX, description='no')
@bot.remove_command('help')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=';help | xeam.nl'))
    
    
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return
    if message.author == bot.user:
        return
    if message.author.bot: return
    if 'discord.gg' in message.content:
        await message.delete()
        em = discord.Embed(title='Invite removed', description='Your invite was removed, self promotion is currently not allowed here.', color=discord.Color.red())
        await message.channel.send(embed=em)
    
@bot.command()
async def help(ctx):
    em = discord.Embed(title='Hello', description='Hello I am personal assistant! The bot for the Xeam community!', color=discord.Color.red())
    em.add_field(name='Website', value='[https://xeam.nl/](https://xeam.nl/)', inline=False)
    em.add_field(name='Minecraft Server IP', value='xeam.nl', inline=False)
    em.add_field(name='Support', value='[Ban appeal](https://xeam.nl/unban), [Support ticket](https://xeam.nl/help)', inline=False)
    em.set_footer(text='Made my Jake.#8428 - https://jakesystems.us')
    await ctx.send(embed=em)
    
@bot.command()
@commands.has_permissions(manage_messages = True)
async def poll(ctx, *, arg=None):
    channel = bot.get_channel(577569252614209547)
    if arg == None:
        await ctx.send('Error: No poll argument found, please do this: `;poll whatever you want the poll to be about`')
    else:
        em = discord.Embed(title='Poll', description=arg, color=discord.Color.red())
        em.set_footer(text=f'Poll from {ctx.author.name}- Poll system created by Jake.#8428')
        msg = await channel.send(embed=em)
        await msg.add_reaction('\U00002705')
        await msg.add_reaction('\u274E')
@poll.error
async def poll_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title='Error', description='You need `manage messages` to use this command', color=discord.Color.red())
        await ctx.send(embed=em)
        
@bot.command()
async def server(ctx):
    findbots = sum(1 for member in ctx.guild.members if member.bot)
    em = discord.Embed(title=f'About {ctx.guild.name}', color=discord.Color.red())
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.add_field(name='Member Count', value=ctx.guild.member_count)
    em.add_field(name='Server ID', value=ctx.guild.id)
    em.add_field(name='Created at', value=str(ctx.guild.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC")))
    em.add_field(name='Verification level', value=str(ctx.guild.verification_level))
    em.add_field(name='Bots', value=findbots)
    await ctx.send(embed=em)
    
@bot.command()
async def user(ctx, member:discord.Member = None):
    if not member:
        member = ctx.message.author
    roles = [role for role in member.roles]
    whoisb = discord.Embed(title=f'Who is {member}', timestamp = ctx.message.created_at, color=member.color)
    whoisb.set_thumbnail(url=member.avatar_url)
    whoisb.set_footer(text='Requested by ' + str(ctx.message.author))
    whoisb.add_field(name='Created account on', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    whoisb.add_field(name='Display name', value=member.display_name)
    whoisb.add_field(name='UID', value=member.id)
    whoisb.add_field(name='Joined server @', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    whoisb.add_field(name='Roles', value=''.join([role.mention for role in roles]))
    whoisb.add_field(name='Top role', value=member.top_role.mention)
    await ctx.send(embed=whoisb)
    
bot.run('TOKEN HERE')
