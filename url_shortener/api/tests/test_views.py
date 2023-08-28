from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase, APIClient

from url_shortener.models import ShortenedURL


class TestUrlShortenerAPI(APITestCase):
    def setUp(self):
        self.test_client = APIClient()

    def test_if_create_short_url_is_successful(self):
        url = api_reverse('urls-shorten')
        test_url = "https://www.test.com"
        res = self.test_client.post(path=url, data={"url": test_url})
        obj = ShortenedURL.objects.get(url=test_url)
        self.assertContains(res, obj.short_code, status_code=status.HTTP_201_CREATED)

    def test_invalid_url_for_creating_short_code_returns_error(self):
        url = api_reverse('urls-shorten')
        test_url = "test"
        res = self.test_client.post(path=url, data={"url": test_url})
        self.assertEqual(ShortenedURL.objects.count(), 0)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_existing_shortcode_request_returns_existing_shortcode(self):
        url = api_reverse('urls-shorten')
        test_url = "https://www.test.com"
        self.test_client.post(path=url, data={"url": test_url})
        obj = ShortenedURL.objects.get(url=test_url)
        res = self.test_client.post(path=url, data={"url": test_url})
        self.assertContains(res, obj.short_code, status_code=status.HTTP_303_SEE_OTHER)
        self.assertEqual(ShortenedURL.objects.count(), 1)

    def test_if_request_shortcode_detail_view_increases_number_of_hits(self):
        test_url = "https://www.test.com"
        obj = ShortenedURL.objects.create(url=test_url)
        detail_url = api_reverse("urls-detail", kwargs={"short_code": obj.short_code})
        self.assertEqual(obj.hits, 0)

        for _ in range(4):
            res = self.test_client.get(path=detail_url)
            self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        obj.refresh_from_db()
        self.assertEqual(obj.hits, 4)

    def test_if_stats_page_request_is_successfull(self):
        test_url = "https://www.test.com"
        obj = ShortenedURL.objects.create(url=test_url)
        stats_url = api_reverse("urls-stats", kwargs={"short_code": obj.short_code})
        res = self.test_client.get(path=stats_url)
        self.assertContains(res, obj.hits, status_code=status.HTTP_200_OK)
        self.assertContains(res, obj.url, status_code=status.HTTP_200_OK)
        expected_keys = {"url", "hits", "created_time"}
        self.assertTrue(set(list(res.json())).issubset(expected_keys))
