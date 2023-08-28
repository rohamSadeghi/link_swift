from django.urls import path, include
from rest_framework import routers

from url_shortener.api.views import ShortenedURLViewSet

router = routers.SimpleRouter()
router.register(r'urls', ShortenedURLViewSet, basename='urls')

urlpatterns = [
    path('', include(router.urls)),
]
