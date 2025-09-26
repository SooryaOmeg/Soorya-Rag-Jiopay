import json

pdf_json = "merged_final.json"      # from PDFs
faq_json = "merged.json"      # from JSON1 + JSON2
output_file = "final.json"    # final big JSON

merged_data = []

# Load PDF JSON
with open(pdf_json, "r", encoding="utf-8") as f1:
    try:
        merged_data.extend(json.load(f1))
    except json.JSONDecodeError:
        print("⚠️ merged.json is empty or invalid, skipping.")

# Load FAQ/Other JSON
with open(faq_json, "r", encoding="utf-8") as f2:
    try:
        merged_data.extend(json.load(f2))
    except json.JSONDecodeError:
        print("⚠️ merges.json is empty or invalid, skipping.")

# Save final big JSON
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(merged_data, out, ensure_ascii=False, indent=4)

print(f"✅ Final merged JSON written to {output_file}")
