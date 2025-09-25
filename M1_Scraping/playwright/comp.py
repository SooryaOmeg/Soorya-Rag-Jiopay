import os
import json
import glob

# Paths
raw_folder = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\puppeteer\scraped_data_final\scraped_data_q_and_a\scraped_data_general"
cleaned_file = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\playwright\scraped_data_playwright.json"

def count_tokens(text: str) -> int:
    # Simple whitespace-based token count
    return len(text.split())

# --- Load raw data (multiple JSON files) ---
raw_pages = []
for filepath in glob.glob(os.path.join(raw_folder, "*.json")):
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            raw_pages.append(data)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

# --- Load cleaned data (single JSON file, list of pages) ---
with open(cleaned_file, "r", encoding="utf-8") as f:
    cleaned_pages = json.load(f)

# --- Metrics ---
# Raw tokens (handle "texts": [..] format)
raw_tokens = 0
for page in raw_pages:
    if "texts" in page and isinstance(page["texts"], list):
        text = " ".join(page["texts"])
    else:
        text = page.get("text", "")
    raw_tokens += count_tokens(text)

# Cleaned tokens (already one "text" field)
cleaned_tokens = sum(count_tokens(page.get("text", "")) for page in cleaned_pages)

raw_pages_count = len(raw_pages)
cleaned_pages_count = len(cleaned_pages)

# Noise %
noise_pct = ((raw_tokens - cleaned_tokens) / raw_tokens * 100) if raw_tokens > 0 else 0

# Throughput
throughput = cleaned_tokens / cleaned_pages_count if cleaned_pages_count > 0 else 0

# Failures (%)
empty_pages = sum(1 for page in cleaned_pages if not page.get("text", "").strip())
failures_pct = (empty_pages / raw_pages_count * 100) if raw_pages_count > 0 else 0

# --- Print report ---
print("===== Evaluation Report =====")
print(f"# Pages (Raw): {raw_pages_count}")
print(f"# Pages (Cleaned): {cleaned_pages_count}")
print(f"# Tokens (Raw): {raw_tokens}")
print(f"# Tokens (Cleaned): {cleaned_tokens}")
print(f"Noise %: {noise_pct:.2f}%")
print(f"Throughput (tokens/page): {throughput:.2f}")
print(f"Failures %: {failures_pct:.2f}%")
