
from cryptography.fernet import Fernet
import os
import pdfplumber

# Step 1: Extract text from PDF
pdf_path = 'Copy_of_Untitled_Report.pdf'
extracted_text_path = 'extracted_text.txt'

if os.path.exists(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    with open(extracted_text_path, 'w', encoding='utf-8') as f:
        f.write(text)
else:
    print(f'PDF file {pdf_path} not found. Skipping extraction.')

# Step 2: Encrypt the extracted text
if not os.path.exists('secret.key'):
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
else:
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()

with open(extracted_text_path, 'rb') as file:
    data = file.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)
with open('extracted_text_encrypted.txt', 'wb') as enc_file:
    enc_file.write(encrypted)

# Step 3: Verify encryption by decrypting and comparing
with open('extracted_text_encrypted.txt', 'rb') as enc_file:
    encrypted_data = enc_file.read()
decrypted = fernet.decrypt(encrypted_data)

if decrypted == data:
    print('Verification successful: Decrypted data matches original.')
else:
    print('Verification failed: Decrypted data does not match original.')
