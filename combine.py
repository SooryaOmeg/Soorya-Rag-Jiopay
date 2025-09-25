import json

# File paths
file2 = r"Data\faq_help.json"
file1 = r"Data\scraped_data_playwright.json"
output_file = "merged.json"

HELP_CENTER_URL = "https://jiopay.com/business/help-center"

# Load JSON files
# Load json1
with open(file1, "r", encoding="utf-8") as f1:
    data1 = json.load(f1)

# Load json2 (it's a dict, not a list)
with open(file2, "r", encoding="utf-8") as f2:
    data2 = json.load(f2)

# Extract faq entries
faq_entries = []
if "faq" in data2:
    for item in data2["faq"]:
        question = item.get("question", "").strip()
        answer = item.get("answer", "").strip()
        combined_text = f"{question} {answer}".strip()
        faq_entries.append({
            "url": HELP_CENTER_URL,
            "text": combined_text
        })

# Merge both
merged_data = data1 + faq_entries

# Save result
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(merged_data, out, ensure_ascii=False, indent=4)

print(f"Merged JSON written to {output_file}")