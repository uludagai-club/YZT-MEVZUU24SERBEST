from django.test import TestCase
from .models import *

class EvaluationTestCase(TestCase):
    def setUp(self):
        Education.objects.create(education="Lise")
        Certificy.objects.create(certificy="Sertifika")

    def test_education_creation(self):
        education = Education.objects.get(education="Lise")
        self.assertEqual(education.education, "Lise")

    def test_certificy_creation(self):
        certificy = Certificy.objects.get(certificy="Sertifika")
        self.assertEqual(certificy.certificy, "Sertifika")