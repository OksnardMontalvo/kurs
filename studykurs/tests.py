
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from studykurs.models import UserAccount, Course
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class AutTest(TestCase):

    def test_inter(self):
        def setUp(self):
            self.url = reverse('search_view')
            self.user = User.objects.create(
                username='testuser',
                email='test@test.com',
                password='qwerty123',
            )
            self.course = Course.objects.create(title='Java для начинающих')
            self.course2 = Course.objects.create(title='Java для начинающих2')
        def test_search(self):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "kurs/search.html")
            self.assertQuerysetEqual(
                response.context.get('object_list'),
                map(repr, [self.course, self.course2]),
                ordered=False
            )











