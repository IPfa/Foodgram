from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import (FollowCreateDeleteViewSet, ListUser, RetrieveUser,
                    SubscriptionsListView)

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', FollowCreateDeleteViewSet, basename='subscribe')


urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsListView.as_view(),
        name='subscriptions'
    ),
    path('users/', ListUser.as_view()),
    path('users/<int:pk>/', RetrieveUser.as_view()),
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
]
