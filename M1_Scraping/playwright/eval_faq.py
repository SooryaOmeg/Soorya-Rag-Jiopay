import json
from transformers import GPT2TokenizerFast

# Path to your FAQ JSON
fpath = r"C:\Main Files\Soorya\7thSem\LLM_Prod\Exp2\M1_Scraping\puppeteer\scraped_data_final\scraped_data_q_and_a\faq_help.json"

# Load tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text):
    return len(tokenizer.encode(text))

print("========== Step 1: Loading JSON ==========")
with open(fpath, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded file: {fpath}")
print(f"Top-level type: {type(data).__name__}")

# ---------- Step 2: Explore keys ----------
if isinstance(data, dict):
    keys = list(data.keys())
    print(f"Top-level keys: {keys}")

# ---------- Step 3: Inspect 'faq' ----------
if isinstance(data, dict) and "faq" in data:
    faq_entries = data["faq"]
    print(f"\nFound 'faq' with {len(faq_entries)} entries")

    total_chars = 0
    total_words = 0
    total_tokens = 0

    for i, entry in enumerate(faq_entries):
        print(f"\n--- FAQ {i+1} ---")
        q = entry.get("question", "")
        a = entry.get("answer", "")

        print(f"Q: {q}")
        print(f"A: {a}")

        q_chars, q_words, q_tokens = len(q), len(q.split()), count_tokens(q)
        a_chars, a_words, a_tokens = len(a), len(a.split()), count_tokens(a)

        print(f"Question → chars: {q_chars}, words: {q_words}, tokens: {q_tokens}")
        print(f"Answer   → chars: {a_chars}, words: {a_words}, tokens: {a_tokens}")

        total_chars += q_chars + a_chars
        total_words += q_words + a_words
        total_tokens += q_tokens + a_tokens

    print("\n========== Aggregate for 'faq' ==========")
    print(f"Total characters: {total_chars}")
    print(f"Total words: {total_words}")
    print(f"Total GPT2 tokens: {total_tokens}")
