from django.conf import settings
from django.db import models
import secrets

# knockknock imports
import yagmail
import telegram
import requests
import json


# Create your models here.
def gen_secret():
    return secrets.token_hex(16)


class Channel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def send(self, message):
        attrs = ["gmailchannel", "telegramchannel", "slackchannel"]
        for attr in attrs:
            if hasattr(self, attr):
                obj = getattr(self, attr)
                obj.send(message)
                return
        raise AttributeError("could not find subclass")

    def message_to_str(self, message):
        return str(message)

class Pager(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default=gen_secret, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channels = models.ManyToManyField(Channel)

    def __str__(self):
        return self.name

    def page(self, request):
        message = dict(request.GET.dict(), **request.POST.dict())
        for channel in self.channels.all():
            channel.send(message)

class GmailChannel(Channel):
    recipient_email = models.EmailField()
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def send(self, message):
        yag_sender = yagmail.SMTP(self.email, self.password)
        yag_sender.send(
            self.recipient_email,
            "HTTPager: " + message.get("subject", "no subject"),
            self.message_to_str(message),
        )

class TelegramChannel(Channel):
    token = models.CharField(max_length=255)
    chat_id = models.IntegerField()

    def send(self, message):
        bot = telegram.Bot(token=self.token)
        bot.send_message(chat_id=self.chat_id, text=self.message_to_str(message))

class SlackChannel(Channel):
    webhook_url = models.CharField(max_length=255)
    channel = models.CharField(max_length=255)

    def send(self, message):
        dump = {
            "username": "HTTPager",
            "channel": self.channel,
            "icon_emoji": ":clapper:",
        }
        dump['text'] = self.message_to_str(message)
        dump['icon_emoji'] = ':tada:'
        requests.post(self.webhook_url, json.dumps(dump))

