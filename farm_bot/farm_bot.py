from twitchio.ext import commands
from dotenv import load_dotenv
from t90_farm import T90_Farm
import asyncio
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
        self.farms = T90_Farm()

    async def event_ready(self):
        print(f'ready | {self.nick}')

    async def event_message(self, message):
        farm_cnt = len(self.farmRe.findall(message.content))
        print(f'text: {message.content} - farms: {farm_cnt}')
        if farm_cnt > 0:
            self.queue.put_nowait(farm_cnt)
        await self.handle_commands(message)

    @commands.command(name='farms')
    async def my_command(self, ctx):
        farm_cnt = self.farms.get_farm_count()
        await ctx.send(f'there have been {farm_cnt} farms misplaced!')

    async def consume(self):
        print('consumer started')
        while True:
            item = await self.queue.get()
            if item is None:
                break

            print(f'consumer got {item}')
            await self.farms.begin_update_farm_count(item)
        print('consumer finished')


async def main():
    bot = Farm_Bot()
    await asyncio.gather(bot.start(), bot.consume())


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main(), debug=True)
