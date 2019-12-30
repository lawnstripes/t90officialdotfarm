import boto3
import asyncio


class T90_Farm():

    def __init__(self, loop=asyncio.get_event_loop()):
        self.loop = loop
        self.dyn = boto3.resource('dynamodb', region_name='us-east-1')
        self.farm_table = self.dyn.Table('t90-farms')

    def get_farm_count(self):
        cnt = self.farm_table.get_item(Key={'counter': 'id'})
        return cnt['Item']['counter_value']

    async def update_farm_count(self, new_farms):
        self.farm_table.update_item(
            Key={'counter': 'id'},
            UpdateExpression='SET counter_value = counter_value + :farms',
            ExpressionAttributeValues={':farms': new_farms}
        )

    async def begin_update_farm_count(self, new_farms):
        return asyncio.create_task(self.update_farm_count(new_farms))


if __name__ == '__main__':
    farm = T90_Farm()
    print(farm.get_farm_count())
    asyncio.run(farm.update_farm_count_async(5))
    print(farm.get_farm_count())
