import logging
import random
import re

import discord
from discord.ext import commands

import bot_util as btl
from dice import Dice
from fortune import FortuneMeow
from template import ResponseTemplate
from twsc import TwscCalendar
from tarot import TarotMeow

token = open('token', 'r').readline().strip()
activity = discord.Activity(name='帥氣的威廷', type=discord.ActivityType.watching)
bot = commands.Bot(command_prefix='!', help_command=None, activity=activity)

# Modules

tc = TwscCalendar()
rt = ResponseTemplate()
bu = btl.BotUtils()
fm = FortuneMeow()
tm = TarotMeow()

# Events

@bot.event
async def on_ready():
    print("Logged in as %s" % bot.user)

# Help

@bot.command()
async def help(ctx):
    msg = rt.get_response('help')
    await ctx.send(msg)

# Feature Commands

@bot.command(aliases=['哈囉'])
async def hello(ctx):
    msg = rt.get_response('hello', ctx.author.nick or ctx.author.name)
    await ctx.send(msg)

@bot.command(name='sc', aliases=['星海比賽'])
async def fight(ctx):
    msg = rt.get_response('twsc', tc.get_recent_events())
    await ctx.send(msg)

@bot.command()
async def dice(ctx, dice='', name=None):
    msg = '%s %s' % (btl.mk_mention(ctx), Dice.roller(dice, name))
    await ctx.send(msg)

@bot.command(name='薯條籤筒', aliases=['貓貓籤筒', '喵喵籤筒'])
async def fortune(ctx):
    msg = rt.get_response('fortune', btl.mk_mention(ctx), fm.get_fortune())
    await ctx.send(msg)

@bot.command(name='薯條塔羅', aliases=['貓貓塔羅', '喵喵塔羅'])
async def tarot(ctx, *args):
    try:
        n = int(args[0])
    except:
        n = 1
    for msg, path in tm.get_many_tarot(int(n)):
        await ctx.send(msg, file=discord.File(path))

# Dev Commands

@bot.command()
async def reset(ctx):
    await ctx.send('Wait...')
    await bot.close()

@bot.command()
async def bye(ctx, code=0):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return
    with open('tmp', 'w', encoding='UTF-8') as fout:
        fout.write(str(code))
    await ctx.send('Bye!')
    await bot.close()

bot.run(token)
