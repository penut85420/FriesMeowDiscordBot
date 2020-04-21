"""
Author: PenutChen
"""
import asyncio
import datetime
import logging
import random
import re

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import modules.utils as btl
from modules.dice import Dice
from modules.easy_calculator import EasyCalculator
from modules.fortune import FortuneMeow
from modules.fries_summon import FriesSummoner
from modules.sc_mutation import SC2Mutation
from modules.tarot import TarotMeow
from modules.template import ResponseTemplate
from modules.twsc import TwscCalendar
from modules.wikiman import WikiMan
from modules.sixty_jiazi import SixtyJiazi
from modules.meow_talk import MeowTalk

# Modules
bu = btl.BotUtils()
rt = ResponseTemplate()
fs = FriesSummoner()
fm = FortuneMeow()
tm = TarotMeow()
tc = TwscCalendar()
sm = SC2Mutation()
ec = EasyCalculator()
wm = WikiMan()
sj = SixtyJiazi()
mt = MeowTalk()


class FriesBot(commands.Bot):
    def __init__(self, **kwargs):
        self.msg_log = logging.getLogger('fries.meow.friesbot')
        self.ignore_channels = bu.get_ignore_channels()
        bu.start_time = datetime.datetime.now()
        commands.Bot.__init__(self, **kwargs)

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if msg.content == '!r' and msg.channel.id == bu.restart_channel:
            btl.restart_bot()
            await bot.close()
        elif msg.content == '!bye' and msg.channel.id == bu.restart_channel:
            btl.shutdown_bot()
            await bot.close()

        if msg.guild is not None:
            if msg.guild.id not in self.ignore_channels:
                if msg.content.startswith('!'):
                    self.msg_log.info(rt.get_response('msglog').format(msg))

        name_tag = f'<@!{self.user.id}>'
        if msg.guild is None and not msg.content.startswith('!') or msg.content.startswith(name_tag):
            self.msg_log.info(rt.get_response('msglog').format(msg))
            await msg.channel.send(mt.get_sent())

        await commands.Bot.on_message(self, msg)

token = bu.get_token()
activity = discord.Activity(name='奴僕清貓砂', type=discord.ActivityType.watching)
bot = FriesBot(command_prefix='!', help_command=None, activity=activity)


def log(msg):
    bot.msg_log.info(msg)

# Events


@bot.event
async def on_ready():
    log('Logged in as %s' % bot.user)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    log(str(error).replace('\n', ' | '))

# Commands


@bot.command(name='help', aliases=['喵'])
async def help(ctx):
    msg = rt.get_response('help')
    await ctx.send(msg)


@bot.command(aliases=['哈囉'])
async def hello(ctx, *args):
    try:
        msg = rt.get_response('hello', ctx.author.nick or ctx.author.name)
    except:
        msg = rt.get_response('hello', ctx.author.name)
    await ctx.send(msg)

# Fries Commands


@bot.command(name='時間', aliases=['time'])
async def time(ctx):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    await ctx.send(f'喵喵喵，現在是臺灣時間 {ts}')

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


@bot.command()
async def wiki(ctx, *args):
    msgs = wm.get_response(*args)
    for msg in msgs:
        await ctx.send(msg)


@bot.command()
async def say(ctx, *args):
    await ctx.send(mt.get_sent())

# StarCraft II Commands


@bot.command(name='sc', aliases=['星海比賽', '星海賽事'])
async def fight(ctx):
    msg = rt.get_response('twsc', tc.get_recent_events())
    await ctx.send(msg)


@bot.command(name='本週異變', aliases=['本周異變', '異變', 'mutation'])
async def mutation(ctx):
    msg = sm.get_recent_stage()
    await ctx.send(msg)


@bot.command(name='下週異變', aliases=['下周異變', 'mutationnw'])
async def mutation_next_week(ctx):
    msg = sm.get_next_week_stage()
    await ctx.send(msg)

# TRPG Commands


@bot.command()
async def dice(ctx, dice='', name=None):
    msg = '%s %s' % (btl.mk_mention(ctx), Dice.roller(dice, name))
    await ctx.send(msg)


@bot.command()
async def calc(ctx, *args):
    msg = ec.calc(' '.join(args))
    await ctx.send(msg)

# Fortune Commands


@bot.command(name='薯條籤筒', aliases=['貓貓籤筒', '喵喵籤筒', '薯條籤桶', '貓貓籤桶', '喵喵籤桶'])
async def fortune(ctx):
    msg = rt.get_response('fortune', btl.mk_mention(ctx), fm.get_fortune())
    await ctx.send(msg)

@bot.command(name='薯條甲子籤', aliases=['貓貓甲子籤', '喵喵甲子籤'])
async def sixty_jiazi(ctx):
    msg = sj.pick()
    await ctx.send(msg)

@bot.command(name='薯條塔羅', aliases=['貓貓塔羅', '喵喵塔羅'])
async def tarot(ctx, *args):
    n, has_num = btl.cast_int(args)

    if len(args) > has_num:
        wish = ' '.join(args[has_num:])
        wish = btl.exchange_name(wish)
        msg = '%s 讓本喵來占卜看看 %s ლ(́◕◞౪◟◕‵ლ)' % (btl.mk_mention(ctx), wish)
    else:
        msg = '%s 讓本喵來幫你抽個 ლ(́◕◞౪◟◕‵ლ)' % (btl.mk_mention(ctx))
    await ctx.send(msg)

    for msg, path in tm.get_many_tarot(n):
        await ctx.send(msg, file=discord.File(path))


@bot.command(name='薯條解牌', aliases=['貓貓解牌', '喵喵解牌'])
async def tarot_query(ctx, *args):
    for query in args:
        msg, path = tm.query_card(query)
        if path:
            await ctx.send(msg, file=discord.File(path))
        else:
            await ctx.send(msg)

# Dev Commands


@bot.command(aliases=['r'])
async def restart(ctx):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return
    btl.restart_bot()
    await ctx.send('Wait...')
    await bot.close()


@bot.command()
async def bye(ctx):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return
    btl.shutdown_bot()
    await ctx.send('Bye!')
    await bot.close()


@bot.command(aliases=['v'])
async def version(ctx):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return

    await ctx.send('Last build: %s' % bu.get_build_time())

if __name__ == "__main__":
    bot.run(token)
