from django.contrib import admin
from users.models import User

# Register your models here.
@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name')
    list_filter = ('first_name',)
    search_fields = ('first_name', 'email')