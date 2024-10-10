from cryptography.fernet import Fernet
from pathlib import Path

class PasswordManager:
    # format: (website, username) = hashed password
    password_dict = {}
    encryption_key = Fernet.generate_key()

    def __init__(self) -> None:
        self.load_account_info()        

    # Have user enter account information
    # Saves information to password_dict temporarily
    # Args:
    #   website: string containing the website to look up
    #   username: string containing the username to look up
    #   plaintext_pass: string containing password before encryption
    # Returns: 
    #   True if account information is saved in password_dict
    #   False otherwise
    def enter_account_info(self, website: str, username: str, plaintext_pass: str) -> bool:
        try:
            cipher = Fernet(self.encryption_key)
            encrypted_pass = cipher.encrypt(plaintext_pass.encode())
            self.password_dict[(website, username)] = encrypted_pass
        except Exception as e:
            print("Save unsuccessfull") 
            return False
        return True

    # Gets the password for the account and username
    # Args:
    #   website: string containing the website to look up
    #   username: string containing the username to look up
    # Returns: 
    #   String of plaintext password
    #   if key isnt found, return error message
    def get_password(self, website: str, username: str) -> str:
        try:
            encrypted_pass = self.password_dict[(website, username)]
            cipher = Fernet(self.encryption_key)
            decrypted_password = cipher.decrypt(encrypted_pass).decode()
            return decrypted_password
        except Exception as e:
            return "Error: (" + website + ", " + username + ") not found"

    # Saves password_dict to file
    def save_account_info(self):
        file = open("pswrds.txt", "w")
        keys = self.password_dict.keys()
        for tuple in keys:
            concat_string = tuple[0] + "," + tuple[1] + "," + self.password_dict[tuple].decode('utf-8') + "\n"
            file.write(concat_string)
        file.close()

    # Load account information into password_dict from file
    def load_account_info(self):
        file_path = Path('pswrds.txt')
        if file_path.exists():
            with file_path.open('r') as file:
                lines = file.readlines()
                for line in lines:
                    params = line.strip().split(",")
                    self.password_dict[(params[0], params[1])] = params[2]
                file.close()
        else:
            print("File does not exist.")        

'''
def main():
    manager = PasswordManager()
    # Perform user actions
    manager.enter_account_info("Facebook.com", "user1", "123456")
    #manager.enter_account_info("Facebook.com", "user2", "abcdef")
    print(manager.get_password("Facebook.com", "user1"))
    manager.save_account_info()

if __name__ == "__main__":
    main()
'''