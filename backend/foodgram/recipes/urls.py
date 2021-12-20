from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteCreateDeleteViewSet, ListCreateRecipeViewSet,
                    ListRetrieveIngredientViewSet,
                    RetrieveUpdateDeleteRecipeViewSet,
                    ShoppingListCreateDeleteViewSet, download_shopping_cart,
                    tag, tags_list)

app_name = 'recipes'

router = DefaultRouter()
router.register(
    'recipes',
    RetrieveUpdateDeleteRecipeViewSet,
    basename='retrieve_update__delete_recipes'
)
router.register('recipes', FavoriteCreateDeleteViewSet, basename='favorite')
router.register(
    'recipes',
    ShoppingListCreateDeleteViewSet,
    basename='shopping_list'
)
router.register(
    'recipes',
    ListCreateRecipeViewSet,
    basename='list_create_recipes'
)
router.register(
    'ingredients',
    ListRetrieveIngredientViewSet,
    basename='ingredients'
)


urlpatterns = [
    path('tags/', tags_list, name='tags_list'),
    path('tags/<int:pk>/', tag, name='tag'),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download_shopping_cart'
    ),
    path('', include(router.urls)),
]
