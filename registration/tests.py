from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestCase(TestCase):
    # Preparar la prueba
    def setUp(self):
        User.objects.create_user('test', 'test@gmail.com', 'test1234')

    # Creando la prueba (Las pruebas pueden tener cualquier nombre seguido de test_)
    def test_profile_exist(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)