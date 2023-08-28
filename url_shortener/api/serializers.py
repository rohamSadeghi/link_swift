from rest_framework import serializers

from url_shortener.models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    url = serializers.URLField()

    class Meta:
        model = ShortenedURL
        fields = ["url", "hits", "created_time"]
        read_only_fields = ["hits", "created_time"]
