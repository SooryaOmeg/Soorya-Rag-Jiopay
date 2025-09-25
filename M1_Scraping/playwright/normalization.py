import os
import re
import json
from glob import glob

# Input & output folders
input_folder = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\playwright\scraped_data_final\scraped_data_general"
output_folder = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\playwright\scraped_data_cleaned"
os.makedirs(output_folder, exist_ok=True)

# Common boilerplate patterns (expandable)
BOILERPLATE = [
    "JioPay Business",
    "Products", "Partner Program", "Contact Us", "About Us",
    "Privacy Policy", "Terms & Conditions",
    "Help Center", "Investor Relations",
    "Complaint Resolution", "Grievance Redressal Policy",
    "Merchant Onboarding & KYC-AML Policy",
    "BillPay Terms & Conditions",
    "Jio Payment Solutions Limited",
]

# Regex for junk characters
JUNK_RE = re.compile(r"[]+|\s{2,}")

def clean_block(text: str) -> str:
    # Remove junk chars & collapse whitespace
    text = JUNK_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def is_boilerplate(text: str) -> bool:
    # Small fragments and menu/footer items are boilerplate
    if len(text) < 5:
        return True
    for bp in BOILERPLATE:
        if text.strip().startswith(bp) or text.strip() == bp:
            return True
    return False

def normalize_texts(texts):
    cleaned = []
    seen = set()
    for block in texts:
        if not isinstance(block, str):
            continue
        block = clean_block(block)
        if not block or is_boilerplate(block):
            continue
        if block in seen:
            continue
        seen.add(block)
        cleaned.append(block)
    return cleaned

# Process all JSON files
for file_path in glob(os.path.join(input_folder, "*.json")):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "texts" in data:
        data["texts"] = normalize_texts(data["texts"])

    # Save to new folder
    fname = os.path.basename(file_path)
    out_path = os.path.join(output_folder, fname)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Cleaned & saved {fname}")
