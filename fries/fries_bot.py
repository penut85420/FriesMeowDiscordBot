import asyncio
import random
from threading import Lock

import discord
from discord.ext.commands import AutoShardedBot, CommandNotFound
from loguru import logger
from opencc import OpenCC
from revChatGPT.revChatGPT import Chatbot

from .utils import get_debug_guild, get_chatgpt_config


class FriesBot(AutoShardedBot):
    def __init__(self, **kwargs):
        from fries import (
            CrystalBallMeow,
            Dice,
            EasyCalculator,
            FortuneMeow,
            FriesSummoner,
            MeowTalk,
            ResponseTemplate,
            SixtyJiazi,
            TarotMeow,
            WikiMan,
        )

        self.mutex_lock = Lock()
        self.gpt_using = False
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

        chatgpt_config = get_chatgpt_config()
        self.chatbot = Chatbot(chatgpt_config, conversation_id=None)
        self.chatbot.refresh_session()
        self.cc_conv = OpenCC("s2t")
        self.delim = chatgpt_config["delim"]
        self.target_channels = chatgpt_config["target_channel"]

        activity = discord.Activity(
            name="/薯條喵喵喵",
            type=discord.ActivityType.playing,
        )

        AutoShardedBot.__init__(
            self,
            command_prefix="!",
            help_command=None,
            activity=activity,
            debug_guilds=get_debug_guild(),
            **kwargs,
        )

    def is_using(self):
        with self.mutex_lock:
            return self.gpt_using

    def toggle_using(self, b: bool):
        with self.mutex_lock:
            self.gpt_using = b

    def is_need_break(self, msg: str):
        for d in self.delim:
            if msg.endswith(d):
                return True

        return False

    def get_chatgpt_response(self, prompt: str):
        for resp in self.chatbot.get_chat_response(prompt, output="stream"):
            resp_msg: str = self.cc_conv.convert(resp["message"])
            resp_msg = resp_msg.replace("\n\n", "\n")
            resp_msg = resp_msg.replace("。喵喵", "，喵喵")
            if self.is_need_break(resp_msg):
                yield resp_msg
        yield resp_msg
        self.chatbot.reset_chat()

    async def on_message(self, msg: discord.Message):
        if msg.author == self.user:
            return

        if msg.content.startswith("！"):
            msg.content = "!" + msg.content[1:]

        if msg.content.startswith("!"):
            log_type = "msglog"
            if msg.guild is None:
                log_type = "msglog2"
            logger.info(self.resp(log_type).format(msg))
            if "薯條" in msg.content:
                await msg.channel.send("現在改為斜線指令囉！請輸入 /薯條喵喵喵 獲得更多資訊")
        elif self.user in msg.mentions or msg.guild is None:
            logger.info(self.resp("msglog").format(msg))
            await self.chatting(msg)

        await AutoShardedBot.on_message(self, msg)

    async def on_ready(self):
        logger.info(f"{self.user} | Ready")

    async def on_command_error(self, _, error):
        if isinstance(error, CommandNotFound):
            return
        logger.info(str(error).replace("\n", " | "))

    def resp(self, key, *args):
        return self.resp_template.get_resp(key, *args)

    def get_pictures(self, n):
        return self.fries_summoner.get_pictures(n)

    def get_fortune(self):
        return self.fortune_meow.get_fortune()

    def get_tarots(self, n):
        return self.tarot_meow.get_tarots(n)

    def get_gpt_tarots(self, problem):
        return self.tarot_meow.get_gpt_tarot(problem)

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
                emojis = "🤔😂😊🤣😍😘😁😉😎"
                await msg.add_reaction(random.choice(emojis))
            except:
                pass
            await asyncio.sleep(0.5)
        await msg.channel.send(self.meow_talk.get_sent() + "\n現在改為斜線指令囉！")
