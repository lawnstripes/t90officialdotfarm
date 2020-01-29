import asyncio
import aiohttp
import os
from yarl import URL


class T90_Farm():

    def __init__(self,
                 session: aiohttp.ClientSession,
                 farm_end_point=None,
                 farm_user=None,
                 farm_pass=None):
        self.farm_end_point = URL(farm_end_point or
                                  os.getenv("FARM_APP_ENDPOINT"))
        self.farm_user = farm_user or os.getenv("FARM_BOT_USER")
        self.farm_password = farm_pass or os.getenv("FARM_BOT_PASSWORD")
        self.session = session
        self.access_token = None
        self.refresh_token = None

    async def authenticate(self, session=None):
        session = session or self.session
        async with session.post(
            url=self.farm_end_point.with_path('/api/login'),
            json={'username': self.farm_user, 'password': self.farm_password}
        ) as response:
            if response.status == 200:
                auth = await response.json()
                self.access_token = auth['access_token']
                self.refresh_token = auth['refresh_token']
            else:
                raise Exception('login failed')

    async def refresh_access_token(self):
        if self.refresh_token is None:
            await self.authenticate()
            return
        self.auth_header = self.access_token
        async with self.session.post(
            url=self.farm_end_point.with_path('api/refresh'),
            headers=self.format_auth_header(self.refresh_token)
        ) as response:
            auth = await response.json()
            self.access_token = auth['access_token']

    async def get_farm_count(self):
        async with self.session.get(
                    self.farm_end_point.with_path('/api/farms')
                ) as response:
            farms = await response.json()
        return farms['farms']

    async def update_farm_count(self, twitch_user, new_farms):
        if not self.access_token:
            await self.authenticate()

        for attempt in range(5):
            async with self.session.post(
                url=self.farm_end_point.with_path('/api/farms'),
                json={'twitch_user': twitch_user, 'farms': new_farms},
                headers=self.format_auth_header()
            ) as response:
                if 200 <= response.status <= 300:
                    return await response.json()
                elif response.status == 401:
                    err = await response.json()
                    await asyncio.sleep(2 ** attempt+1)
                    if err is not None and err['msg'] == 'Token has expired':
                        await self.refresh_access_token()
                    else:
                        await self.authenticate()
                else:
                    await asyncio.sleep(5 ** attempt+1)
        raise Exception('farm count update failed')

    def format_auth_header(self, token=None):
        token = token or self.access_token
        return {
                'Authorization':
                f'Bearer {token}'
            }


async def main():
    try:
        session = aiohttp.ClientSession()
        farm = T90_Farm(session=session,
                        farm_end_point='http://localhost:5000')
        await farm.authenticate()
        f = await farm.get_farm_count()
        print(f)
        fm = await farm.update_farm_count('atomic_sausage', 10)
        print(f'fm {fm}')
    finally:
        await session.close()


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
