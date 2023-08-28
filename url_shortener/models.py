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
        """
            Create a random short code composed of characters from the provided set.

            Args:
                chars (str): The set of characters to choose from for creating the code.
                             Default is the set of available characters (AVAILABLE_CHARS).

            Returns:
                str: A randomly generated short code.

            Example:
                >>> code = ShortenedURL.create_random_code()
                >>> print(code)
                "8zxd9A"
        """
        return "".join([choice(chars) for _ in range(settings.MAXIMUM_URL_CHARS)])

    @classmethod
    def create_shortened_url(cls):
        """
         Create a new ShortenedURL instance with a unique random short code.

         This method generates a random short code and ensures that it is unique
         among existing ShortenedURL instances. If the generated code is already in use,
         the method recursively attempts to create a new one until a unique code is found.

         Returns:
             str: A unique random short code for the new ShortenedURL instance.

         Example:
             >>> shortened_url = ShortenedURL.create_shortened_url()
             >>> print(shortened_url)
             "6GkTf2"
         """
        random_code = cls.create_random_code()

        if cls.objects.filter(short_code=random_code).exists():
            return cls.create_shortened_url()

        return random_code

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.create_shortened_url()
        super().save(*args, **kwargs)
