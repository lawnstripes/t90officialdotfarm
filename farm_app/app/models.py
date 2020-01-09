from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute


class FarmModel(Model):
    class Meta:
        table_name = "t90-farms"
    counter = UnicodeAttribute(hash_key=True)
    counter_value = NumberAttribute(range_key=True)
