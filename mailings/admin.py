from django.contrib import admin

from mailings.models import Notification, Client, Message


# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_at', 'finish_at', 'status')
    list_filter = ('message', 'start_at', )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
    search_fields = ('title',)