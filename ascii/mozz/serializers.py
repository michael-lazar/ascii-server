from rest_framework import serializers

from ascii.mozz.models import ArtPost, ArtPostAttachment


class MozzArtPostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtPostAttachment
        fields = ["id", "name", "file"]


class MozzArtPostSerializer(serializers.ModelSerializer):
    attachments = MozzArtPostAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ArtPost
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
