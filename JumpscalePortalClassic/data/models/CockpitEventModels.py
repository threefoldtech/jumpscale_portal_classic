from jumpscale import j
from mongoengine import Document
from mongoengine.fields import IntField
from mongoengine.fields import StringField
from mongoengine.fields import ListField
from mongoengine.fields import DictField
from JumpscaleLib.data.models.Models import ModelBase


DB = 'jumpscale_cockpitevent'


class Email(ModelBase):
    type = StringField(default='email', choices=('email'), required=True)
    body = StringField(required=True, default='')
    body_type = StringField(choices=('md', 'html', 'text'))
    attachments = DictField()
    cc = ListField(StringField())
    sender = StringField(required=True)
    to = ListField(StringField(required=True))
    subject = StringField(required=True)
    epoch = IntField(default=j.data.time.getTimeEpoch(), required=True)


class Telegram(ModelBase):
    type = StringField(default='telegram', choices=('telegram'), required=True)
    io = StringField(choices=('input', 'output'), required=True)
    action = StringField(required=True)
    args = DictField()
    epoch = IntField(default=j.data.time.getTimeEpoch(), required=True)


class Alarm(ModelBase):
    type = StringField(default='alarm', choices=('alarm'), required=True)
    service = StringField(required=True)
    method = StringField(required=True)
    msg = StringField(required=True)
    epoch = IntField(default=j.data.time.getTimeEpoch(), required=True)


class Generic(ModelBase):
    type = StringField(default='Generic', choices=('Generic'), required=True)
    args = DictField()
    epoch = IntField(default=j.data.time.getTimeEpoch(), required=True)
