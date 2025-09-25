# import json
# import os
# import fitz  # PyMuPDF

# pdf_folder = r"Data\pdf"   # folder containing PDFs
# output_file = "merged_final.json"

# # Load existing data if file exists, else start fresh
# if os.path.exists(output_file):
#     with open(output_file, "r", encoding="utf-8") as f:
#         try:
#             merged_data = json.load(f)
#         except json.JSONDecodeError:
#             merged_data = []
# else:
#     merged_data = []

# # Process PDFs
# for filename in os.listdir(pdf_folder):
#     if filename.lower().endswith(".pdf"):
#         pdf_path = os.path.join(pdf_folder, filename)
#         try:
#             doc = fitz.open(pdf_path)
#             text_content = ""
#             for page in doc:
#                 text_content += page.get_text("text") or ""
#             text_content = text_content.strip()
#             if text_content:
#                 merged_data.append({
#                     "url": filename,   # use original PDF name
#                     "text": text_content
#                 })
#             doc.close()
#         except Exception as e:
#             print(f"⚠️ Could not read {filename}: {e}")

# # Save updated JSON (append style)
# with open(output_file, "w", encoding="utf-8") as out:
#     json.dump(merged_data, out, ensure_ascii=False, indent=4)

# print(f"✅ Merged JSON updated in {output_file}")


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
