from twitchio.ext import commands
from dotenv import load_dotenv
from t90_farm import T90_Farm
import asyncio
import aiohttp
import os
import re
import logging
import sys


class Farm_Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.getenv('IRC_TOKEN'),
            client_id=os.getenv('TWITCH_CLIENT_ID'),
            nick='t90_farmbot',
            prefix='!',
            initial_channels=[os.getenv('TWITCH_CHANNEL') or '#atomic_sausage']
            )
        self.queue = asyncio.Queue()
        self.farmRe = re.compile(r'\bt90Farm\b')
        self.farms = T90_Farm(session=aiohttp.ClientSession(),
                              farm_end_point=os.getenv("FARM_APP_ENDPOINT"),
                              farm_user=os.getenv("FARM_BOT_USER"),
                              farm_pass=os.getenv("FARM_BOT_PASSWORD"))
        self._init_logging()

    def _init_logging(self):
        self.log = logging.getLogger(__name__)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        out_hdlr.setLevel(logging.INFO)
        self.log.addHandler(out_hdlr)
        self.log.setLevel(logging.INFO)

    async def authenticate(self):
        self.log.debug('authenticate')
        await self.farms.authenticate()

    async def event_ready(self):
        self.log.info(f'ready | {self.nick}')
        await self.authenticate()

    async def event_message(self, message):
        self.log.debug(f'user {message.author.name} - msg: {message.content}')
        farm_cnt = len(self.farmRe.findall(message.content))
        if farm_cnt > 0:
            self.log.info(f'user: {message.author.name} - farms: {farm_cnt}')
            self.queue.put_nowait({
                'user': message.author.name,
                'farms': farm_cnt})
        await self.handle_commands(message)

    @commands.command(name='farms')
    async def get_farms(self, ctx):
        farm_cnt = await self.farms.get_farm_count()
        resp = f'there have been {farm_cnt} farms misplaced!'
        self.log.info(resp)
        await ctx.send(resp)

    async def consume(self):
        self.log.info('consumer started')
        while True:
            item = await self.queue.get()
            if item is None:
                self.log.error('none item found in queue')
                break

            await self.farms.update_farm_count(item['user'],
                                               item['farms'])
        self.log.info('consumer finished')


async def main():
    bot = Farm_Bot()
    await asyncio.gather(bot.start(), bot.consume())

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main(), debug=True)
