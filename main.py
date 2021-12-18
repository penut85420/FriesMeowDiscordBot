"""
Author: PenutChen
"""
import random
import asyncio
import hashlib
import datetime as dt

import discord
from loguru import logger
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from fries import (
    BotUtils, ResponseTemplate, FriesSummoner, FortuneMeow,
    TarotMeow, EasyCalculator, WikiMan, SixtyJiazi, MeowTalk,
    CrystalBallMeow, Dice, exchange_name, to_int
)

# Modules
utils = BotUtils()
resp = ResponseTemplate()
fries_summoner = FriesSummoner()
fortune_meow = FortuneMeow()
tarot_meow = TarotMeow()
calculator = EasyCalculator()
wiki = WikiMan()
sixty_jiazi = SixtyJiazi()
meow_talk = MeowTalk()
crystal = CrystalBallMeow()


class FriesBot(commands.Bot):
    def __init__(self, **kwargs):
        commands.Bot.__init__(self, **kwargs)

    async def on_message(self, msg: discord.Message):
        if msg.author == self.user:
            return

        if msg.content.startswith('！'):
            msg.content = '!' + msg.content[1:]

        if msg.content.startswith('!'):
            log_type = 'msglog'
            if msg.guild is None:
                log_type = 'msglog2'
            logger.info(resp.get_resp(log_type).format(msg))
        elif self.user in msg.mentions or msg.guild is None:
            logger.info(resp.get_resp('msglog').format(msg))
            await chatting(msg)

        await commands.Bot.on_message(self, msg)


activity = discord.Activity(name='奴僕清貓砂', type=discord.ActivityType.watching)
bot = FriesBot(command_prefix='!', help_command=None, activity=activity)


async def chatting(msg):
    async with msg.channel.typing():
        try:
            emojis = '🤔😂😊🤣😍😘😁😉😎'
            await msg.add_reaction(random.choice(emojis))
        except:
            pass
        await asyncio.sleep(0.5)
    await msg.channel.send(meow_talk.get_sent())

# Events


@bot.event
async def on_ready():
    logger.info(f'{bot.user} | Ready')


@bot.event
async def on_command_error(_, error):
    if isinstance(error, CommandNotFound):
        return
    logger.info(str(error).replace('\n', ' | '))

# Commands


@bot.command(name='help', aliases=['喵'])
async def help(ctx):
    msg = resp.get_resp('help')
    await ctx.send(msg)


@bot.command(aliases=['哈囉'])
async def hello(ctx, *_):
    try:
        msg = resp.get_resp('hello', ctx.author.nick or ctx.author.name)
    except:
        msg = resp.get_resp('hello', ctx.author.name)
    await ctx.send(msg)


@bot.command(name='灑花', aliases=['撒花'])
async def sprinkle(ctx, *args):
    n, _ = to_int(args[0])
    n = 1 if n < 1 else n
    n = 5 if n > 5 else n

    msg = ['灑花 (\\*￣▽￣)/‧☆\\*"\\`\'\\*-.,_,.-\\*\'\\`"\\*-.,_☆'] * n
    msg = '\n'.join(msg)

    await ctx.send(msg)


@bot.command(name='斗內', aliases=['贊助', '抖內', 'donate'])
async def donate(ctx, *_):
    msgs = [
        '贊助我的奴僕一杯咖啡吧 ヽ(=^･ω･^=)丿',
        '贊助我一個貓罐頭吧 ฅ(≚ᄌ≚)'
    ]
    url = 'https://p.ecpay.com.tw/DEA19'
    await ctx.send(f'{random.choice(msgs)}\n{url}')


@bot.command(name='粉絲', aliases=['fans', 'fb', 'ig'])
async def fanpage(ctx, *_):
    await ctx.send(
        '薯條的臉書粉絲團\n'
        '<https://www.facebook.com/FattyCatFries/>\n\n'
        '薯條的 Instagram\n'
        '<https://www.instagram.com/fatty_fries_cat/>'
    )

# Fries Commands


@bot.command(name='時間', aliases=['time', '薯條時間'])
async def time(ctx):
    ts = dt.datetime.utcnow() + dt.timedelta(hours=8)
    ts = ts.strftime('%H:%M:%S')
    await ctx.send(f'喵喵喵，現在時間 {ts} (GMT+8)')


