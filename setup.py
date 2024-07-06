import subprocess

user = subprocess.run(["whoami"],stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if user.stdout.strip() != "root":
	print("Please Run the setup as root")
	exit()

import sys
import os

def Install():
	import sqlite3
	print("[+] Installing IntelliCrypt...")
	
	result = subprocess.run(["apt","install","python3-pip","-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to Initialize pip")
		return False
	
	user = subprocess.run(["who","am","i"],stdout=subprocess.PIPE,text=True)
	user = user.stdout.split()[0].strip()
	
	result = subprocess.run(["sudo","-u",user,"pip","install","-r","requirements.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	print(result.stdout)
	print(result.stderr)
	if result.returncode != 0:
		print("[-] Error", "Failed to install required python libraries")
		return False
	result = subprocess.run(["pip","install","-r","requirements.txt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to install required python libraries")
		return False
	else:
		print("[+] Python libraries installed")
			
	if not os.path.isfile("/var/lib/IntelliCrypt/Intellicrypt.db"):
		result = subprocess.run(["mkdir","/var/lib/IntelliCrypt/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
		if result.returncode != 0:
			print("[-] Error", "Failed to create database")
			return False
		else:
			print("[+] Directory Initialized")
			
		result = subprocess.run(["touch","/var/lib/IntelliCrypt/Intellicrypt.db"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
		if result.returncode != 0:
			print("[-] Error", "Failed to create database")
			return False
		else:
			print("[+] Encryption Database Created")
			
		result = subprocess.run(["chmod","777", "/var/lib/IntelliCrypt/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
		if result.returncode != 0:
			print("[-] Error", "Failed to grant permissions")
			return False
		result = subprocess.run(["chmod","777", "/var/lib/IntelliCrypt/Intellicrypt.db"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
		if result.returncode != 0:
			print("[-] Error", "Failed to grant permissions")
			return False
		else:
			print("[+] Permissions Granted")
			
	conn = sqlite3.connect("/var/lib/IntelliCrypt/Intellicrypt.db")
	conn.execute("CREATE TABLE IF NOT EXISTS Auth_Table(UID VARCHAR(32) PRIMARY KEY, FileName VARCHAR(100), Password VARCHAR(128))")
	
	result = subprocess.run(["apt","install","ccrypt","-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to initialize ccrypt")
		return False
	else:
		print("[+] Initialized ccrypt")

	result = subprocess.run(["apt","install","cryptsetup","-y"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to initialize cryptsetup")
		return False
	else:
		print("[+] Initialized cryptsetup")
		
	result = subprocess.run(["find", "/home/","-name", "intellicrypt.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Could not find script ")
		return False
		
	path = result.stdout.strip()
	result = subprocess.run(["chmod","+x",path],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to Create Executable")
		return False
	else:
		print("[+] Created Executable")
		
	result = subprocess.run(["cp",path,"/usr/local/src/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to transfer source.")
		return False
		
	result = subprocess.run(["ln","-s","/usr/local/src/intellicrypt.py","/usr/local/bin/intellicrypt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to set up Symlink")
		return False
	else:
		print("[+] Set up Symlink")
		
	return True	

def Uninstall():
	print("[+] Uninstalling IntelliCrypt")
	if os.path.isfile("/var/lib/IntelliCrypt/Intellicrypt.db"):
		result = subprocess.run(["rm","-rf","/var/lib/IntelliCrypt/"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
		if result.returncode != 0:
			print("[-] Error", "Failed to delete database")
			return False
		else:
			print("[+] Removed Encryption Database.")

	result = subprocess.run(["rm","/usr/local/src/intellicrypt.py"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to remove source code.")
		return False
		
	result = subprocess.run(["rm","/usr/local/bin/intellicrypt"],stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
	if result.returncode != 0:
		print("[-] Error", "Failed to remove Symlink")
		return False
	else:
		print("[+] Removed Symlink")
		
	return True


if len(sys.argv) < 2 or sys.argv[1] == "install":
	if Install():
		print("[+] IntelliCrypt Installed Succesfully!\nUse the command \"intellicrypt\" to start using it.")
	else:
		print("[-] Installation Aborted!")

elif sys.argv[1] == "uninstall":
	confirmation = input("Warning! All Data in Files That Are Still Encrypted Will be Unrecoverable\n Do you Wish to Continue? (y/N): ")
	if confirmation.lower() == 'y':
		if Uninstall():
			print("[+] IntelliCrypt Uninstalled Successfully!")
		else:
			print("[-] Could not Uninstall the application!")   
else:
	print("Invalid option: Kindly read the documentaion: linktogithub")
