#!/usr/bin/env python3

from tkinter import Tk, Label, Button, Entry, Frame, filedialog, StringVar, Radiobutton, OptionMenu
from tkinter import  LEFT, RIGHT, CENTER, W, END, DISABLED
from tkinter import messagebox  # For pop-up messages
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf import pbkdf2
import subprocess
import sqlite3
import time
import hashlib
import threading
import sys

conn = sqlite3.connect("/var/lib/IntelliCrypt/Intellicrypt.db")
#conn.execute("CREATE TABLE IF NOT EXISTS Auth_Table(UID VARCHAR(32) PRIMARY KEY, FileName VARCHAR(100), Password VARCHAR(128))")
check_progress = 0
sys.stderr = object

def close_function(win):
	win.destroy()
	root.deiconify()
	
def throbber(msg):
	# Create the window
	window1 = Tk()
	window1.title("IntelliCrypt")
	window1.geometry("500x150")
	window1.resizable(False, False)

	# Label for displaying training progress
	num_periods = 1
	message = f"{msg} {'.' * num_periods}"
	label = Label(
		  window1,
		  text=message,
		  font=("Arial", 20, "bold"),
		  fg="navy",  # Set text color to navy
		  padx=10,  # Add internal padding (horizontal)
		  pady=50   # Add internal padding (vertical, top and bottom)
	  )
	label.pack(anchor=CENTER)  # Center the label

	def update_progress():
		global check_progress
		if check_progress == 1:
			window1.destroy()
			check_progress = 0
			return
		nonlocal num_periods, message  # Modify variables within the function

		num_periods = (num_periods + 1) % 6  # Ensures max of 5 periods
		message = f"{msg} {'.' * num_periods}{' '*(5-num_periods)}"
		label.config(text=message)
		window1.after(1000, update_progress)

	# Start animation
	update_progress()

	# Display the window and close automatically when the function exits
	window1.mainloop()


