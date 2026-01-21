from rest_framework import serializers

from ascii.mozz.models import ArtPost


class MozzArtPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtPost
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
