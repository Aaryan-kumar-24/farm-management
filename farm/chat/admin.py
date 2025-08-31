from django.contrib import admin

from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    list = ('chat',)
    
admin.site.register(Chat,ChatAdmin)
