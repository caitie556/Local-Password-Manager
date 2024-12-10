from cryptography.fernet import Fernet
from pathlib import Path
import random
import string

class PasswordManager:
    # format: (website, username) = encrypted password
    password_dict = {}
    encryption_key = Fernet.generate_key()

    def __init__(self) -> None:
        self.load_account_info()  

    # Have user set pin for the manager
    # Saves pin to password_dict temporarily
    # Args:
    #   plaintext_pin: int containing pin before encryption
    # Returns: 
    #   True if pin is saved in password_dict
    #   False otherwise
    def set_pin(self, plaintext_pin: int) -> bool:
        try:
            cipher = Fernet(self.encryption_key)
            encrypted_pin = cipher.encrypt(str(plaintext_pin).encode())
            self.password_dict[("pin", "pin")] = encrypted_pin
        except Exception as e:
            print("Pin save unsuccessfull") 
            return False
        return True   

    # Check pin for the manager
    # Args:
    #   plaintext_pin: str containing user entered pin
    # Returns: 
    #   True if pin matches saved pin
    #   False otherwise
    def check_pin(self, plaintext_pin: str) -> bool:
        try:
            if ('pin', 'pin') in self.password_dict.items():
                encrypted_pin = self.password_dict[('pin', 'pin')]
                cipher = Fernet(self.encryption_key)
                decrypted_pin = cipher.decrypt(encrypted_pin).decode()
                return decrypted_pin == plaintext_pin
            else:
                return self.set_pin(int(plaintext_pin))
        except Exception as e:
            print("Pin save unsuccessfull") 
            return False   

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
        
    # Gets the (website, username) pairs in the manager
    # Returns: 
    #   if password dict is not empty, returns list of (website, username)
    #   if password dict is empty, returns empty list
    def get_keys(self) -> list[(str, str)]:
        if len(self.password_dict) > 0:
            result = list(self.password_dict.keys())
            result.remove(('pin', 'pin'))
            return result
        else:
            return []
        
    # Generates a random password with varying strengths
    # Example:
    # 1 = 6 characters
    # 2 = 8 characters with atleast one lowercase, one uppercase and a number
    # 3 = 10 characters with atleast one lowercase, one uppercase, a number and special character
    # Args:
    #   strength: int corresponting with the desired strength of generated password
    # Returns: 
    #   String of generated password
    #   if key isnt found, return error message
    def generate_password(self, strength: int) -> str:
        try:
            generated_password = []
            if (strength >= 1):
                # Generate inital password of 6 chars for lovers level
                generated_password = [random.choice(string.ascii_letters) for _ in range(6)]
                if (strength >= 2):
                    # Generate an additional 2 characters for level 2
                    generated_password.append(random.choice(string.ascii_letters + string.digits))
                    generated_password.append(random.choice(string.ascii_letters + string.digits))
                    
                    # Generate random amount of uppercase letters
                    uppercase_desired = random.randint(1, 4)
                    # Add the desired amount of uppercases
                    for i in range(1, uppercase_desired):
                        index = random.randint(0, len(generated_password))
                        c = random.choice(string.ascii_uppercase)
                        generated_password.insert(index, c)
                            
                    # Generate random amount of lowercase letters
                    lowercase_desired = random.randint(1, 4)
                    # Add the desired amount of lowercases
                    for i in range(1, lowercase_desired):
                        index = random.randint(0, len(generated_password))
                        c = random.choice(string.ascii_lowercase)
                        generated_password.insert(index, c)

                    # Generate random amount of numbers
                    nums_desired = random.randint(1, 4)
                    # Add the desired amount of numbers
                    for i in range(1, nums_desired):
                        index = random.randint(0, len(generated_password))
                        num = random.choice(string.digits)
                        generated_password.insert(index, num)

                    if (strength >= 3):
                        # Generate an additional 2 characters for level 3
                        generated_password.append(random.choice(string.ascii_letters + string.digits))
                        generated_password.append(random.choice(string.ascii_letters + string.digits))

                        # Generate random amount of special characters
                        specials_desired = random.randint(1, 4)
                        special_chars = "~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/"
                        # Add the desired amount of special characters
                        for i in range(1, specials_desired):
                            index = random.randint(0, len(generated_password))
                            c = random.choice(special_chars)
                            generated_password.insert(index, c)
            return ''.join(generated_password)
        except Exception as e:
            return "Error: password not generated"

    # Saves password_dict to file
    def save_account_info(self):
        file = open("pswrds.txt", "wb")
        file.write(self.encryption_key + b'\n')
        for (website, username), encrypted_pass in self.password_dict.items():
            cipher = Fernet(self.encryption_key)
            encrypted_website = cipher.encrypt(website.encode('utf-8'))
            encrypted_username = cipher.encrypt(username.encode('utf-8'))
            concat_string = f"{encrypted_website},{encrypted_username},{encrypted_pass.decode('utf-8')}\n"
            file.write(concat_string.encode())

    # Load account information into password_dict from file
    def load_account_info(self):
        file_path = Path('pswrds.txt')
        if file_path.exists():
            with file_path.open('rb') as file:
                self.encryption_key = file.readline().strip()
                if (self.encryption_key == b''):
                        self.encryption_key = Fernet.generate_key()
                cipher = Fernet(self.encryption_key)
                lines = file.readlines()
                for line in lines:
                    line_str = line.decode('utf-8').strip()
                    params = line_str.strip().split(",")
                    encrypted_website = params[0][2:-1].encode('utf-8')
                    encrypted_username = params[1][2:-1].encode('utf-8')
                    encrypted_pass = params[2].encode('utf-8')
                    website = cipher.decrypt(encrypted_website).decode('utf-8')
                    username = cipher.decrypt(encrypted_username).decode('utf-8') 
                    self.password_dict[(website, username)] = encrypted_pass
            file.close()       

def main():
    manager = PasswordManager()
    # Perform user actions
    manager.set_pin(1234)
    manager.enter_account_info("Facebook.com", "user1", "123456")
    manager.enter_account_info("Facebook.com", "user2", "abcdef")
    
    #print(manager.get_password("Facebook.com", "user1"))
    #print(manager.get_password("Facebook.com", "user2"))
    #print(manager.check_pin('1234'))
    manager.save_account_info()
    #keys = manager.get_keys()
    #print(keys)

if __name__ == "__main__":
    main()