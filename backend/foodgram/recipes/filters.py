import django_filters

from .models import Recipe

CHOICES = (
    (0, 'False'),
    (1, 'True'),
)


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = django_filters.ChoiceFilter(
        choices=CHOICES,
        method='favorite_filter'
    )
    is_in_shopping_cart = django_filters.ChoiceFilter(
        choices=CHOICES,
        method='shopping_cart_filter'
    )

    def favorite_filter(self, queryset, name, value):
        if int(value) == 1:
            qs = Recipe.objects.filter(favorite__user=self.request.user)
        else:
            qs = Recipe.objects.all().exclude(
                favorite__user=self.request.user
            )
        return qs

    def shopping_cart_filter(self, queryset, name, value):
        if int(value) == 1:
            qs = Recipe.objects.filter(shoppinglist__user=self.request.user)
        else:
            qs = Recipe.objects.all().exclude(
                shoppinglist__user=self.request.user
            )
        return qs

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
