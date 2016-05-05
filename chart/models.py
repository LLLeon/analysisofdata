from django.db import models
from mongoengine import *


# class ArtiInfo(Document):
#     title = StringField()
#     price = IntField()
#     area = ListField(StringField())
#     time = IntField()
#     look = StringField()
#     pub_date = StringField()
#     cates = ListField(StringField())
#     url = StringField()

#     meta = {'collection': 'sample'}


class ItemInfo(Document):
    title = StringField()
    price = IntField()
    area = ListField(StringField())
    pub_date = StringField()
    url = StringField()
    cates = ListField(StringField())
    time = IntField()
    look = StringField()

    meta = {'collection': 'sample'}