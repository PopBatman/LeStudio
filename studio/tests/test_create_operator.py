from io import StringIO
import secrets
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command, CommandError
from django.db import IntegrityError
from django.test import TestCase


class CreateOperatorTests(TestCase):
    def setUp(self):
        self.password = secrets.token_urlsafe(32)
        self.output = StringIO()
        self.prompt = self.enterContext(
            patch("workspace.management.commands.create_operator.getpass")
        )
        self.prompt.return_value = self.password

    def create(self, username="operatrice"):
        call_command("create_operator", username, stdout=self.output)

    def test_creates_only_a_regular_active_operator_with_a_hashed_password(self):
        self.create()
        user = get_user_model().objects.get(username="operatrice")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(list(user.groups.values_list("name", flat=True)), ["Opérateurs Studio"])
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertNotIn(self.password, self.output.getvalue())
        self.assertEqual(self.prompt.call_count, 2)

    def test_existing_user_is_never_granted_access_or_reset(self):
        old_password = secrets.token_urlsafe(32)
        user = get_user_model().objects.create_user("operatrice", password=old_password)
        with self.assertRaises(CommandError):
            self.create()
        self.prompt.assert_not_called()
        user.refresh_from_db()
        self.assertTrue(user.check_password(old_password))
        self.assertFalse(user.groups.exists())

    def test_rejects_invalid_name_without_prompting(self):
        with self.assertRaises(CommandError):
            self.create("nom incorrect")
        self.prompt.assert_not_called()

    def test_failed_confirmation_or_weak_password_creates_no_user(self):
        for answer in ((self.password, self.password[::-1]), ("1", "1")):
            with self.subTest(matching=answer[0] == answer[1]):
                self.prompt.side_effect = answer
                with self.assertRaises(CommandError):
                    self.create()
                self.assertFalse(get_user_model().objects.exists())

    def test_membership_failure_rolls_back_account_creation(self):
        with patch.object(Group.objects, "get_or_create", side_effect=IntegrityError):
            with self.assertRaises(CommandError):
                self.create()
        self.assertFalse(get_user_model().objects.exists())
