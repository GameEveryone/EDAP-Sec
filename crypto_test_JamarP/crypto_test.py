from cryptography.fernet import Fernet
def generate_key():
    """
    Generates a key and saves it into a file.
    You must keep this key secret! Anyone with this key can decrypt your data.
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print("Key generated and saved to 'secret.key'. Keep this safe!")

def load_key():
    """
    Loads the previously generated key from the 'secret.key' file.
    """
    return open("secret.key", "rb").read()

def encrypt_message(message):
    """
    Encrypts a message.
    """
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    print(f"\nOriginal Message: {message}")
    print(f"Encrypted (bytes): {encrypted_message}")
    # Save to a file to see it as a string
    with open("encrypted_message.txt", "wb") as encrypted_file:
        encrypted_file.write(encrypted_message)
    print("Encrypted message also saved to 'encrypted_message.txt'")
    return encrypted_message

def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message.
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    print(f"\nEncrypted Message (bytes): {encrypted_message}")
    print(f"Decrypted Message: {decrypted_message.decode()}")
    return decrypted_message.decode()

# --- MAIN EXECUTION FOR TESTING ---
if __name__ == "__main__":
    # First, we need a key. Run this once, then you can comment it out.
    generate_key()

    # The message we want to encrypt
    my_message = "This is my secret message for VS Code! 123 #$%"

    # Encrypt the message
    encrypted = encrypt_message(my_message)

    # Decrypt the message
    decrypted = decrypt_message(encrypted)