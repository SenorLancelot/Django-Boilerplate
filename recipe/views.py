from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Recipe, RecipeLike
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing recipe instances.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            new_like, created = RecipeLike.objects.get_or_create(user=request.user, recipe=recipe)
            if created:
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.delete()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipeLikeViewSet(viewsets.GenericViewSet):
    """
    A viewset for liking and unliking recipe instances.
    """
    serializer_class = RecipeLikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        new_like, created = RecipeLike.objects.get_or_create(user=request.user, recipe=recipe)
        if created:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

