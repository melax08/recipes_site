from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import permissions, status, serializers, mixins
from django.shortcuts import get_object_or_404

from .models import User, Follow
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        return Response(self.get_serializer(request.user).data)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        following = User.objects.filter(following__user=request.user)
        return Response(self.get_serializer(following, many=True).data)

    @action(detail=True, permission_classes=(permissions.IsAuthenticated,),
            methods=['post', 'delete'])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            if request.user == author:
                raise serializers.ValidationError(
                    {'errors': 'Вы не можете подписываться на самого себя!'})
            if Follow.objects.filter(user=request.user, author=author).exists():
                raise serializers.ValidationError(
                    {'errors': 'Вы уже подписаны на этого пользователя.'})
            Follow.objects.create(user=request.user, author=author)
            return Response(self.get_serializer(author).data,
                            status=status.HTTP_201_CREATED)

        follow = Follow.objects.filter(user=request.user, author=author)
        if not follow.exists():
            raise serializers.ValidationError(
                {'errors': 'Вы не подписаны на этого автора.'})
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# class FollowViewSet(mixins.ListModelMixin,
#                     mixins.CreateModelMixin,
#                     mixins.DestroyModelMixin,
#                     GenericViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = ...
