from django.db import transaction
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from url_shortener.api.serializers import ShortenedURLSerializer
from url_shortener.models import ShortenedURL


class ShortenedURLViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = ShortenedURLSerializer
    queryset = ShortenedURL.objects.all()
    lookup_url_kwarg = "short_code"
    lookup_field = "short_code"

    def retrieve(self, request, *args, **kwargs):
        shortened_url = self.get_object()
        with transaction.atomic():
            shortened_url.hits += 1
            shortened_url.save()

        return redirect(shortened_url.url)

    def build_location_url(self, short_code):
        detail_url = reverse("urls-detail", kwargs={"short_code": short_code}, request=self.request)
        return detail_url

    @action(detail=False, methods=['post'])
    def shorten(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data["url"]
        try:
            obj = self.get_queryset().get(url=url)
        except ShortenedURL.DoesNotExist:
            obj = serializer.save()
            return Response({"location": self.build_location_url(obj.short_code)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"location": self.build_location_url(obj.short_code)}, status=status.HTTP_303_SEE_OTHER)

    @action(detail=True)
    def stats(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        data = serializer.data
        return Response(data)
