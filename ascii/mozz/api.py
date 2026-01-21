from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ascii.mozz.models import ArtPost
from ascii.mozz.serializers import MozzArtPostSerializer


class MozzArtPostModelViewSet(ModelViewSet):
    queryset = ArtPost.objects.all()
    serializer_class = MozzArtPostSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"
