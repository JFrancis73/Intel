<div align="center">

   ![IntelliCrypt](https://github.com/user-attachments/assets/5aad5a92-5089-4dd0-953f-67338bdf47e6)

[![Version](https://img.shields.io/badge/version-1.5-blue.svg)](https://github.com/JFrancis73/intellicrypt/releases/tag/v1.5)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
</div>

# Secure Your Data with Intellicrypt

Intellicrypt offers a unique approach to data encryption, prioritizing confidentiality with a multi-layered defense system. Here's a breakdown of the key features of its encryption model:

*Zero-Knowledge Encryption:*

  Follows a zero-knowledge model, keeping the encryption key completely separate from the encrypted files.
  User password is never stored in the files themselves, significantly enhancing security.
  Even if an attacker steals an encrypted file, they cannot decrypt it without the additional information stored securely elsewhere.

*"Fort Knox" Defense with Tamper-Evident Protection:*

  Implements a "Fort Knox" defense mechanism that detects any unauthorized modification attempts made to the encrypted files or the database containing key derivation information.
  Triggers a "scorched earth" protocol by overwriting the data with garbage values if tampering is detected. This ensures data confidentiality even if an attacker breaches some security layers.

*Configurable Security with Balanced Approach:*

  Offers a configuration option to balance the "Fort Knox" defense and potential data loss.
        Default: "Scorched earth" on tamper attempt (maximum security but risk of data loss).
        Optional: Refuses decryption with incorrect key (prevents data loss but at the cost of a potential breach in confidentiality).
  Allows users to choose the level of risk they're comfortable with.

*Database as Central Management:*

  Stores authentication information and key derivation data in a secure database thereby requiring the users to have access to the database to even attempt to decrypt the files which further helps in mitigating unautorized access.

*Honeypot Potential:*

  Encrypted files can act as honeypots.
  Data destruction triggered by tampering attempts alerts users to potential security breaches.

Note: The "Scorched-Earth" protocol is restricted to the encryption and decryption of single files as of version 1.5 in order to minimize data loss.

**See it in Action**

Before diving in, get a quick glimpse of Intellicrypt's capabilities through a video demonstration:



https://github.com/JFrancis73/Intel/assets/108940466/34721026-4de1-4ee8-b670-26fc147993ec



# Installation

Getting started with Intellicrypt is a breeze! Choose your preferred installation method:

**Clone the repository:**

    git clone https://github.com/JFrancis73/Intel
    cd Intel/

**1. Assisted Installation (Recommended):**

If you're using a Debian-based Linux distribution (like Ubuntu or Kali) that uses the apt package manager, you can leverage the included setup script. The installer will handle all configurations and install the required dependencies.

Simply run the following command in your terminal:

    sudo python3 setup.py install

**2. Manual Installation:**

If you're not using a Debian-based distro or encounter issues with the setup script, you can still run Intellicrypt manually. Here's what you'll need to do:

*A. Modifying the Database Path (Optional):*

By default, Intellicrypt expects the database to be located at /var/lib/IntelliCrypt/Intellicrypt.db. If you prefer a different location, you can modify the path directly within the intellicrypt.py file. Edit line 15 to reflect your desired database path.

*B. Manual Database Setup:*

Alternatively, you can create the necessary directory structure and copy the database file:

Create the directory:

    sudo mkdir /var/lib/IntelliCrypt/

Set appropriate permissions:

    sudo chmod 777 /var/lib/IntelliCrypt/

Copy the database file:

    sudo cp Intellicrypt.db /var/lib/IntelliCrypt/

Set permissions for the database file:

    sudo chmod 777 /var/lib/IntelliCrypt/Intellicrypt.db

**Installing Python Libraries:**

Intellicrypt only relies on built-in Python libraries. However, to ensure their presence and update them if necessary, you can run:

    pip install -r requirements.txt

**Installing Linux Dependencies:**

Finally, install the required Linux dependencies using your package manager (apt in this example):

    sudo apt update
    sudo apt install ccrypt -y
    sudo apt install cryptsetup -y

Once you've completed these steps based on your preferred installation method, Intellicrypt should be ready to use!

# Usage

If you did the assisted install, you can use the tool simply by typing:

    intellicrypt

If you did the manual install, you can run:

    python3 intellicrypt.py

Note: You will have to run the tool as root if you intend to encrypt drives with it.

Once you launch it, just choose your preffered action and the intuitive GUI will prompt you for all the required information and the application will handle the rest.
Here are a few examples of what using the tool is like:

<div align="center">
	
![icrypt0](https://github.com/JFrancis73/Intel/assets/108940466/669d979e-cae9-44ab-bc4a-34b083b46df5)


**Encrypting Files/Folders:**


![icrypt1](https://github.com/JFrancis73/Intel/assets/108940466/12ef839e-9ade-48af-a0e3-cfacd6429b55)![icrypt2](https://github.com/JFrancis73/Intel/assets/108940466/b361e9b1-ca25-4803-96cb-6eb36956deaf)


**Decrypting Files/Folders:**


![icrypt3](https://github.com/JFrancis73/Intel/assets/108940466/65f656f3-6621-4a9f-88c8-69552aeb28f5)![icrypt4](https://github.com/JFrancis73/Intel/assets/108940466/50334766-b8ea-47b5-9098-0ecd5fff422e)


**Encrypting Drives:**


![icrypt5](https://github.com/JFrancis73/Intel/assets/108940466/b2bb875d-eb48-4d26-a0ac-bb1d5f62f7fe)

</div>

# Uninstalling Intellicrypt

If you no longer need Intellicrypt, you can uninstall it using the included setup.py:
	Just run the following command:
 
	sudo python setup.py uninstall
	
Note: If you uninstall the application, the data on files that are still encrypted by it will not be recoverable. Make sure you decrypt all your required files prior to uninstalling the application.

## MIT License

Copyright 2024 JFrancis73

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

