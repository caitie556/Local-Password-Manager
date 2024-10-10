import hashlib
import getpass

# format: (website, username) = hashed password
password_dict = {}

# Have user enter account information
# Saves information to password_dict temporarily
# Args:
#   website: string containing the website to look up
#   username: string containing the username to look up
#   plaintext_pass: string containing password before hash
# Returns: 
#   True if account information is saved in password_dict
#   False otherwise
def enter_account_info(website: str, username: str, plaintext_pass: str) -> bool:
    try:
        hashed_pass = hashlib.sha256(plaintext_pass.encode()).hexdigest()
        password_dict[(website, username)] = hashed_pass
    except Exception as e:
        print("Save unsuccessfull") 
        return False
    return True

# Checks the password for the account and username
# Args:
#   website: string containing the website to look up
#   username: string containing the username to look up
#   plaintext_pass: string containing password before hash
# Returns: 
#   True if passwords match
#   False if passwords don't match
def check_password(website: str, username: str, plaintext_pass: str) -> bool:
    return password_dict[(website, username)] == hashlib.sha256(plaintext_pass.encode()).hexdigest()


# Saves password_dict to file
def save_account_info():
    file = open("pswrds.txt", "w")
    keys = password_dict.keys()
    for tuple in keys:
        concat_string = tuple[0] + "," + tuple[1] + "," + password_dict[tuple] + "\n"
        file.write(concat_string)
    file.close()

# Load account information into password_dict from file
def load_account_info():
    file = open("pswrds.txt", "r")
    lines = file.readlines()
    for line in lines:
        params = line.strip().split(",")
        password_dict[(params[0], params[1])] = params[2]
    file.close()

def main():
    load_account_info()
    # Perform user actions

    save_account_info()

if __name__ == "__main__":
    main()