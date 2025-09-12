
## Setup

1. Clone this project or unzip the files into a folder.
2. Open the folder
3. Create a virtual environment:

```bash
python -m venv venv
# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the API:
- On Linux/Mac:
```bash
./run.sh
```
- On Windows:
```bash
start.bat
```

6. Open the docs:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## VS Code Debugging

Use the `.vscode/launch.json` configuration to run/debug directly in VS Code.

## Endpoints

- `POST /decrypt` → Decrypts a single encrypted string.
- `GET /decrypt-csv?input_csv=<file>&col_index=1` → Decrypts a CSV column and returns it as JSON.

## Notes

- Ensure `secret.key` is present in the project root.
- Keep `secret.key` safe and never commit it to public repos.
