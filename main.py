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
from fries_summon import FriesSummoner


token = btl.get_token()
activity = discord.Activity(name='帥氣的威廷', type=discord.ActivityType.watching)
bot = commands.Bot(command_prefix='!', help_command=None, activity=activity)

# Modules

tc = TwscCalendar()
rt = ResponseTemplate()
bu = btl.BotUtils()
fm = FortuneMeow()
tm = TarotMeow()
fs = FriesSummoner()

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
    try:
        msg = rt.get_response('hello', ctx.author.nick or ctx.author.name)
    except:
        msg = rt.get_response('hello', ctx.author.name)
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
    args = list(args)
    try:
        n = int(args[0])
        has_num = True
    except:
        n = 1
        has_num = False

    is_detail = True if 'detail' in args else False
    if is_detail: args.remove('detail')

    if len(args) > 0:
        idx = 1 if has_num else 0
        wish = ' '.join(args[idx:])
        wish = btl.exchange_name(wish)
        msg = '%s 讓本喵來占卜看看 %s ლ(́◕◞౪◟◕‵ლ)' % (btl.mk_mention(ctx), wish)
        await ctx.send(msg)

    for msg, path in tm.get_many_tarot(int(n)):
        await ctx.send(msg, file=discord.File(path))

@bot.command(name='召喚薯條', aliases=['召喚貓貓', '召喚喵喵'])
async def summon(ctx, n=1):
    n = int(n)
    if n > 10: 
        n = 10
        await ctx.send('%s 不可以一次召喚太多啊啊啊會壞掉啊啊啊啊啊' % btl.mk_mention(ctx))
    else:
        await ctx.send('%s 熱騰騰的薯條來囉~' % btl.mk_mention(ctx))
    
    for pic in fs.get_pictures(n):
        await ctx.send(file=discord.File(pic))

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
