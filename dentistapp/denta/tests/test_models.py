from datetime import datetime

from django.test import TestCase
from denta.models import DentistDoctor, Client
from django.utils import timezone


class ModelsTestCase(TestCase):
    def setUp(self):
        DentistDoctor.objects.create(
            first_name='Hypocrat',
            last_name='August',
            experience='5 years'
        )
        DentistDoctor.objects.create(
            first_name='Clara',
            last_name='Bee',
            experience='3 years'
        )
        DentistDoctor.objects.create(
            first_name='Mat',
            last_name='Mount',
            experience='12 years'
        )

    def test_doc_count_records(self):
        res = DentistDoctor.objects.all().count()
        self.assertEqual(res, 3)

    def test_add_new_doctor(self):
        DentistDoctor.objects.create(
            first_name='Barbara',
            last_name='Dream',
            experience='4 years'
        )
        res = DentistDoctor.objects.all().count()
        self.assertEqual(res, 4)

    def test_update_doc(self):
        doc = DentistDoctor.objects.get(pk=3)
        DentistDoctor.objects.filter(pk=3).update(last_name='Bull')
        doc.refresh_from_db()
        self.assertEqual(doc.last_name, 'Bull')

    def test_delete_doc(self):
        doc = DentistDoctor.objects.get(pk=3)
        doc.delete()
        res = DentistDoctor.objects.all().count()
        self.assertEqual(res, 2)

    def test_create_client(self):
        doc = DentistDoctor.objects.get(pk=1)
        date = datetime.now(tz=timezone.utc)
        Client.objects.create(
            first_name='Fibi',
            last_name='Preston',
            email='fibipreston@mail.com',
            doc=doc,
            visit_date=date
        )
        clt = Client.objects.all()
        self.assertEqual(clt.count(), 1)
        self.assertQuerysetEqual(clt, Client.objects.all())
        self.assertEqual(clt[0].doc.experience, '5 years')
