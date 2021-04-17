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
from mcstatus import MinecraftServer
import socket

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
        if message.channel.id == 814973910088155203:
            return
        elif message.channel.id != 814973910088155203:
            await message.delete()
            em = discord.Embed(title='Invite verwijderd', description='Jou invite is verwijderd, zelf promotie is niet toegestaan in dit kanaal.', color=discord.Color.red())
            await message.channel.send(embed=em)
        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.CommandNotFound):
        em = discord.Embed(title='Error: Command Not Found', description='The command you executed likely doesnt exist. You may have made a spelling error aswell, if the issue persists, contact bot staff.', color=discord.Color.red())
        await ctx.send(embed=em)
    else:
        raise error
    
@bot.command()
async def help(ctx):
    em = discord.Embed(title='Hello', description='Hello I am personal assistant! The bot for the Xeam community!', color=discord.Color.red())
    em.add_field(name='Website', value='[https://xeam.nl/](https://xeam.nl/)', inline=False)
    em.add_field(name='Minecraft Server IP', value='xeam.nl', inline=False)
    em.add_field(name='Support', value='[Ban appeal](https://xeam.nl/unban), [Support ticket](https://xeam.nl/help)', inline=False)
    em.add_field(name='Commands', value='```\nserver - show info about the server\nuser - show info about a specific user\nstatus - check the minecraft server status\n```')
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
    

#WATCHOUT this stat command is kinda bad, it works except for the server.query(), also it throws an ssl error whenever its executed but this doesnt cause stability issues or issues with the output so I dont really care to fix it.
@bot.command(aliases=['stat'])
async def status(ctx):
    async with ctx.typing():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('xeam.nl', 25565))
        if result == 0:
            server = MinecraftServer.lookup('xeam.nl')
            status = server.status()
            #query = server.query() -- this code is currently disabled as the Xeam minecraft server has protection that causes this code to timeout
            em = discord.Embed(title='Xeam minecraft server status', color=discord.Color.red(), inline=False)
            em.add_field(name='Server status', value='Server is online :green_circle:')
            em.add_field(name='Player count', value='{0} players online'.format(status.players.online), inline=False)
            #em.add_field(name='Players Online', value="{0}".format(", ".join(query.players.names)), inline=False) -- goto line 112
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title='Xeam minecraft server status', color=discord.Color.red())
            em.add_field(name='Server status', value='Server is offline :red_circle:')
            await ctx.send(embed=em)
          
          
@bot.group()
async def verify(ctx):
    member = ctx.author
    role = ctx.guild.get_role(800171403214979102)
    await ctx.author.add_roles(role)
    await ctx.message.delete()
    em = discord.Embed(title='Verificatie compleet!', description=f'Welkom {member.name}! Bedankt dat je de Bot verificatie hebt voldaan, Xeam en al haar partners wensen jou veel plezier in onze gezellige community!', color=discord.Color.red())
    await member.send(embed=em)
    print(f'{member} was verified')
    
@bot.command()
async def setup(ctx):
    em = discord.Embed(title='Verify Here', description='All users are required to verify after reading the rules, please type `;verify` after you have read the rules. Please ensure your DMs are open to this server and this bot in order to verify', color=discord.Color.red())
    await ctx.send(embed=em)
    
@bot.command()
@commands.has_permissions(manage_messages = True)
async def mute(ctx, member : discord.Member):
    role = ctx.guild.get_role(801197013378138142)
    await ctx.member.add_roles(role)
    await ctx.send(f'{member} was muted')
    

"""
@bot.command()
async def ticket(ctx, *, issue=None):
    member = ctx.author
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
    }
    
    em = discord.Embed(title='New Ticket', description='Hello! Our staff will be with you shortly. While you wait, please describe your issue further.', color=discord.Color.red())
    em.add_field(name='Issue', value=issue)
    em.set_footer(text='A staff member can close this ticket with ;solve, ;close, or ;resolve')
    
    if issue == None:
        em2 = discord.Embed(title='Ticket creation failed', description='I need a reason to create the ticket\nExample: `;ticket how to get roles`', color=discord.Color.red())
        await ctx.send(embed=em2)
        return False
    else:
        category = get(ctx.guild.category_channels, 'ticket-support')
        channel = await guild.create_text_channel(f'{member.name}-ticket', overwrites=overwrites, category=category)
        await channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    
        await channel.send(str(ctx.author.mention), embed=em)
        await ctx.send('done')
        print(f'{member} created a ticket about: {issue}')

@bot.command(aliases=['close', 'resolve'])
@commands.has_permissions(manage_channels = True)
async def solve(ctx):
    channel = ctx.message.channel
    await channel.delete()
"""
    
bot.run('TOKEN HERE')
