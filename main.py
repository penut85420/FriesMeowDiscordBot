"""
Author: PenutChen
"""
import re
import random
import asyncio
import logging
import datetime

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import modules.utils as btl
from modules.dice import Dice
from modules.wikiman import WikiMan
from modules.tarot import TarotMeow
from modules.twsc import TwscCalendar
from modules.meow_talk import MeowTalk
from modules.fortune import FortuneMeow
from modules.sixty_jiazi import SixtyJiazi
from modules.sc_mutation import SC2Mutation
from modules.template import ResponseTemplate
from modules.fries_summon import FriesSummoner
from modules.easy_calculator import EasyCalculator

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

@bot.command(name='灑花', aliases=['撒花'])
async def sprinkle(ctx, *args):
    try:
        n = int(args[0])
    except:
        n = 1
    if n < 1: n = 1
    if n > 5: n = 5
    msg = ['灑花 (\\*￣▽￣)/‧☆\\*"\\`\'\\*-.,_,.-\\*\'\\`"\\*-.,_☆'] * n
    msg = '\n'.join(msg)
    await ctx.send(msg)

@bot.command(name='斗內', aliases=['贊助', '抖內', 'donate'])
async def donate(ctx, *args):
    msgs = [
        '贊助我的奴僕一杯咖啡吧 ヽ(=^･ω･^=)丿',
        '贊助我一個貓罐頭吧 ฅ(≚ᄌ≚)'
    ]
    url = 'https://p.ecpay.com.tw/DEA19'
    await ctx.send(f'{random.choice(msgs)}\n{url}')

@bot.command(name='粉絲', aliases=['fans', 'fb', 'ig'])
async def fanpage(ctx, *args):
    await ctx.send(
        '薯條的臉書粉絲團\n'
        '<https://www.facebook.com/FattyCatFries/>\n\n'
        '薯條的 Instagram\n'
        '<https://www.instagram.com/fatty_fries_cat/>'
    )

# Fries Commands


@bot.command(name='時間', aliases=['time'])
async def time(ctx):
    ts = datetime.datetime.now().strftime('%H:%M:%S')
    await ctx.send(f'喵喵喵，現在是臺灣時間 {ts}')

@bot.command(name='召喚薯條', aliases=['召喚貓貓', '召喚喵喵'])
async def summon(ctx, n=1):
    n = int(n)

    send = ctx.send

    if n > 1:
        if ctx.guild is not None:
            await ctx.send('%s 召喚超過一張會改成私訊給你喔！' % btl.mk_mention(ctx))
        send = ctx.author.send

    if n > 10:
        n = 10
        await send('%s 不可以一次召喚太多啊啊啊會壞掉啊啊啊啊啊' % btl.mk_mention(ctx))
    else:
        await send('%s 熱騰騰的薯條來囉~' % btl.mk_mention(ctx))

    for pic in fs.get_pictures(n):
        await send(file=discord.File(pic))


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

    send = ctx.send

    if n > 1:
        if ctx.guild is not None:
            await ctx.send('%s 抽超過一張塔羅牌會改成私訊給你喔！' % btl.mk_mention(ctx))
        send = ctx.author.send

    if len(args) > has_num:
        wish = ' '.join(args[has_num:])
        wish = btl.exchange_name(wish)
        msg = '%s 讓本喵來占卜看看 %s ლ(́◕◞౪◟◕‵ლ)' % (btl.mk_mention(ctx), wish)
    else:
        msg = '%s 讓本喵來幫你抽個 ლ(́◕◞౪◟◕‵ლ)' % (btl.mk_mention(ctx))
    await send(msg)

    for msg, path in tm.get_many_tarot(n):
        await send(msg, file=discord.File(path))


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
    await bot.logout()
    await bot.close()


@bot.command()
async def bye(ctx):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return
    btl.shutdown_bot()
    await ctx.send('Bye!')
    await bot.logout()
    await bot.close()


@bot.command(aliases=['v'])
async def version(ctx):
    if not bu.is_dev(ctx):
        await bu.not_dev_msg(ctx)
        return

    await ctx.send('Last build: %s' % bu.get_build_time())

if __name__ == "__main__":
    bot.run(token)
