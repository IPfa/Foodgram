import django_filters

from .models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def favorite_filter(request):
        is_favorited = request.query_params.get('is_favorited')
        if is_favorited == 'true':
            qs = Recipe.objects.filter(favorite__user=request.user)
        else:
            qs = Recipe.objects.all().exclude(
                favorite__user=request.user
            )
        return qs

    def shopping_cart_filter(request):
        is_in_shopping_cart = request.query_params.get('is_in_shopping_cart')
        if is_in_shopping_cart == 'true':
            qs = Recipe.objects.filter(shoppinglist__user=request.user)
        else:
            qs = Recipe.objects.all().exclude(
                shoppinglist__user=request.user
            )
        return qs

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
