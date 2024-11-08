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

for frame in (login_frame, home_frame):
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

logout_button = tk.Button(home_frame, text="Log Out", command=log_out)
logout_button.pack()

# Show the login screen initially
show_frame(login_frame)

root.mainloop()
