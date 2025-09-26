import os
import json
from glob import glob
from transformers import GPT2TokenizerFast
from prettytable import PrettyTable

# ---------- Setup ----------
folder = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\puppeteer\scraped_data_general"

# Load tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
tokenizer.model_max_length = int(1e30)  # disable length check

# Function to count tokens safely
def count_tokens(text, fname, block_idx):
    try:
        return len(tokenizer.encode(text))
    except Exception as e:
        print(f"⚠️ Tokenization error in file '{fname}', block {block_idx}: {e}")
        print(f"Block preview: {text[:200]}...\n")
        return 0

# ---------- Process Files ----------
results = []

for file_path in glob(os.path.join(folder, "*.json")):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        continue

    total_chars = 0
    total_words = 0
    total_tokens = 0
    num_images = 0
    num_pdfs = 0

    # Process texts
    if isinstance(data, dict) and "texts" in data:
        texts = data["texts"]
        for i, block in enumerate(texts):
            if not isinstance(block, str):
                continue
            chars = len(block)
            words = len(block.split())
            tokens = count_tokens(block, os.path.basename(file_path), i)

            total_chars += chars
            total_words += words
            total_tokens += tokens

    # Process images
    if isinstance(data, dict) and "images" in data:
        num_images = len(data["images"])

    # Process pdfs
    if isinstance(data, dict) and "pdfs" in data:
        num_pdfs = len(data["pdfs"])

    results.append({
        "File": os.path.basename(file_path),
        "Chars": total_chars,
        "Words": total_words,
        "Tokens": total_tokens,
        "Images": num_images,
        "PDFs": num_pdfs
    })

# ---------- Final Table ----------
table = PrettyTable()
table.field_names = ["File", "Chars", "Words", "Tokens", "Images", "PDFs"]

for r in results:
    table.add_row([r["File"], r["Chars"], r["Words"], r["Tokens"], r["Images"], r["PDFs"]])

print(table)




