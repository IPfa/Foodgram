from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteCreateDeleteViewSet, ListCreateRecipeViewSet,
                    ListRetrieveIngredientViewSet, ListRetrieveTagViewSet,
                    RetrieveUpdateDeleteRecipeViewSet,
                    ShoppingListCreateDeleteViewSet, download_shopping_cart,)

app_name = 'recipes'

router_v1 = DefaultRouter()
router_v1.register(
    'recipes',
    RetrieveUpdateDeleteRecipeViewSet,
    basename='retrieve_update__delete_recipes'
)
router_v1.register('recipes', FavoriteCreateDeleteViewSet, basename='favorite')
router_v1.register(
    'recipes',
    ShoppingListCreateDeleteViewSet,
    basename='shopping_list'
)
router_v1.register(
    'recipes',
    ListCreateRecipeViewSet,
    basename='list_create_recipes'
)
router_v1.register(
    'ingredients',
    ListRetrieveIngredientViewSet,
    basename='ingredients'
)
router_v1.register(
    'tags',
    ListRetrieveTagViewSet,
    basename='tags'
)


urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('', include(router_v1.urls)),
]
