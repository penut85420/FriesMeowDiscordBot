"""
Author: PenutChen
"""
import asyncio
import datetime as dt
import hashlib
import random

import discord
from discord.commands import Option
from fries import FriesBot, exchange_name, get_token, set_logger


bot = FriesBot()
# Commands


@bot.slash_command(name="薯條喵喵喵", description="喵喵喵！")
async def help(ctx):
    await ctx.respond(bot.resp("help"))


@bot.slash_command(name="薯條哈囉", description="跟本喵打招呼")
async def hello(ctx):
    await ctx.respond(bot.resp("hello", ctx.author.mention))


@bot.slash_command(name="薯條灑花", description="灑花！")
async def sprinkle(ctx, n: Option(int, "想灑花的次數", name="次數", required=False, default=1)):
    n = 1 if n < 1 else n
    n = 5 if n > 5 else n

    msg = ["灑花 (\\*￣▽￣)/‧☆\\*\"\\`'\\*-.,_,.-\\*'\\`\"\\*-.,_☆"] * n
    msg = "\n".join(msg)

    await ctx.respond(msg)


@bot.slash_command(name="薯條斗內", description="來個贊助本喵罐罐的連結")
async def donate(ctx):
    msgs = ["贊助我的奴僕一杯咖啡吧 ヽ(=^･ω･^=)丿", "贊助我一個貓罐頭吧 ฅ(≚ᄌ≚)"]
    url = "https://p.ecpay.com.tw/DEA19"
    await ctx.respond(f"{random.choice(msgs)}\n{url}")


@bot.slash_command(name="薯條粉絲", description="秀出本喵的粉絲團")
async def fanpage(ctx):
    await ctx.respond(
        "薯條的臉書粉絲團\n"
        "<https://www.facebook.com/FattyCatFries/>\n\n"
        "薯條的 Instagram\n"
        "<https://www.instagram.com/fatty_fries_cat/>"
    )


# Fries Commands


@bot.slash_command(name="薯條時間", description="顯示 GMT+8 時間")
async def time(ctx):
    ts = dt.datetime.utcnow() + dt.timedelta(hours=8)
    ts = ts.strftime("%H:%M:%S")
    await ctx.respond(f"喵喵喵，現在時間 {ts} (GMT+8)")


@bot.slash_command(name="召喚薯條", description="獲得本喵的美照一張")
async def summon(ctx, n: Option(int, "美照的數量", name="數量", required=False, default=1)):
    n = int(n)
    n = 1 if n < 1 else n

    send = ctx.respond
    mention = ctx.author.mention

    if n > 1:
        if ctx.guild is not None:
            await ctx.respond(f"{mention} 召喚超過一張會改成私訊給你喔！")
        send = ctx.author.send

    async def _send():
        for pic in bot.get_pictures(n):
            await send(pic)

    if n > 10:
        n = 10
        await send(f"{mention} 不可以一次召喚太多啊啊啊會壞掉啊啊啊啊啊")
    else:
        await send(f"{mention} 熱騰騰的薯條來囉~")

    await _send()


@bot.slash_command(name="薯條維基", description="搜尋中文維基頁面")
async def wiki(ctx, query: Option(str, "想要搜尋的頁面名稱", name="搜尋目標", required=True)):
    msgs = bot.get_wiki(query)
    for msg in msgs:
        await ctx.respond(msg)


# TRPG Commands


@bot.slash_command(name="薯條擲骰子", description="讓本喵來幫你擲個骰子")
async def dice(
    ctx,
    dice: Option(str, "骰子的格式，決定骰子的面數與個數", name="格式", required=True),
    name: Option(str, "任務名稱", name="任務", required=False),
):
    msg = f"{ctx.author.mention} {bot.roll_dice(dice, name)}"
    await ctx.respond(msg)


@bot.slash_command(name="薯條算術", description="讓本喵來幫你做個簡單運算")
async def calc(ctx, pattern: Option(str, "想要讓本喵幫你計算的數學式", name="算式", required=True)):
    msg = bot.do_calc(pattern)
    await ctx.respond(msg)


