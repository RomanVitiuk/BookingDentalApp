from datetime import datetime, timedelta

from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from denta.models import DentistDoctor, Client
from denta.views import (
    BookingDateView, DetaiDoctorInfoView,
    DoctorListCardView, HomeView, query_result
)
from django.utils import timezone

from denta.utils import DOC_GRADE


class ViewsTestCase(TestCase):
    """
    Validation of templates and views rendering.
    """
    def setUp(self):
        DentistDoctor.objects.create(
            first_name='Hypocrat',
            last_name='August',
            experience='5 years'
        )
        DentistDoctor.objects.create(
            first_name='Clara',
            last_name='Bee',
            edication_grade=DOC_GRADE[1],
            experience='3 years'
        )
        DentistDoctor.objects.create(
            first_name='Mat',
            last_name='Mount',
            experience='12 years'
        )

        self.date = datetime.now(tz=timezone.utc)

        fibi = Client.objects.create(
            first_name='Fibi',
            last_name='Preston',
            email='fibipreston@mail.com',
            doc=DentistDoctor.objects.get(pk=2),
            visit_date=self.date
        )
        john = Client.objects.create(
            first_name='Homer',
            last_name='Simpson',
            email='homersimpson@mail.com',
            doc=DentistDoctor.objects.get(pk=1),
            visit_date=self.date
        )
        monty = Client.objects.create(
            first_name='Monty',
            last_name='Burns',
            email='montyburns@mail.com',
            doc=DentistDoctor.objects.get(pk=3),
            visit_date=self.date
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'denta/home.html')

    def test_team_view(self):
        response = self.client.get(reverse('team'))
        self.assertTemplateUsed(response, 'denta/team.html')

    def test_doc_info_view(self):
        response = self.client.get(reverse('doc_info', args=[2]))
        self.assertTemplateUsed(response, 'denta/doctor_info.html')

    def test_query_result_view(self):
        response = self.client.get(
            reverse('query_result'), {'query': 'doctor'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'denta/team.html')
        doctors = DentistDoctor.objects.filter(
            Q(edication_grade__icontains='doctor')
        ).order_by('first_name')
        self.assertEqual(doctors.count(), 2)
        self.assertQuerysetEqual(
            response.context['doctors'].order_by('first_name'), doctors
        )

    def test_booking_date_POST_correct_data_view(self):
        booking_date = self.date + timedelta(days=1)
        doc = DentistDoctor.objects.get(pk=3)
        response = self.client.post(
            '/booking-date/', {
                'first_name': 'Adam',
                'last_name': 'West',
                'email': 'adamwest@mail.com',
                'doc': doc.pk,
                'visit_date': booking_date
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_booking_date_POST_incorrect_data_view(self):
        booking_date = self.date
        doc = DentistDoctor.objects.get(pk=3)
        response = self.client.post(
            '/booking-date/', {
                'first_name': 'Adam',
                'last_name': 'West',
                'email': 'adamwest@mail.com',
                'doc': doc.pk,
                'visit_date': booking_date
            }
        )
        self.assertNotEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'denta/booking_date.html')
