import tabula
import pandas as pd
import os

# Define the path to your PDF file
pdf_path = "Plant Generation Dataaaaa.pdf"

# Check if the file exists
if not os.path.isfile(pdf_path):
    print(f"❌ Error: The file '{pdf_path}' was not found. Please make sure it's in the same folder as this script.")
    exit()

print(f"Found '{pdf_path}'. Starting extraction...")

# Method 1: Extract all tables into a list of DataFrames
print("\n1. Extracting all tables from the PDF...")
try:
    # 'pages' can be set to 'all' or a specific number/range like '1-3'
    list_of_dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True)
    
    print(f"✅ Successfully found {len(list_of_dfs)} potential table(s).")

    # Save each extracted table to a separate CSV file
    for i, df in enumerate(list_of_dfs):
        output_filename = f"extracted_table_{i+1}.csv"
        df.to_csv(output_filename, index=False)
        print(f"   - Saved table {i+1} to '{output_filename}'")
        print(f"     Shape: {df.shape} (rows, columns)")
        print(f"     Columns: {list(df.columns)}")
        print()

    # Let's display the first table to preview the data
    if list_of_dfs:
        print("Preview of the first extracted table:")
        print(list_of_dfs[0].head(10)) # Show first 10 rows

except Exception as e:
    print(f"❌ An error occurred during extraction: {e}")

# Method 2: Try to extract all content at once into a single CSV (often useful)
print("\n2. Attempting to extract all content into a single file...")
try:
    tabula.convert_into(pdf_path, "all_data.csv", output_format="csv", pages='all')
    print("✅ Also saved all content to 'all_data.csv'")
except Exception as e:
    print(f"   - Could not create single file: {e}")

print("\n Extraction process complete! Please check the CSV files.")