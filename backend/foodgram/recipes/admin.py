from django.contrib import admin

from .models import Favorite, Ingredient, Quantity, Recipe, ShoppingList, Tag
from .forms import TagForm

EMPTY = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def добавлен_в_избранное(self, obj):
        return obj.favorite.count()
    list_display = (
        'author',
        'name',
        'pub_date',
        'image',
        'text',
        'cooking_time',
        'добавлен_в_избранное',
        'pk'
    )
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    empty_value_display = EMPTY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    form = TagForm
    empty_value_display = EMPTY


@admin.register(Quantity)
class QuantityAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', 'pk')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY
