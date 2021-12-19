"""
Author: PenutChen
"""
import asyncio
import datetime as dt
import hashlib
import random

import discord

from fries import FriesBot, exchange_name, to_int, get_token, set_logger


bot = FriesBot()


# Commands


@bot.command(name='help', aliases=['喵'])
async def help(ctx):
    await ctx.send(bot.resp('help'))


@bot.command(aliases=['哈囉'])
async def hello(ctx, *_):
    await ctx.send(bot.resp('hello', ctx.author.mention))


@bot.command(name='灑花', aliases=['撒花'])
async def sprinkle(ctx, *args):
    n, _ = to_int(args)
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
        for pic in bot.get_pictures(n):
            await send(pic)

    if n > 10:
        n = 10
        await send(f'{mention} 不可以一次召喚太多啊啊啊會壞掉啊啊啊啊啊')
    else:
        await send(f'{mention} 熱騰騰的薯條來囉~')

    await _send()


@bot.command(aliases=['維基'])
async def wiki(ctx, *args):
    msgs = bot.get_wiki(*args)
    for msg in msgs:
        await ctx.send(msg)

# TRPG Commands


@bot.command(aliases=['擲骰子'])
async def dice(ctx, dice='', name=None):
    msg = f'{ctx.author.mention} {bot.roll_dice(dice, name)}'
    await ctx.send(msg)


@bot.command(aliases=['薯條算數', '薯條算術'])
async def calc(ctx, *args):
    msg = bot.do_calc(' '.join(args))
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
    sent = f'{sent}是「:{bot.get_crystal()}:」！'
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
    msg = bot.resp('fortune', ctx.author.mention, bot.get_fortune())
    await ctx.send(msg)


@bot.command(name='薯條甲子籤', aliases=['貓貓甲子籤', '喵喵甲子籤'])
async def sixty_jiazi(ctx):
    await ctx.send(bot.get_sixty_jiazi())


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

    for msg, path in bot.get_tarots(n):
        await send(msg, file=discord.File(path))


@bot.command(name='薯條解牌', aliases=['貓貓解牌', '喵喵解牌'])
async def tarot_query(ctx, *args):
    for query in args:
        msg, path = bot.query_card(query)
        if path:
            await ctx.send(msg, file=discord.File(path))
        else:
            await ctx.send(msg)

if __name__ == "__main__":
    set_logger()
    bot.run(get_token())