def encrypt_file_folder():
  #print("Encrypt File/Folder button clicked!")
  # Open a new window for file selection and password input
  encrypt_window = Tk()
  root.withdraw()
  encrypt_window.title("Encrypt File/Folder")

  # Function to check password match and empty fields
  def password_match():
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()
    check = conn.execute(f"Select UID from Auth_Table where password=\"{hashlib.sha3_512((password + selected_file.get()[selected_file.get().rfind('/')+1:]).encode()).hexdigest()}\"").fetchall()
    #check = conn.execute("Select * from Auth_Table").fetchall()
    #print("check",check)
    if not selected_file.get():
      messagebox.showinfo("Reminder", "Please select a file to encrypt!")
      return  # Exit the function if no file is selected
    elif not password:
      messagebox.showinfo("Reminder", "Please enter a password!")
    elif not confirm_password:
      messagebox.showinfo("Reminder", "Please confirm your password!")
      return  # Exit the function if confirm password is empty
    elif password != confirm_password:
      messagebox.showerror("Error", "Passwords don't match!")
    elif check != []:
    	messagebox.showerror("Error", "Please select a different password.")
    else:
      #print(f"Encrypting file: {selected_file.get()}")
      #print(f"Password: {password}")
      global check_progress
      #throb = threading.Thread(target=throbber, args = ("Encrypting Target",))
      #throb.start()
      UID = hashlib.md5(str(time.time()).encode()).hexdigest()
      key = hashlib.sha256((password + selected_file.get()[selected_file.get().rfind('/')+1:] + UID).encode()).hexdigest()
      kdf = pbkdf2.PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=selected_file.get()[selected_file.get().rfind('/')+1:].encode(),iterations=50000)
      key = kdf.derive(key.encode()).decode("iso-8859-1")
      #print("Key: ",key)
      password = hashlib.sha3_512((password + selected_file.get()[selected_file.get().rfind('/')+1:]).encode()).hexdigest()
      #print("check",check)
      #print(password)
      #print(key)
      try:
      	result = subprocess.run(["ccrypt","--encrypt","--recursive","--force",selected_file.get(),"--key",key,"--suffix",".encrypted"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      	conn.execute(f"Insert into Auth_Table values(\"{UID}\",\"{selected_file.get()[selected_file.get().rfind('/')+1:]}\",\"{password}\")")
      	conn.commit()
      except ValueError as ve:
      	messagebox.showerror("Error", "Files Not Encrypted. Please Try Again")
      if result.returncode != 0:
      	messagebox.showerror("Error", "Files Not Encrypted")
      else:
      	messagebox.showinfo("Success", "Encryption Completed Successfully!")
      
      #check_progress=1	
      # Close the window after successful encryption
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
    #print(selection_type.get())
    if selection_type.get() == "File":
      selected_path = filedialog.askopenfilename()
    elif selection_type.get() == "Folder":
      selected_path = filedialog.askdirectory()
    if selected_path:
      selected_file.set(selected_path)  # Update selected_file with path
      selected_file_entry.config(text=selected_path[selected_path.rfind("/")+1:])
      #selected_file_entry = Label(encrypt_window, text=selected_path[selected_path.rfind("\\"):])
      #selected_file_entry.grid(row=1, column=1, padx=5, pady=5)
    

  select_button = Button(encrypt_window, text="Browse", command=open_selection_dialog)
  select_button.grid(row=1, column=2, pady=5)  # Use grid layout

  # Variable to store the selected path
  selected_file = StringVar(encrypt_window)
  selected_file_entry = Label(encrypt_window, text="-Select-")
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
  close_button = Button(encrypt_window, text="Close", command=lambda: close_function(encrypt_window))
  close_button.grid(row=4, column=0, pady=10, sticky="W")  # Use grid layout with sticky for left alignment

  # Button to encrypt with validation (row 4)
  encrypt_button = Button(encrypt_window, text="Encrypt", command=password_match)
  encrypt_button.grid(row=4, column=2, pady=10, sticky="E")  # Use grid layout with sticky for right alignment
  
  encrypt_window.protocol('WM_DELETE_WINDOW', lambda arg=encrypt_window: close_function(arg))
  encrypt_window.mainloop()  # Run the inner window loop

def encrypt_drive():
	#https://www.cyberciti.biz/security/howto-linux-hard-disk-encryption-with-luks-cryptsetup-command/
	root.withdraw()
	#print("Encrypt Drive button clicked!")
	syscmd = subprocess.run(["sudo","lsblk","-o","NAME,VENDOR,MODEL"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	drives = [x.split()[1]+": "+x[x.rfind(" ")+1:] for x in syscmd.stdout.split("\n") if len(x.strip().split(" "))>1]
	ls1 = ["/dev/"+x.split()[0] for x in syscmd.stdout.split("\n") if len(x.strip().split(" "))>1]
	drives.pop(0)
	ls1.pop(0)
	drive_dict = dict(zip(drives,ls1))
	#print(drive_dict)
	
	def on_encrypt_click():
		selected_drive = drive_menu.get()
		password = password_entry.get()
		confirm_password = password_entry1.get()
		
		# Check if all fields are populated
		if not selected_drive:
			messagebox.showerror("Error", "Please select a drive to encrypt.")
		elif not password:
			messagebox.showerror("Error", "Please enter a password.")
		elif not confirm_password:
			messagebox.showerror("Error", "Please confirm the password.")
		elif password != confirm_password:
			messagebox.showerror("Error", "Passwords don't match.")
		else:
			confirmation = messagebox.askyesno("Warning!", "This will erase all data on the selected drive. \nDo you wish to continue?",icon="warning")
			if confirmation:
				global check_progress
				throb = threading.Thread(target=throbber, args = ("Encrypting Target",))
				throb.start()
				#print(f"Encrypting drive {selected_drive} with password {password}")
				with open("/tmp/icrypt_pass.txt","w") as File:
					File.write(password)
				
				#print("Password:", password)
				#print(["cryptsetup","luksFormat","--type","luks2","-q","--key-file","/tmp/icrypt_pass.txt",drive_dict[selected_drive]])
				result = subprocess.run(["cryptsetup","luksFormat","--type","luks2","-q","--key-file","/tmp/icrypt_pass.txt",drive_dict[selected_drive]],stdout = subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				#print(result.stdout)
				result = subprocess.run(["cryptsetup","luksOpen","-q","--key-file","/tmp/icrypt_pass.txt",drive_dict[selected_drive],"backup2"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				#print(result.stdout)
				result = subprocess.run(["mkfs.ext4","/dev/mapper/backup2"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				result = subprocess.run(["umount","/dev/mapper/backup2"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				# Clear password entry for security
				password_entry.delete(0, END)
				with open("/tmp/icrypt_pass.txt","w") as File:
					File.write(" ")
				result = subprocess.run(["rm","/tmp/icrypt_pass.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
				check_progress = 1
				window.destroy()
				root.deiconify()
				messagebox.showinfo("Success", "Device Encryption Successful!")
	
	# Create the main window
	window = Tk()
	window.title("Drive Encryption")
	
	# Increase window size and set padding
	window.geometry("400x200")  # Adjust width and height as desired
	window.grid()  # Add padding around all widgets in grid
  
  # Create widgets with grid layout
  # Drive selection
	drive_label = Label(window, text="Select Drive:")
	drive_label.grid(column=0, row=0, sticky=W)  # Left-align label
  
	drive_menu = StringVar(window)
	drive_menu.set(drives[0])  # Set default selection
  
	drive_dropdown = OptionMenu(window, drive_menu, *drives)
	drive_dropdown.grid(column=1, row=0, padx=10, pady=10)  # Add individual padding
  
  # Password entry
	password_label = Label(window, text="Password:")
	password_label.grid(column=0, row=1, sticky=W)  # Left-align label
  
	password_entry = Entry(window, show="*",width=25)  # Hide password characters
	password_entry.grid(column=1, row=1, padx=10, pady=10)  # Add individual padding
  
  #Confirm Password entry
	password_label1 = Label(window, text="Confirm Password:")
	password_label1.grid(column=0, row=2, sticky=W)  # Left-align label
  
	password_entry1 = Entry(window, show="*",width=25)  # Hide password characters
	password_entry1.grid(column=1, row=2, padx=10, pady=10)  # Add individual padding
  
  # Create the buttons
	close_button = Button(window, text="Close", command=lambda: close_function(window))
	close_button.grid(column=0, row=3, padx=10, pady=10)  # Add individual padding
  
	encrypt_button = Button(window, text="Encrypt", command=on_encrypt_click)
	encrypt_button.grid(column=1, row=3, padx=10, pady=10)  # Add individual padding
	
	window.protocol('WM_DELETE_WINDOW', lambda arg=window: close_function(arg))
  # Run the main event loop
	window.mainloop()

def decrypt_file_folder():
	#print("Decrypt File/Folder button clicked!")
	decrypt_window = Tk()
	root.withdraw()
	decrypt_window.title("Decrypt File/Folder")

  # Function to check password match and empty fields
	def password_match():
		password = password_entry.get()
		if selection_type.get() == "File":
			check = conn.execute(f"Select * from Auth_Table where FileName=\"{selected_file.get()[selected_file.get().rfind('/')+1:selected_file.get().rfind('.')]}\"").fetchall()
			password = hashlib.sha3_512((password + selected_file.get()[selected_file.get().rfind('/')+1:selected_file.get().rfind('.')]).encode()).hexdigest()
		else:
			check = conn.execute(f"Select * from Auth_Table where FileName=\"{selected_file.get()[selected_file.get().rfind('/')+1:]}\"").fetchall()
			password = hashlib.sha3_512((password + selected_file.get()[selected_file.get().rfind('/')+1:]).encode()).hexdigest()
    #check = conn.execute("Select * from Auth_Table").fetchall()
    #print("check",check)
		if not selected_file.get():
			messagebox.showinfo("Reminder", "Please select a file to Decrypt!")
			return  # Exit the function if no file is selected
		elif not password:
			messagebox.showinfo("Reminder", "Please enter the password!")
		elif check == []:
			messagebox.showerror("Error", "File not found in Database.")
		else:
			#throb = threading.Thread(target=throbber, args = ("Decrypting Target",))
			#throb.start()
			#print(f"Decrypting file: {selected_file.get()}")
			#print(f"Password: {password}")
      #password = hashlib.sha3_512((password + selected_file.get()[selected_file.get().rfind('/')+1:selected_file.get().rfind('.')]).encode()).hexdigest()
			#print(password)
      #print(check[1][2])
			for i in check:
				if password in i:
					key = hashlib.sha256((password_entry.get() + i[1] + i[0]).encode()).hexdigest()
					kdf = pbkdf2.PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=i[1].encode(),iterations=50000)
					key = kdf.derive(key.encode()).decode("iso-8859-1")
					result = subprocess.run(["ccrypt","--decrypt","--recursive","--force",selected_file.get(),"--key",key,"--suffix",".encrypted"],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
					if result.returncode != 0:
						messagebox.showerror("Error", "Files Not Decrypted")
						#check_progress = 1
					else:
						messagebox.showinfo("Success", "Decryption Completed Successfully!")
						#check_progress = 1
						conn.execute(f"Delete from Auth_Table where UID=\"{i[0]}\"")
						conn.commit()
						decrypt_window.destroy()
						root.deiconify()
				elif i == check[-1]:
					messagebox.showerror("Error", "Invalid Credentials")
      
	selection_type = StringVar(decrypt_window)
  # Label for file selection
	type_label = Label(decrypt_window, text="Select Type:")
	type_label.grid(row=0, column=0, pady=10)
  
	file_radio = Radiobutton(decrypt_window, text="File", variable=selection_type, value="File")
	file_radio.select()  # Select "File" by default
	file_radio.grid(row=0, column=1, padx=5, pady=10)

	folder_radio = Radiobutton(decrypt_window, text="Folder", variable=selection_type, value="Folder")
	folder_radio.grid(row=0, column=2, padx=5, pady=10)

  # Label for selection
	file_label = Label(decrypt_window, text="Select File/Folder:")
	file_label.grid(row=1, column=0, pady=10)  # Use grid layout
  
	selected_path=""

  # Button to open selection dialog
	def open_selection_dialog():
		#print(selection_type.get())
		if selection_type.get() == "File":
			selected_path = filedialog.askopenfilename()
		elif selection_type.get() == "Folder":
			selected_path = filedialog.askdirectory()
		if selected_path:
			selected_file_entry.config(text=selected_path[selected_path.rfind("/")+1:])
			selected_file.set(selected_path)  # Update selected_file with path
    

	select_button = Button(decrypt_window, text="Browse", command=open_selection_dialog)
	select_button.grid(row=1, column=2, pady=5)  # Use grid layout

  # Variable to store the selected path
	selected_file = StringVar(decrypt_window)
	selected_file_entry = Label(decrypt_window, text="-Select-")
	selected_file_entry.grid(row=1, column=1, padx=5, pady=5)  # Use grid layout with padding

  # Label for password (row 2)
	password_label = Label(decrypt_window, text="Password:")
	password_label.grid(row=2, column=0, pady=10)  # Use grid layout

  # Entry field for password (row 2)
	password_entry = Entry(decrypt_window, show="*")  # Hides characters for password
	password_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)  # Use grid layout with columnspan and padding

  # Button to close the window (row 4)
	close_button = Button(decrypt_window, text="Close", command=lambda: close_function(decrypt_window))
	close_button.grid(row=4, column=0, pady=10, sticky="W")  # Use grid layout with sticky for left alignment

  # Button to encrypt with validation (row 4)
	decrypt_button = Button(decrypt_window, text="Decrypt", command=password_match)
	decrypt_button.grid(row=4, column=2, pady=10, sticky="E")  # Use grid layout with sticky for right alignment
	
	decrypt_window.protocol('WM_DELETE_WINDOW', lambda arg=decrypt_window: close_function(arg))
	decrypt_window.mainloop()  # Run the inner window loop

def decrypt_drive():
	print("Decrypt Drive button clicked!")


user = subprocess.run(["whoami"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
#print(user.stdout)
# Create the main window
root = Tk()
root.title("IntelliCrypt")
root.geometry("500x300")

# Create the "IntelliCrypt" label
label = Label(root, text="Intelli-Crypt", font=("Arial", 30, "bold"), fg="navy")
label.pack(pady=20)

# Create the buttons
encrypt_file_folder_button = Button(root, text="Encrypt File/Folder", command=encrypt_file_folder)
encrypt_drive_button = Button(root, text="Encrypt Drive", command=encrypt_drive)
decrypt_file_folder_button = Button(root, text="Decrypt File/Folder", command=decrypt_file_folder)
#decrypt_drive_button = Button(root, text="Decrypt Drive", command=decrypt_drive)

# Center the buttons
button_width = 20
for button in (encrypt_file_folder_button, decrypt_file_folder_button, encrypt_drive_button): #, decrypt_drive_button):
  button.config(width=button_width)
  button.pack(pady=10)
  
if user.stdout.strip() != 'root':
	encrypt_drive_button["state"] = DISABLED
	label1 = Label(root, text="Run the application as root to encrypt drives", fg="red")
	label1.pack(pady=15)

# Run the main loop
root.mainloop()
