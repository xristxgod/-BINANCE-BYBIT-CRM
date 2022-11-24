from django.contrib import admin

from .models import Account
from .models import Google2FA
from .models import Telegram


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'active', 'user')
    list_filter = ('network', 'active', 'user')


class Google2FAAdmin(admin.ModelAdmin):
    list_display = ('code', 'qr_code', 'active', 'user')
    list_filter = ('active', 'user')


class TelegramAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'active', 'user')
    list_filter = ('active', 'user')


admin.site.register(Account, AccountAdmin)
admin.site.register(Google2FA, Google2FAAdmin)
admin.site.register(Telegram, TelegramAdmin)
