from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import AccessTokenlist
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")
        self.accesstokenlist_name = "Write world class code"
        self.accesstokenlist_value = "1153509b2845bcebb21c7de5905e9fa8c51c9d78"
        self.accesstokenlist = AccessTokenlist(name=self.accesstokenlist_name,
                                               value=self.accesstokenlist_value,
                                               owner=user)

    def test_model_can_create_a_accesstokenlist(self):
        """Test the accesstokenlist model can create a accesstokenlist."""
        old_count = AccessTokenlist.objects.count()
        self.accesstokenlist.save()
        new_count = AccessTokenlist.objects.count()
        self.assertNotEqual(old_count, new_count)

class ViewTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.accesstokenlist_data = {'name': 'Go to Ibiza',
                                     'value': '1153509b2845bcebb21c7de5905e9fa8c51c9d79',
                                     'owner': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.accesstokenlist_data,
            format="json")

    def test_api_can_create_a_accesstokenlist(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/accesstokenlists/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_accesstokenlist(self):
        """Test the api can get a given accesstokenlist."""
        accesstokenlist = AccessTokenlist.objects.get(id=1)
        response = self.client.get(
            '/accesstokenlists/',
            kwargs={'pk': accesstokenlist.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, accesstokenlist)

    def test_api_can_update_accesstokenlist(self):
        """Test the api can update a given accesstokenlist."""
        accesstokenlist = AccessTokenlist.objects.get()
        change_accesstokenlist = {'name': 'Something new',
                                  'value': '2153509b2845bcebb21c7de5905e9fa8c51c9d79'}
        res = self.client.put(
            reverse('details', kwargs={'pk': accesstokenlist.id}),
            change_accesstokenlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_accesstokenlist(self):
        """Test the api can delete a accesstokenlist."""
        accesstokenlist = AccessTokenlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': accesstokenlist.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)