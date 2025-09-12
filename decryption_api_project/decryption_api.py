from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
import csv
import os

app = FastAPI(title="Decryption API", description="API to decrypt plant data using Jamar's Fernet code")

# --- Load key (same logic as Jamar's files) ---
def load_key(key_path="secret.key"):
    try:
        with open(key_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError("secret.key not found. Please generate it first.")

FERNET = Fernet(load_key())

# --- Models ---
class Message(BaseModel):
    encrypted: str

class DecryptedMessage(BaseModel):
    decrypted: str

# --- Endpoints ---

@app.post("/decrypt", response_model=DecryptedMessage)
def decrypt_message(msg: Message):
    try:
        decrypted = FERNET.decrypt(msg.encrypted.encode()).decode()
        return {"decrypted": decrypted}
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed. Invalid ciphertext or wrong key.")

@app.get("/decrypt-csv")
def decrypt_csv(input_csv: str, col_index: int = 1):
    """
    Decrypts a CSV file column and returns it inline.
    Example: GET /decrypt-csv?input_csv=Plant_Generation_Data_encrypted.csv&col_index=1
    """
    if not os.path.exists(input_csv):
        raise HTTPException(status_code=404, detail=f"CSV file {input_csv} not found")

    decrypted_rows = []
    with open(input_csv, "r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        decrypted_rows.append(header)
        for row in reader:
            if len(row) > col_index:
                try:
                    row[col_index] = FERNET.decrypt(row[col_index].encode()).decode()
                except Exception:
                    row[col_index] = "[DECRYPTION FAILED]"
            decrypted_rows.append(row)

    return {"rows": decrypted_rows}


from fastapi.responses import StreamingResponse  # make sure this import is at the top of the file

@app.get("/decrypt-csv-stream")
def decrypt_csv_stream(input_csv: str, col_index: int = 1):
    """
    Stream-decrypts a CSV column row by row and sends it back as a CSV download.
    This avoids infinite loading for big files.
    """
    if not os.path.exists(input_csv):
        raise HTTPException(status_code=404, detail=f"CSV file {input_csv} not found")

    def row_generator():
        with open(input_csv, "r", newline="", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            for row in reader:
                if len(row) > col_index:
                    try:
                        row[col_index] = FERNET.decrypt(row[col_index].encode()).decode()
                    except Exception:
                        row[col_index] = "[FAILED]"
                yield ",".join(row) + "\n"

    return StreamingResponse(row_generator(), media_type="text/csv")



@app.get("/decrypt-csv-paged")
def decrypt_csv_paged(input_csv: str, page: int = 1, page_size: int = 100):
    """
    Returns a portion (page) of the CSV instead of the entire file.
    Example:
    /decrypt-csv-paged?input_csv=Plant_Generation_Data_decrypted.csv&page=1&page_size=100
    """
    if not os.path.exists(input_csv):
        raise HTTPException(status_code=404, detail=f"CSV file {input_csv} not found")

    start = (page - 1) * page_size
    end = start + page_size

    rows = []
    with open(input_csv, "r", newline="", encoding="utf-8") as infile:
        reader = list(csv.reader(infile))
        header = reader[0]
        data_rows = reader[1:]

        for row in data_rows[start:end]:
            rows.append(row)

    return {
        "header": header,
        "rows": rows,
        "page": page,
        "page_size": page_size,
        "total_rows": len(data_rows)
    }
