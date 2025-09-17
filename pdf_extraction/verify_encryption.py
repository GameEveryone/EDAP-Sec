from cryptography.fernet import Fernet

# Load the key
with open('secret.key', 'rb') as key_file:
    key = key_file.read()

# Read the encrypted data
with open('extracted_text_encrypted.txt', 'rb') as enc_file:
    encrypted = enc_file.read()

# Decrypt the data
fernet = Fernet(key)
decrypted = fernet.decrypt(encrypted)

# Print the decrypted data
print(decrypted.decode())
