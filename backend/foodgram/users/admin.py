from django.contrib import admin

from .models import CustomUser, Follow

EMPTY = '-пусто-'


@admin.register(CustomUser)
class CustomUSerAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'pk',
    )
    list_filter = ('username', 'email')
    search_fields = ('username',)
    empty_value_display = EMPTY


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = EMPTY
