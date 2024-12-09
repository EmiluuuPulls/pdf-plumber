import re
import pdfplumber
import sys
import io

# Replacing sys.stdout with an encoding-compatible version
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Open the PDF and extract text
pdf_file = "sample.pdf"
with pdfplumber.open(pdf_file) as pdf:
    text = ""
    for page in pdf.pages:
        # Append text from each page, remove excessive spaces/newlines
        text += page.extract_text()

# Clean up the text (optional)
text = text.replace("\n", " ").replace("\r", " ").strip()

# Regular expressions to extract data
patterns = {
    'consumption': r'CONSUM\sGAZE\sNATURALE\s\(kWh\)\s?([\d,]+)',  # Specific to the "CONSUM GAZE NATURALE" phrase
    'total_amount': r'TOTAL\sDE\sPLATĂ\sCU\sT\.V\.A\.\s([\d,]+)\sLEI',  # Looking for Total amount (with LEI)
    'due_date': r'DATA\sSCADENTĂ\s([\d\.]+)',  # Capturing Due date
    'account_status_date': r'SITUAȚIA\sCONTELOUI\sLA\sDATA\sDE\s([\d\.]+)',  # Capturing Account status date
    'billing_period': r'PERIOADA\sDE\sFACTURARE\s([\d\.]+)\s-\s([\d\.]+)',  # Billing period range
}

# Extract data using the regular expressions
extracted_info = {}

for key, pattern in patterns.items():
    match = re.search(pattern, text)
    if match:
        # If a match is found, store the corresponding group(s)
        extracted_info[key] = match.groups() if len(match.groups()) > 1 else match.group(1)

# Display the extracted information
if extracted_info:
    print(f"Consumption (kWh): {extracted_info.get('consumption')}")
    print(f"Total amount (LEI): {extracted_info.get('total_amount')}")
    print(f"Due date: {extracted_info.get('due_date')}")
    print(f"Account status date: {extracted_info.get('account_status_date')}")
else:
    print("No match found.")
