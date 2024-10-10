import unittest
from Password_Manager.password_manager import PasswordManager
# Run using python -m folder2.main from parent folder

class TestPasswordManager(unittest.TestCase):
    
    def setUp(self) -> None:
        self.pass_manager = PasswordManager()
        return super().setUp()

    def test_add_password(self):
        self.assertTrue(self.pass_manager.enter_account_info("Facebook.com", "user1", "123456"))

    def test_get_password(self):
        self.pass_manager.enter_account_info("Facebook.com", "user1", "123456")
        self.assertEqual(self.pass_manager.get_password("Facebook.com", "user1"), "123456")

if __name__ == "__main__":
    unittest.main()
