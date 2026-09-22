from rest_framework import serializers

from ascii.mozz.models import ArtPost, ArtPostAttachment, ScrollFile


class MozzArtPostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtPostAttachment
        fields = ["id", "name", "file"]


class MozzArtPostAttachmentUploadSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field="slug", queryset=ArtPost.objects.all())

    class Meta:
        model = ArtPostAttachment
        fields = ["id", "name", "post", "file"]


class MozzScrollFileSerializer(serializers.ModelSerializer):
    text = serializers.CharField(trim_whitespace=False, allow_blank=True)

    class Meta:
        model = ScrollFile
        fields = ["slug", "text", "updated_at"]
        read_only_fields = ["updated_at"]


class MozzArtPostSerializer(serializers.ModelSerializer):
    attachments = MozzArtPostAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ArtPost
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