# Fortune Commands


@bot.slash_command(name="薯條水晶球", description="讓本喵幫你看看薯條水晶球")
async def crystal_ball(
    ctx,
    wish: Option(str, "你的願望是什麼？讓本喵幫你看看吧！", name="願望", required=False, default=""),
):
    wish = exchange_name(wish)
    sent = f"{ctx.author.mention} 讓本喵來幫你看看{wish}"
    msg = await ctx.respond(sent)

    await asyncio.sleep(1)
    sent = f"{sent}\n喵喵喵，召喚水晶球 :crystal_ball:！"
    await msg.edit_original_message(content=sent)

    await asyncio.sleep(1)
    sent = f"{sent}\n本喵從水晶球裡看到了，"
    await msg.edit_original_message(content=sent)

    await asyncio.sleep(1)
    sent = f"{sent}是「:{bot.get_crystal()}:」！"
    await msg.edit_original_message(content=sent)


@bot.slash_command(name="薯條抽籤", description="讓本喵來幫你抽根簡單的籤")
async def draw(ctx, wish: Option(str, "你想要占卜的目標是什麼？", name="目標", required=False)):
    draw_name = ["大吉", "吉", "小吉", "小兇", "兇", "大凶"]

    if not wish:
        r = random.choice(draw_name)
        await ctx.respond(f"{ctx.author.mention} 抽到了「{r}」！")
    else:
        ts = dt.datetime.now().strftime("%Y%m%d")
        ss = f"{wish}{ctx.author.id}{ts}"
        m = hashlib.sha384(ss.encode()).hexdigest()
        r = sum([ord(ch) for ch in m]) % len(draw_name)
        r = draw_name[r]
        await ctx.respond(f"{ctx.author.mention} 的「{wish}」抽到了「{r}」！")


@bot.slash_command(name="薯條籤筒", description="讓本喵來幫你抽根淺草籤")
async def fortune(ctx, _: Option(str, "來個淺草籤幫你的未來祈願吧～", name="祈願", required=False)):
    msg = bot.resp("fortune", ctx.author.mention, bot.get_fortune())
    await ctx.respond(msg)


@bot.slash_command(name="薯條甲子籤", description="讓本喵幫你抽一張六十甲子籤")
async def sixty_jiazi(ctx, _: Option(str, "人定勝天，路是自己走出來的", name="命運", required=False)):
    await ctx.respond(bot.get_sixty_jiazi())


@bot.slash_command(name="薯條塔羅", description="讓本喵來幫你抽張塔羅牌")
async def tarot(
    ctx,
    n: Option(int, "想要抽的塔羅牌數量", name="牌數", required=False, default=1),
    wish: Option(str, "讓本喵為你的夢想抽張塔羅牌吧！", name="夢想", required=False),
):
    send = ctx.respond
    mention = ctx.author.mention

    if n > 1:
        if ctx.guild is not None:
            await ctx.respond(f"{mention} 抽超過一張塔羅牌會改成私訊給你喔！")
        send = ctx.author.send

    if wish is not None:
        wish = exchange_name(wish)
        msg = f"{mention} 讓本喵來占卜看看 {wish} ლ(́◕◞౪◟◕‵ლ)"
    else:
        msg = f"{mention} 讓本喵來幫你抽個 ლ(́◕◞౪◟◕‵ლ)"
    await send(msg)

    for msg, path in bot.get_tarots(n):
        await send(msg, file=discord.File(path))


@bot.slash_command(name="薯條解牌", description="查詢特定塔羅牌")
async def tarot_query(ctx, query: Option(str, "想要解牌的塔羅牌名稱", name="牌名", required=True)):
    msg, path = bot.query_card(query)
    if path:
        await ctx.respond(msg, file=discord.File(path))
    else:
        await ctx.respond(msg)


if __name__ == "__main__":
    set_logger()
    bot.run(get_token())
