from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Pager)
admin.site.register(GmailChannel)
admin.site.register(TelegramChannel)
admin.site.register(SlackChannel)