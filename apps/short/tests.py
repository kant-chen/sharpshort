from faker import Faker
import json

from django.test import TestCase
from django.core.validators import URLValidator
from apps.short.models import Shorting

fake = Faker()


class TestShortingModel(TestCase):
    def test_pre_generate(self):
        cnt = 30
        Shorting.pre_generate(count=cnt)
        shortings_count = Shorting.objects.filter(
            is_valid=False, path__isnull=False, destination=None
        ).count()
        self.assertEqual(shortings_count, cnt)


class TestShorteningAPI(TestCase):
    def test_shorten_and_redirect(self):
        Shorting.pre_generate()
        client = self.client_class()
        # test shorten
        destination = fake.url()
        url = f"/shorten/create/?destination={destination}"
        res = client.post(url)
        content = json.loads(res.content)
        data = content.get("data")
        error = content.get("error")
        path = data["path"]

        self.assertIsNone(error)
        self.assertIsNotNone(data)
        self.assertTrue(data["is_valid"])
        URLValidator()(path)

        # test redirect
        res = client.get(path)
        self.assertRedirects(
            res, data["destination"], status_code=302, fetch_redirect_response=False
        )
