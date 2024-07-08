# IntelliCrypt
**Secure Your Data with Intellicrypt**

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

Note: It is important and a reccomended practice to have multiple copies of important data across different devices with at least one offsite.

**See it in Action**

Before diving in, get a quick glimpse of Intellicrypt's capabilities through a video demonstration:

**Installation**

Getting started with Intellicrypt is a breeze! Choose your preferred installation method:

Clone the repository:

    git clone https://github.com/JFrancis73/Intel
    cd Intel/

1. Assisted Installation (Recommended):

If you're using a Debian-based Linux distribution (like Ubuntu or Kali) that uses the apt package manager, you can leverage the included setup script. The installer will handle all configurations and install the required dependencies.

Simply run the following command in your terminal:

    sudo python3 setup.py install

2. Manual Installation:

If you're not using a Debian-based distro or encounter issues with the setup script, you can still run Intellicrypt manually. Here's what you'll need to do:

A. Modifying the Database Path (Optional):

By default, Intellicrypt expects the database to be located at /var/lib/IntelliCrypt/Intellicrypt.db. If you prefer a different location, you can modify the path directly within the intellicrypt.py file. Edit line 15 to reflect your desired database path.

B. Manual Database Setup:

Alternatively, you can create the necessary directory structure and copy the database file:

Create the directory:

    sudo mkdir /var/lib/IntelliCrypt/

Set appropriate permissions:

    sudo chmod 777 /var/lib/IntelliCrypt/

Copy the database file:

    sudo cp Intellicrypt.db /var/lib/IntelliCrypt/

Set permissions for the database file:

    sudo chmod 777 /var/lib/IntelliCrypt/Intellicrypt.db

Installing Python Libraries:

Intellicrypt only relies on built-in Python libraries. However, to ensure their presence and update them if necessary, you can run:

    pip install -r requirements.txt

Installing Linux Dependencies:

Finally, install the required Linux dependencies using your package manager (apt in this example):

    sudo apt update
    sudo apt install ccrypt -y
    sudo apt install cryptsetup -y

Once you've completed these steps based on your preferred installation method, Intellicrypt should be ready to use!

**Usage**

If you did the assisted install, you can use the tool simply by typing:

    intellicrypt

If you did the manual install, you can run:

    python3 intellicrypt.py

Note: You will have to run the tool as root if you intend to encrypt drives with it.

Once you launch it, just choose your preffered action and the intuitive GUI will prompt you for all the required information and the application will handle the rest.
Here are a few examples of what using the tool is like:

**Uninstalling Intellicrypt**

If you no longer need Intellicrypt, you can uninstall it using the included setup.py:
	Just run the following command:
 
	sudo python setup.py uninstall
	
Note: If you uninstall the application, the data on files that are still encrypted by it will not be recoverable. Make sure you decrypt all your required files prior to uninstalling the application.
