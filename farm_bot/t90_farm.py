import asyncio
import aiohttp
import os
from yarl import URL


class T90_Farm():

    def __init__(self,
                 session: aiohttp.ClientSession,
                 farm_end_point=os.getenv('FARM_APP_ENDPOINT'),
                 farm_user=os.getenv('FARM_BOT_USER'),
                 farm_pass=os.getenv('FARM_BOT_PASSWORD')):
        self.farm_end_point = URL(farm_end_point)
        self.farm_user = farm_user or 'FARM_BOT'
        self.farm_password = farm_pass or \
            'FARM-BOTS-TOP-SECRET-CODE'
        self.session = session

    async def authenticate(self, session=None):
        session = session or self.session
        async with session.post(
            url=self.farm_end_point.with_path('/api/login'),
            json={'username': self.farm_user, 'password': self.farm_password}
        ) as response:
            auth = await response.json()
            self.access_token = auth['access_token']
            self.refresh_token = auth['refresh_token']
        self.auth_header = {
             'Authorization':
             f'Bearer {self.access_token}'
        }

    async def get_farm_count(self):
        async with self.session.get(
                    self.farm_end_point.with_path('/api/farms')
                ) as response:
            farms = await response.json()
        return farms['farms']

    async def update_farm_count(self, twitch_user, new_farms):
        async with self.session.post(
            url=self.farm_end_point.with_path('/api/farms'),
            json={'twitch_user': twitch_user, 'farms': new_farms},
            headers=self.auth_header
        ) as response:
            return await response.json()


async def main():
    try:
        session = aiohttp.ClientSession()
        farm = T90_Farm(session=session,
                        farm_end_point='http://localhost:1337')
        print(farm.farm_user)
        print(farm.farm_password)
        await farm.authenticate()
        f = await farm.get_farm_count()
        print(f)
        fm = await farm.update_farm_count('atomic_sausage', 10)
        print(fm)
    finally:
        await session.close()


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv(verbose=True)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
