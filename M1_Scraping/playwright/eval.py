# import os
# import json
# from transformers import GPT2TokenizerFast

# # Root directory of your scraped data
# ROOT_DIR = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\playwright\scraped_data_final"

# # Directories to include
# TARGET_DIRS = [
#     os.path.join(ROOT_DIR, "scraped_data_general"),
#     os.path.join(ROOT_DIR, "scraped_data_q_and_a"),
# ]

# tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# def count_tokens(text):
#     return len(tokenizer.encode(text))

# pages = 0
# total_tokens = 0
# noise_tokens = 0
# failures = 0

# print("\n========== Per-File Report ==========")

# for directory in TARGET_DIRS:
#     for fname in os.listdir(directory):
#         if fname.endswith(".json"):
#             fpath = os.path.join(directory, fname)
#             try:
#                 with open(fpath, "r", encoding="utf-8") as f:
#                     data = json.load(f)

#                 pages += 1
#                 text_chunks = []

#                 # Handle dict or list
#                 if isinstance(data, dict):
#                     # Try multiple key names
#                     for key in ["headings", "content", "paragraphs", "question", "answer"]:
#                         if key in data:
#                             text_chunks.extend(data[key])
#                 elif isinstance(data, list):
#                     for d in data:
#                         for key in ["headings", "content", "paragraphs", "question", "answer"]:
#                             if key in d:
#                                 text_chunks.extend(d[key])

#                 text = " ".join(text_chunks).strip()
#                 tokens = count_tokens(text) if text else 0
#                 total_tokens += tokens

#                 # Simple noise heuristic
#                 if any(x in text for x in ["©", "Privacy", "Terms", "Disclaimer", "Cookie"]):
#                     noise_tokens += int(tokens * 0.1)

#                 print(f"✅ {fname}: {tokens} tokens extracted")

#             except Exception as e:
#                 failures += 1
#                 print(f"❌ Failed reading {fpath}: {e}")

# # Final summary
# noise_pct = (noise_tokens / total_tokens * 100) if total_tokens else 0
# failure_pct = (failures / pages * 100) if pages else 0

# print("\n========== Ingestion Report ==========")
# print(f"Total JSON files (pages): {pages}")
# print(f"Total tokens extracted: {total_tokens:,}")
# print(f"Approx Noise %: {noise_pct:.2f}%")
# print(f"Failures: {failures} ({failure_pct:.1f}% of pages)")

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




