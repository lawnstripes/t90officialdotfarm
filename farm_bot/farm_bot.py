from twitchio.ext import commands
from dotenv import load_dotenv
from t90_farm import T90_Farm
import asyncio
import aiohttp
import os
import re


class Farm_Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            irc_token=os.getenv('IRC_TOKEN'),
            client_id=os.getenv('TWITCH_CLIENT_ID'),
            nick='t90_farmbot',
            prefix='!',
            initial_channels=['#atomic_sausage']
            )
        self.queue = asyncio.Queue()
        self.farmRe = re.compile(r'\bt90Farm\b')
        self.farms = T90_Farm(session=aiohttp.ClientSession(),
                              farm_end_point=os.getenv("FARM_APP_ENDPOINT"),
                              farm_user=os.getenv("FARM_BOT_USER"),
                              farm_pass=os.getenv("FARM_BOT_PASSWORD"))

    async def authenticate(self):
        await self.farms.authenticate()

    async def event_ready(self):
        print(f'ready | {self.nick}')
        await self.authenticate()

    async def event_message(self, message):
        farm_cnt = len(self.farmRe.findall(message.content))
#        print(f'text: {message.content} - farms: {farm_cnt}')
        if farm_cnt > 0:
            self.queue.put_nowait({
                'user': message.author.name,
                'farms': farm_cnt})
        await self.handle_commands(message)

    @commands.command(name='farms')
    async def get_farms(self, ctx):
        farm_cnt = await self.farms.get_farm_count()
        await ctx.send(f'there have been {farm_cnt} farms misplaced!')

    async def consume(self):
        print('consumer started')
        while True:
            item = await self.queue.get()
            if item is None:
                break

            await self.farms.update_farm_count(item['user'],
                                               item['farms'])
        print('consumer finished')


async def main():
    bot = Farm_Bot()
    await asyncio.gather(bot.start(), bot.consume())


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main(), debug=True)
