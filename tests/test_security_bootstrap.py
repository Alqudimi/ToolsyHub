import unittest

from security import AdminBootstrapError, require_admin_password


class TestAdminBootstrap(unittest.TestCase):
    def test_returns_configured_password(self) -> None:
        self.assertEqual(
            require_admin_password({"ADMIN_PASSWORD": "a-long-unique-secret"}),
            "a-long-unique-secret",
        )

    def test_missing_password_fails_closed(self) -> None:
        with self.assertRaises(AdminBootstrapError):
            require_admin_password({})

    def test_empty_password_fails_closed(self) -> None:
        with self.assertRaises(AdminBootstrapError):
            require_admin_password({"ADMIN_PASSWORD": "   "})


if __name__ == "__main__":
    unittest.main()
