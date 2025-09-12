import csv
from cryptography.fernet import Fernet

# --- Key Management ---
def generate_key(key_path='secret.key'):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as key_file:
        key_file.write(key)
    print(f"Key generated and saved to '{key_path}'. Keep this safe!")

def load_key(key_path='secret.key'):
    with open(key_path, 'rb') as key_file:
        return key_file.read()

# --- Encryption/Decryption ---
def encrypt_csv_column(input_csv, output_csv, key_path='secret.key', col_index=1):
    key = load_key(key_path)
    f = Fernet(key)
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if len(row) > col_index:
                original = row[col_index]
                encrypted = f.encrypt(original.encode()).decode()
                row[col_index] = encrypted
            writer.writerow(row)
    print(f"Encrypted CSV written to '{output_csv}' (column {col_index+1})")

def decrypt_csv_column(input_csv, output_csv, key_path='secret.key', col_index=1):
    key = load_key(key_path)
    f = Fernet(key)
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            if len(row) > col_index:
                encrypted = row[col_index]
                try:
                    decrypted = f.decrypt(encrypted.encode()).decode()
                except Exception:
                    decrypted = '[DECRYPTION FAILED]'
                row[col_index] = decrypted
            writer.writerow(row)
    print(f"Decrypted CSV written to '{output_csv}' (column {col_index+1})")

# --- Example Usage ---
if __name__ == "__main__":
    # Set your file paths
    input_csv = r"C:\Users\breya\AppData\Local\Temp\e19416a0-f212-4a57-97b2-d5fa67914fa0_Plant_Generation_Data.csv (1).zip.fa0\Plant_Generation_Data.csv"
    encrypted_csv = "Plant_Generation_Data_encrypted.csv"
    decrypted_csv = "Plant_Generation_Data_decrypted.csv"
    key_path = "secret.key"

    # 1. Generate key (run once)
    generate_key(key_path)

    # 2. Encrypt plant_id column (column 2, index 1)
    encrypt_csv_column(input_csv, encrypted_csv, key_path, col_index=1)

    # 3. Decrypt to verify
    decrypt_csv_column(encrypted_csv, decrypted_csv, key_path, col_index=1)
