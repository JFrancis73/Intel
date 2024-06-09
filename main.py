from tkinter import Tk, Label, Button, Entry, Frame, filedialog, StringVar, Radiobutton
from tkinter import messagebox  # For pop-up messages
import subprocess

# Function definitions (to be replaced with actual encryption logic)
def encrypt_file_folder():
  print("Encrypt File/Folder button clicked!")
  # Open a new window for file selection and password input
  encrypt_window = Tk()
  root.withdraw()
  encrypt_window.title("Encrypt File/Folder")

  # Function to check password match and empty fields
  def password_match():
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    if not password:
      messagebox.showinfo("Reminder", "Please enter a password!")
      return  # Exit the function if password is empty
    elif not confirm_password:
      messagebox.showinfo("Reminder", "Please confirm your password!")
      return  # Exit the function if confirm password is empty
    elif password != confirm_password:
      messagebox.showerror("Error", "Passwords don't match!")
    elif not selected_file.get():
      messagebox.showinfo("Reminder", "Please select a file to encrypt!")
    else:
      # Add your encryption logic here using libraries like cryptography
      # Access selected file using selected_file.get() and password using password.get()
      print(f"Encrypting file: {selected_file.get()}")
      print(f"Password: {password}")
      result = subprocess.run(["ccrypt","--encrypt","--recursive","--force",selected_file.get(),"--key",password,"--suffix",".encrypted"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      if result.returncode != 0:
      	messagebox.showerror("Error", "Files Not Encrypted")
      else:
      	messagebox.showinfo("Success", " √ Folder has been Encrypted!")
      # Close the window after successful encryption (or handle errors)
      encrypt_window.destroy()
      root.deiconify()
  
  selection_type = StringVar(encrypt_window)
  # Label for file selection
  type_label = Label(encrypt_window, text="Select Type:")
  type_label.grid(row=0, column=0, pady=10)
  
  file_radio = Radiobutton(encrypt_window, text="File", variable=selection_type, value="File")
  file_radio.select()  # Select "File" by default
  file_radio.grid(row=0, column=1, padx=5, pady=10)

  folder_radio = Radiobutton(encrypt_window, text="Folder", variable=selection_type, value="Folder")
  folder_radio.grid(row=0, column=2, padx=5, pady=10)

  # Label for selection
  file_label = Label(encrypt_window, text="Select File/Folder:")
  file_label.grid(row=1, column=0, pady=10)  # Use grid layout
  
  selected_path=""

  # Button to open selection dialog
  def open_selection_dialog():
    print(selection_type.get())
    if selection_type.get() == "File":
      selected_path = filedialog.askopenfilename()
    elif selection_type.get() == "Folder":
      selected_path = filedialog.askdirectory()
    if selected_path:
      selected_file.set(selected_path)  # Update selected_file with path
    

  select_button = Button(encrypt_window, text="Browse", command=open_selection_dialog)
  select_button.grid(row=1, column=2, pady=5)  # Use grid layout

  # Variable to store the selected path
  selected_file = StringVar(encrypt_window)
  selected_file_entry = Label(encrypt_window, text=selected_path)
  selected_file_entry.grid(row=1, column=1, padx=5, pady=5)  # Use grid layout with padding

  # Label for password (row 2)
  password_label = Label(encrypt_window, text="Password:")
  password_label.grid(row=2, column=0, pady=10)  # Use grid layout

  # Entry field for password (row 2)
  password_entry = Entry(encrypt_window, show="*")  # Hides characters for password
  password_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)  # Use grid layout with columnspan and padding

  # Label for confirm password (row 3)
  confirm_password_label = Label(encrypt_window, text="Confirm Password:")
  confirm_password_label.grid(row=3, column=0, pady=10)  # Use grid layout

  # Entry field for confirm password (row 3)
  confirm_password_entry = Entry(encrypt_window, show="*")  # Hides characters for password
  confirm_password_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)  # Use grid layout with columnspan and padding

  # Button to close the window (row 4)
  close_button = Button(encrypt_window, text="Close", command=encrypt_window.destroy)
  close_button.grid(row=4, column=0, pady=10, sticky="W")  # Use grid layout with sticky for left alignment

  # Button to encrypt with validation (row 4)
  encrypt_button = Button(encrypt_window, text="Encrypt", command=password_match)
  encrypt_button.grid(row=4, column=2, pady=10, sticky="E")  # Use grid layout with sticky for right alignment

  encrypt_window.mainloop()  # Run the inner window loop

def encrypt_drive():
  print("Encrypt Drive button clicked!")

def decrypt_file_folder():
  print("Decrypt File/Folder button clicked!")

def decrypt_drive():
  print("Decrypt Drive button clicked!")


# Create the main window
root = Tk()
root.title("IntelliCrypt")
root.geometry("500x300")

# Create the "IntelliCrypt" label
label = Label(root, text="IntelliCrypt", font=("Arial", 30, "bold"), fg="navy")
label.pack(pady=20)

# Create the buttons
encrypt_file_folder_button = Button(root, text="Encrypt File/Folder", 
                                   command=encrypt_file_folder)
encrypt_drive_button = Button(root, text="Encrypt Drive", command=encrypt_drive)
decrypt_file_folder_button = Button(root, text="Decrypt File/Folder", 
                                   command=decrypt_file_folder)
decrypt_drive_button = Button(root, text="Decrypt Drive", command=decrypt_drive)

# Center the buttons
button_width = 20
for button in (encrypt_file_folder_button, encrypt_drive_button, 
                decrypt_file_folder_button, decrypt_drive_button):
  button.config(width=button_width)
  button.pack(pady=10)

# Run the main loop
root.mainloop()