@bot.command(name='召喚薯條', aliases=['召喚貓貓', '召喚喵喵'])
async def summon(ctx, n=1):
    n = int(n)
    n = 1 if n < 1 else n

    send = ctx.send
    mention = ctx.author.mention

    if n > 1:
        if ctx.guild is not None:
            await ctx.send(f'{mention} 召喚超過一張會改成私訊給你喔！')
        send = ctx.author.send

    async def _send():
        for pic in fries_summoner.get_pictures(n):
            await send(pic)

    if n > 10:
        n = 10
        await send(f'{mention} 不可以一次召喚太多啊啊啊會壞掉啊啊啊啊啊')
    else:
        await send(f'{mention} 熱騰騰的薯條來囉~')

    await _send()


@bot.command(aliases=['維基'])
async def wiki(ctx, *args):
    msgs = wiki.get_response(*args)
    for msg in msgs:
        await ctx.send(msg)

# TRPG Commands


@bot.command(aliases=['擲骰子'])
async def dice(ctx, dice='', name=None):
    msg = f'{ctx.author.mention} {Dice.roller(dice, name)}'
    await ctx.send(msg)


@bot.command(aliases=['薯條算數', '薯條算術'])
async def calc(ctx, *args):
    msg = calculator.calc(' '.join(args))
    await ctx.send(msg)

# Fortune Commands


@bot.command(name='薯條水晶球', aliases=['貓貓水晶球', '喵喵水晶球', 'crystal_ball'])
async def crystal_ball(ctx, *args):
    wish = ''
    if args:
        args = ' '.join(args)
        wish = exchange_name(args)
    sent = f'{ctx.author.mention} 讓本喵來幫你看看{wish}'
    msg = await ctx.channel.send(sent)

    await asyncio.sleep(1)
    sent = f'{sent}\n喵喵喵，召喚水晶球 :crystal_ball:！'
    await msg.edit(content=sent)

    await asyncio.sleep(1)
    sent = f'{sent}\n本喵從水晶球裡看到了，'
    await msg.edit(content=sent)

    await asyncio.sleep(1)
    sent = f'{sent}是「:{crystal.get()}:」！'
    await msg.edit(content=sent)


@bot.command(name='薯條抽籤', aliases=['貓貓抽籤', '喵喵抽籤', 'draw'])
async def draw(ctx, *args):
    draw_name = ['大吉', '吉', '小吉', '小兇', '兇', '大凶']

    if not args:
        r = random.choice(draw_name)
    else:
        ss = ''.join(ctx.message.content.split())
        ts = dt.datetime.now().strftime("%Y%m%d")
        ss = f'{ss}{ctx.author.id}{ts}'
        m = hashlib.sha384(ss.encode()).hexdigest()
        r = sum([ord(ch) for ch in m]) % len(draw_name)
        r = draw_name[r]

    await ctx.send(f'{ctx.author.mention} 抽到了「{r}」！')


@bot.command(name='薯條籤筒', aliases=['貓貓籤筒', '喵喵籤筒', '薯條籤桶', '貓貓籤桶', '喵喵籤桶'])
async def fortune(ctx):
    msg = resp.get_resp(
        'fortune', ctx.author.mention,
        fortune_meow.get_fortune())
    await ctx.send(msg)


@bot.command(name='薯條甲子籤', aliases=['貓貓甲子籤', '喵喵甲子籤'])
async def sixty_jiazi(ctx):
    await ctx.send(sixty_jiazi.pick())


@bot.command(name='薯條塔羅', aliases=['貓貓塔羅', '喵喵塔羅'])
async def tarot(ctx, *args):
    n, has_num = to_int(args)

    send = ctx.send
    mention = ctx.author.mention

    if n > 1:
        if ctx.guild is not None:
            await ctx.send(f'{mention} 抽超過一張塔羅牌會改成私訊給你喔！')
        send = ctx.author.send

    if len(args) > has_num:
        wish = ' '.join(args[has_num:])
        wish = exchange_name(wish)
        msg = f'{mention} 讓本喵來占卜看看 {wish} ლ(́◕◞౪◟◕‵ლ)'
    else:
        msg = f'{mention} 讓本喵來幫你抽個 ლ(́◕◞౪◟◕‵ლ)'
    await send(msg)

    for msg, path in tarot_meow.get_many_tarot(n):
        await send(msg, file=discord.File(path))


@bot.command(name='薯條解牌', aliases=['貓貓解牌', '喵喵解牌'])
async def tarot_query(ctx, *args):
    for query in args:
        msg, path = tarot_meow.query_card(query)
        if path:
            await ctx.send(msg, file=discord.File(path))
        else:
            await ctx.send(msg)

if __name__ == "__main__":
    bot.run(utils.get_token())
