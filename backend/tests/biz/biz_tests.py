from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import Group
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from biz.models import Biz, Hours
import datetime

BIZ_URL = reverse('biz-list')
# COMMENT_DETAIL_URL = reverse('comment-detail', args=comment.pk)
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('token_obtain_pair')
User = get_user_model()


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class TestBizModel(TestCase):
    """Tests for comment functions"""

    def setUp(self):
        self.client = APIClient()
        Group.objects.get_or_create(name="biz_post")
        Group.objects.get_or_create(name="biz_edit")
        payload_user = {
            'email': 'foo@foo.com',
            'password': 'testpassword',
            'name': 'foo',
            'username': 'foo'
        }
        self.client.post(CREATE_USER_URL, payload_user)
        self.user1_data = get_user_model().objects.get(email="foo@foo.com")
        member_group = Group.objects.get(name="member")
        member_group.user_set.add(self.user1_data)
        get_token1 = self.client.post(TOKEN_URL, payload_user, format='json')
        token1 = get_token1.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token1)

    def test_biz_create_authed(self):
        """Test that users in biz_post group can post new biz"""
        biz_post_group = Group.objects.get(name="biz_post")
        biz_post_group.user_set.add(self.user1_data)
        payload = {
            "title": "test",
            "description": "test",
            "address": "test",
            "city": "test",
            "phone": "+989123456789",
        }
        res = self.client.post(BIZ_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_biz_unauthorized(self):
        """Test that users NOT in biz_post group can NOT post biz"""
        payload = {
            "title": "test",
            "description": "test",
            "address": "test",
            "city": "test",
            "phone": "+989123456789",
        }
        res = self.client.post(BIZ_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_biz_edit_authorized(self):
        """Test that users in biz_edit group can edit biz infos"""
        payload = {
            "title": "test_edit",
            "description": "ORIGINAL",
            "address": "test",
            "city": "test",
            "phone": "+989123456789"
        }
        Biz.objects.create(**payload)
        biz_edit_group = Group.objects.get(name="biz_edit")
        biz_edit_group.user_set.add(self.user1_data)
        biz = Biz.objects.get(title="test_edit")
        res = self.client.patch(reverse('biz-detail', args=[biz.pk]), {'description': 'EDITED'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_biz = Biz.objects.get(title='test_edit').description
        self.assertEqual(new_biz, 'EDITED')

    def test_hours_eidt(self):
        """Test users can edit hours"""
        biz_payload = {
            "title": "test_edit",
            "description": "ORIGINAL",
            "address": "test",
            "city": "test",
            "phone": "+989123456789"
        }
        biz = Biz.objects.create(**biz_payload)
        Hours.objects.create(weekday=1, from_hour="10:00:00", to_hour="22:30:00", biz=biz)
        hour = Hours.objects.get(from_hour="10:00:00")
        res = self.client.patch(reverse('hours-detail', args=[hour.pk]), {'to_hour': '12:30:00'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_hour = Hours.objects.get(from_hour="10:00:00").to_hour
        self.assertEqual(new_hour, datetime.time(12, 30))