import unittest
from Password_Manager.password_manager import PasswordManager
# Run using python -m Tests.password_manager_tests from parent folder

class TestPasswordManager(unittest.TestCase):
    
    def setUp(self) -> None:
        self.pass_manager = PasswordManager()
        file = open("pswrds.txt", "w")
        file.close()
        return super().setUp()

    def test_add_password(self):
        self.assertTrue(self.pass_manager.enter_account_info("Facebook.com", "user1", "123456"))

    def test_get_password(self):
        self.pass_manager.enter_account_info("Facebook.com", "user1", "123456")
        self.assertEqual(self.pass_manager.get_password("Facebook.com", "user1"), "123456")

    def test_generate_password(self):
        genPass = self.pass_manager.generate_password(1)
        self.assertTrue(len(genPass) > 0)
        genPass = self.pass_manager.generate_password(2)
        self.assertTrue(len(genPass) > 0)
        genPass = self.pass_manager.generate_password(3)
        self.assertTrue(len(genPass) > 0)

    def test_set_pin(self):
        self.assertTrue(self.pass_manager.set_pin(1234))

    def test_check_pin(self):
        self.pass_manager.set_pin(1234)
        self.assertTrue(self.pass_manager.check_pin('1234'))
        self.assertFalse(self.pass_manager.check_pin('2345'))


if __name__ == "__main__":
    unittest.main()
