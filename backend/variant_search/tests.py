from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class VariantTests(APITestCase):
    def test_variant_endpoint(self):
        url = reverse("variant-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.json()["count"])

    def test_variant_endpoint_update(self):
        url = reverse("variant-detail", kwargs={"pk": 1})
        response = self.client.get(url)

        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, response.json()["count"])
        breakpoint()
