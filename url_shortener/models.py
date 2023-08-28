from random import choice
from string import ascii_letters, digits

from django.db import models
from django.conf import settings


AVAIABLE_CHARS = ascii_letters + digits


class ShortenedURL(models.Model):
    url = models.URLField(unique=True)
    short_code = models.CharField(max_length=15, unique=True, null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_time"]

    def __str__(self):
        return f"{self.url}->{self.short_code}"

    @staticmethod
    def create_random_code(chars=AVAIABLE_CHARS):
        return "".join([choice(chars) for _ in range(settings.MAXIMUM_URL_CHARS)])

    @classmethod
    def create_shortened_url(cls):
        random_code = cls.create_random_code()

        if cls.objects.filter(short_code=random_code).exists():
            return cls.create_shortened_url()

        return random_code

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.create_shortened_url()
        super().save(*args, **kwargs)
