from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from ascii.mozz.models import ArtPost, ArtPostAttachment, ScrollFile
from ascii.mozz.serializers import (
    MozzArtPostAttachmentUploadSerializer,
    MozzArtPostSerializer,
    MozzScrollFileSerializer,
)


class MozzArtPostModelViewSet(ModelViewSet):
    queryset = ArtPost.objects.all()
    serializer_class = MozzArtPostSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"


class MozzArtPostAttachmentModelViewSet(ModelViewSet):
    queryset = ArtPostAttachment.objects.all()
    serializer_class = MozzArtPostAttachmentUploadSerializer
    permission_classes = [IsAdminUser]


class MozzScrollFileModelViewSet(ModelViewSet):
    queryset = ScrollFile.objects.all()
    serializer_class = MozzScrollFileSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "slug"
