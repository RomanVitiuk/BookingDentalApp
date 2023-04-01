from denta.models import DentistDoctor
from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    """
    Check access to endpoints
    """
    def setUp(self):
        DentistDoctor.objects.create(
            first_name='Hypocrat',
            last_name='August',
            experience='5 years'
        )

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_team_url(self):
        response = self.client.get(reverse('team'))
        self.assertEqual(response.status_code, 200)

    def test_exist_doc_info_url(self):
        response = self.client.get(reverse('doc_info', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_not_exist_doc_info_url(self):
        response = self.client.get(reverse('doc_info', args=[5]))
        self.assertEqual(response.status_code, 404)

    def test_booking_date_url(self):
        response = self.client.get(reverse('booking_date'))
        self.assertEqual(response.status_code, 200)
