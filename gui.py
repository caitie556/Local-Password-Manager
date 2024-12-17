import tkinter as tk
from Password_Manager.password_manager import PasswordManager

# Main application
def show_frame(frame):
    frame.tkraise()

def check_pin():
    pin = pin_entry.get()
    if password_manager.check_pin(pin):
        error_label.config(text="")  # Clear any error message
        show_frame(home_frame)
    else:
        error_label.config(text="Incorrect PIN. Try again!")

def log_out():
    password_manager.save_account_info()
    show_frame(login_frame)

# Initialize the PasswordManager
password_manager = PasswordManager()

# Set up the root window
root = tk.Tk()
root.title("PIN Verification")
root.geometry("400x300")

# Create frames for the screens
login_frame = tk.Frame(root)
home_frame = tk.Frame(root)
generate_frame = tk.Frame(root)
add_account_frame = tk.Frame(root)

for frame in (login_frame, home_frame, generate_frame, add_account_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Login screen
login_label = tk.Label(login_frame, text="Enter PIN:")
login_label.pack(pady=10)

pin_entry = tk.Entry(login_frame, show="*")
pin_entry.pack(pady=5)

check_button = tk.Button(login_frame, text="Log in", command=check_pin)
check_button.pack(pady=5)

error_label = tk.Label(login_frame, text="", fg="red")
error_label.pack()

# Home screen
home_label = tk.Label(home_frame, text="Password Manager")
home_label.pack(pady=20)

generate_button = tk.Button(home_frame, text="Generate Password", command=lambda: show_frame(generate_frame))
generate_button.pack()

add_button = tk.Button(home_frame, text="Add Account", command=lambda: show_frame(add_account_frame))
add_button.pack()

logout_button = tk.Button(home_frame, text="Log Out", command=log_out)
logout_button.pack()

search_label = tk.Label(home_frame, text="Search Passwords")
search_label.pack()

def filter_accounts(event):
    # Clear existing account entries
    for widget in home_frame.winfo_children():
        if isinstance(widget, tk.Label) and widget not in [home_label, search_label]:
            widget.destroy()
        elif isinstance(widget, tk.Button) and widget not in [generate_button, add_button, logout_button]:
            widget.destroy()
    
    # Get the search term
    search_term = search_box.get().lower()

    keys = password_manager.get_keys()
    
    # Filter and recreate entries
    filtered_keys = [
        (website, username)
        for website, username in keys
        if search_term in website.lower() or search_term in username.lower()
    ]
    
    for website, username in filtered_keys:
        create_entry(website, username)

def create_entry(website, username):
    password = ""
    label = tk.Label(home_frame, text=f"Website: {website}, Username: {username}, Password: {password}")
    label.pack()

    is_password_visible = False

    def toggle_password():
        nonlocal is_password_visible
        if is_password_visible:
            # Hide the password
            label.config(text=f"Website: {website}, Username: {username}, Password: ")
            button.config(text="Show Password")
        else:
            # Show the password
            retrieved_password = password_manager.get_password(website, username)
            label.config(text=f"Website: {website}, Username: {username}, Password: {retrieved_password}")
            button.config(text="Hide Password")
        is_password_visible = not is_password_visible

    button = tk.Button(home_frame, text="Show Password", command=toggle_password)
    button.pack()

search_box = tk.Entry(home_frame)
search_box.bind("<KeyRelease>", filter_accounts)
search_box.pack()

keys = password_manager.get_keys()

for website, username in keys:
    create_entry(website, username)

# Generate Password screen
generated_password = ""

def generate_password(strength):
    global generated_password
    generated_password = password_manager.generate_password(strength)
    password_label.config(text=f"Generated Password: {generated_password}")    

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(generated_password)
    root.update()
    copy_status_label.config(text="Password copied!", fg="green")    


generate_label = tk.Label(generate_frame, text="Generate Password")
generate_label.pack(pady=10)

back_button = tk.Button(generate_frame, text="Back", command=lambda: show_frame(home_frame))
back_button.pack(pady=5)

level_one_button = tk.Button(generate_frame, text="Level 1: 6 characters", command=lambda: generate_password(1))
level_one_button.pack()

level_two_button = tk.Button(generate_frame, text="Level 2: 8 characters with atleast one lowercase, \none uppercase and a number", command=lambda: generate_password(2))
level_two_button.pack()

level_three_button = tk.Button(generate_frame, text="Level 3: 10 characters with atleast one lowercase, \none uppercase, a number and special character", command=lambda: generate_password(3))
level_three_button.pack()

password_label = tk.Label(generate_frame, text="Generated Password: ")
password_label.pack()

copy_button = tk.Button(generate_frame, text="Copy Password", command=copy_to_clipboard)
copy_button.pack()

copy_status_label = tk.Label(generate_frame, text="", fg="green")
copy_status_label.pack()

# Add account screen
def add_account():
    web = website_entry.get()
    user = user_entry.get()
    pswrd = pass_entry.get()
    if (password_manager.enter_account_info(web, user, pswrd)):
        status_label.config(text="Password successfully added", fg="green")

        create_entry(web, user)
    else:
        status_label.config(text="Password cannot be added", fg="red")

add_label = tk.Label(add_account_frame, text="Enter Account Information:")
add_label.pack(pady=10)

website_entry = tk.Entry(add_account_frame)
website_entry.pack(pady=5)

user_entry = tk.Entry(add_account_frame)
user_entry.pack(pady=5)

pass_entry = tk.Entry(add_account_frame, show="*")
pass_entry.pack(pady=5)

back_button = tk.Button(add_account_frame, text="Back", command=lambda: show_frame(home_frame))
back_button.pack(pady=5)

submit_add_button = tk.Button(add_account_frame, text="Add", command=add_account)
submit_add_button.pack(pady=5)

status_label = tk.Label(add_account_frame, text="")
status_label.pack()

# Show the login screen initially
show_frame(login_frame)

root.mainloop()
