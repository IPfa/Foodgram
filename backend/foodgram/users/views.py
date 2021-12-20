from foodgram.pagination import CustomPageNumberPagination
from recipes.serializers import FollowSerializer
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer


class SubscriptionForbidden(APIException):
    status_code = 400
    default_detail = 'Вы не можете подписаться дважды или на самого себя'
    default_code = 'forbidden'


class UnsubscriptionForbidden(SubscriptionForbidden):
    default_detail = 'Вы не подписаны на этого пользователя'


class RetrieveUser(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListUser(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination


class FollowCreateDeleteViewSet(mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):

    queryset = CustomUser.objects.all()

    @action(
        methods=['get', 'delete'],
        detail=True,
        url_path='subscribe',
        url_name='subscribe'
    )
    def subscribe(self, request, pk=None):
        author = CustomUser.objects.get(pk=pk)
        user = request.user
        follow = Follow.objects.filter(user=user, author=author)
        if request.method == 'GET':
            if user == author or follow.exists():
                raise SubscriptionForbidden()
            Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                author,
                context={'request': request}
            )
            return Response(serializer.data)
        if not follow.exists():
            raise UnsubscriptionForbidden()
        Follow.objects.filter(user=user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        subscriptions = CustomUser.objects.filter(
            following__user=self.request.user
        )
        return subscriptions
