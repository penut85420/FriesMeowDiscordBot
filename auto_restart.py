import os
import time

import discord

from modules.utils import BotUtils

bu = BotUtils()


class AutoRestart(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.channel = self.get_channel(bu.config['restart_channel'])
        while True:
            if os.path.exists('push'):
                fin = open('push', 'r')
                if fin.read() == '1':
                    await self.channel.send('!r')
                    fin.close()
                    open('push', 'w').write('0')
                    fin = open('push', 'r')
                fin.close()
            time.sleep(1)

    async def on_message(self, message):
        if message.content == 'bye':
            await self.close()

client = AutoRestart()
client.run(bu.config['auto_restart_token'])
