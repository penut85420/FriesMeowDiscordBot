import asyncio
import random

import discord
from discord.ext.commands import CommandNotFound, AutoShardedBot
from loguru import logger


class FriesBot(AutoShardedBot):
    def __init__(self, **kwargs):
        from fries import (
            CrystalBallMeow, Dice, EasyCalculator,
            FortuneMeow, FriesSummoner, MeowTalk,
            ResponseTemplate, SixtyJiazi, TarotMeow, WikiMan
        )
        self.dice = Dice
        self.resp_template = ResponseTemplate()
        self.meow_talk = MeowTalk()
        self.fries_summoner = FriesSummoner()
        self.fortune_meow = FortuneMeow()
        self.tarot_meow = TarotMeow()
        self.calculator = EasyCalculator()
        self.wiki = WikiMan()
        self.sixty_jiazi = SixtyJiazi()
        self.crystal = CrystalBallMeow()

        activity = discord.Activity(
            name='奴僕清貓砂', type=discord.ActivityType.watching)

        AutoShardedBot.__init__(
            self, command_prefix='!',
            help_command=None, activity=activity, **kwargs
        )

    async def on_message(self, msg: discord.Message):
        if msg.author == self.user:
            return

        if msg.content.startswith('！'):
            msg.content = '!' + msg.content[1:]

        if msg.content.startswith('!'):
            log_type = 'msglog'
            if msg.guild is None:
                log_type = 'msglog2'
            logger.info(self.resp(log_type).format(msg))
        elif self.user in msg.mentions or msg.guild is None:
            logger.info(self.resp('msglog').format(msg))
            await self.chatting(msg)

        await AutoShardedBot.on_message(self, msg)

    async def on_ready(self):
        logger.info(f'{self.user} | Ready')

    async def on_command_error(self, _, error):
        if isinstance(error, CommandNotFound):
            return
        logger.info(str(error).replace('\n', ' | '))

    def resp(self, key, *args):
        return self.resp_template.get_resp(key, *args)

    def get_pictures(self, n):
        return self.fries_summoner.get_pictures(n)

    def get_fortune(self):
        return self.fortune_meow.get_fortune()

    def get_tarots(self, n):
        return self.tarot_meow.get_tarots(n)

    def query_card(self, query):
        return self.tarot_meow.query_card(query)

    def do_calc(self, formula):
        return self.calculator.calc(formula)

    def get_wiki(self, *args):
        return self.wiki.get_response(*args)

    def get_sixty_jiazi(self):
        return self.sixty_jiazi.pick()

    def get_crystal(self):
        return self.crystal.get()

    def roll_dice(self, dice, name):
        return self.dice.roller(dice, name)

    async def chatting(self, msg):
        async with msg.channel.typing():
            try:
                emojis = '🤔😂😊🤣😍😘😁😉😎'
                await msg.add_reaction(random.choice(emojis))
            except:
                pass
            await asyncio.sleep(0.5)
        await msg.channel.send(self.meow_talk.get_sent())
