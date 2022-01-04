from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


from .filters import RecipeFilter
from .models import Favorite, Ingredient, Quantity, Recipe, ShoppingList, Tag
from .serializers import (CreateRecipeSerializer, FavoriteRecipeSerializer,
                          IngredientSerializer, RetrieveRecipeSerializer,
                          TagSerializer)


class FavoriteForbidden(APIException):
    status_code = 400
    default_detail = 'Вы уже подписаны на этот рецепт'
    default_code = 'forbidden'


class UnfavoriteForbidden(FavoriteForbidden):
    default_detail = 'Вы не подписаны на этот рецепт'


class AddingInShoppingListForbidden(FavoriteForbidden):
    default_detail = 'Этот рецепт уже находится в списке покупок'


class RemovingFromShoppingListForbidden(FavoriteForbidden):
    default_detail = 'Этого рецепта нет в списке покупок'


class ListCreateRecipeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = RetrieveRecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return RetrieveRecipeSerializer
        return CreateRecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        if is_favorited is not None:
            queryset = RecipeFilter.favorite_filter(self.request)
        if is_in_shopping_cart is not None:
            queryset = RecipeFilter.shopping_cart_filter(self.request)
        return queryset


class RetrieveUpdateDeleteRecipeViewSet(mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RetrieveRecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveRecipeSerializer
        return CreateRecipeSerializer


class FavoriteCreateDeleteViewSet(mixins.RetrieveModelMixin,
                                  mixins.DestroyModelMixin,
                                  viewsets.GenericViewSet):

    queryset = Recipe.objects.all()

    @action(
        methods=['get', 'delete'],
        detail=True,
        url_path='favorite',
        url_name='favorite'
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        favorite_object = Favorite.objects.filter(user=user, recipe=recipe)
        if request.method == 'GET':
            if favorite_object.exists():
                raise FavoriteForbidden()
            Favorite.objects.create(user=user, recipe=recipe)
            favorited_recipe = Recipe.objects.get(favorite__user=user, pk=pk)
            serializer = FavoriteRecipeSerializer(favorited_recipe)
            return Response(serializer.data)
        if not favorite_object.exists():
            raise UnfavoriteForbidden()
        favorite_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListCreateDeleteViewSet(FavoriteCreateDeleteViewSet):

    queryset = Recipe.objects.all()

    @action(
        methods=['get', 'delete'],
        detail=True,
        url_path='shopping_cart',
        url_name='shopping_cart'
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipe.objects.get(pk=pk)
        shopping_list_object = ShoppingList.objects.filter(
            user=user,
            recipe=recipe
        )
        if request.method == 'GET':
            if shopping_list_object.exists():
                raise AddingInShoppingListForbidden()
            ShoppingList.objects.create(user=user, recipe=recipe)
            added_in_shopping_list_recipe = Recipe.objects.get(
                shoppinglist__user=user,
                pk=pk
            )
            serializer = FavoriteRecipeSerializer(
                added_in_shopping_list_recipe
            )
            return Response(serializer.data)
        if not shopping_list_object.exists():
            raise RemovingFromShoppingListForbidden
        shopping_list_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListRetrieveIngredientViewSet(mixins.RetrieveModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
    permission_classes = (permissions.AllowAny,)


class ListRetrieveTagViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


@api_view(['GET'])
def download_shopping_cart(request):
    content = []
    ingredients = {}
    shopping_list = ShoppingList.objects.filter(user=request.user)
    for item in range(0, len(shopping_list)):
        quantities = Quantity.objects.filter(recipe=shopping_list[item].recipe)
        for item in range(0, len(quantities)):
            quantity_ingredient = Ingredient.objects.get(
                name=quantities[item].ingredient
            )
            quantity_quantity = quantities[item].amount
            if quantity_ingredient.name in ingredients.keys():
                new_ingredient_quantity = (
                    ingredients[quantity_ingredient.name] + quantity_quantity
                )
                ingredients[quantity_ingredient.name] = new_ingredient_quantity
            else:
                ingredients[quantity_ingredient.name] = quantity_quantity
    for ingredient in ingredients:
        ingredient_quantity = ingredients[ingredient]
        mu = Ingredient.objects.get(name=ingredient).measurement_unit
        contetnt_member = f'- {ingredient} ({mu}) - {ingredient_quantity}<br>'
        content.append(contetnt_member)
    str = ''.join(content)
    filename = 'my-shopping-cart.pdf'
    html = HTML(string=str)
    generated_pdf = html.write_pdf()
    resp = HttpResponse(generated_pdf, content_type='pdf')
    resp['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return resp
