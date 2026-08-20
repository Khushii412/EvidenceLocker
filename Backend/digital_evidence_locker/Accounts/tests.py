from django.test import TestCase
from .models import User


class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username="testadmin",
            email="admin@example.com",
            password="TestPassword123",
            role=User.Role.ADMIN,
        )

        self.assertEqual(user.username, "testadmin")
        self.assertEqual(user.email, "admin@example.com")
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertTrue(user.check_password("TestPassword123"))

    def test_default_role(self):
        user = User.objects.create_user(
            username="testinvestigator",
            password="TestPassword123",
        )

        self.assertEqual(
            user.role,
            User.Role.INVESTIGATOR
        )

    def test_user_approval(self):
        user = User.objects.create_user(
            username="approveduser",
            password="TestPassword123",
        )

        self.assertFalse(user.is_approved)

        user.is_approved = True
        user.save()

        updated_user = User.objects.get(
            username="approveduser"
        )

        self.assertTrue(updated_user.is_approved)

    def test_user_string_representation(self):
        user = User.objects.create_user(
            username="adminuser",
            password="TestPassword123",
            role=User.Role.ADMIN,
        )

        self.assertEqual(
            str(user),
            "adminuser (Admin)"
        )