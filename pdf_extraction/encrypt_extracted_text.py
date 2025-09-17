from cryptography.fernet import Fernet

# Generate a key and save it for later decryption
key = Fernet.generate_key()
with open('secret.key', 'wb') as key_file:
    key_file.write(key)

# Read the extracted text
with open('extracted_text.txt', 'rb') as file:
    data = file.read()

# Encrypt the data
fernet = Fernet(key)
encrypted = fernet.encrypt(data)

# Save the encrypted data
with open('extracted_text_encrypted.txt', 'wb') as enc_file:
    enc_file.write(encrypted)
