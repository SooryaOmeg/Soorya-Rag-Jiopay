import os
import json
import re
import requests
from playwright.sync_api import sync_playwright


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def download_file(url, save_path):
    """Download a file from URL and save locally"""
    try:
        r = requests.get(url, stream=True, timeout=30)
        if r.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"📥 Downloaded {url} -> {save_path}")
        else:
            print(f"⚠️ Failed to download {url} (status {r.status_code})")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")


def scrape_all_text_images_pdfs(url, save_dir="scraped_data_general"):
    ensure_dir(save_dir)
    pdf_dir = ensure_dir(os.path.join(save_dir, "pdfs"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()

        # Load page fully
        page.goto(url, wait_until="networkidle", timeout=60000)

        # Extract text
        try:
            page.wait_for_selector("div.css-146c3p1, div.css-g5y9jx", timeout=5000)
            texts = page.locator("div.css-146c3p1, div.css-g5y9jx").all_inner_texts()
        except:
            texts = []

        # Extract images (src + alt)
        image_elements = page.locator("img")
        images = []
        for i in range(image_elements.count()):
            el = image_elements.nth(i)
            src = el.get_attribute("src")
            alt = el.get_attribute("alt")
            if src:
                images.append({"src": src, "alt": alt or ""})

        # Extract direct PDF links
        pdf_links = []
        pdf_elements = page.locator('a[href$=".pdf"]')
        for i in range(pdf_elements.count()):
            el = pdf_elements.nth(i)
            href = el.get_attribute("href")
            text = el.inner_text().strip()
            if href and href.lower().endswith(".pdf"):
                pdf_links.append({"href": href, "text": text})

        # ✅ Fixed: Fallback clickable divs (using evaluate instead of inner_text)
        possible_pdf_divs = page.locator("div")
        all_divs = possible_pdf_divs.all()
        for el in all_divs:
            text = (el.evaluate("el => el.innerText") or "").strip()
            onclick = el.get_attribute("onclick")
            href = el.get_attribute("href")

            candidate = None
            if href and ".pdf" in href:
                candidate = href
            elif onclick and ".pdf" in onclick:
                match = re.search(r"(https?://[^\s'\"]+\.pdf)", onclick)
                if match:
                    candidate = match.group(1)

            if candidate:
                pdf_links.append({"href": candidate, "text": text})

        browser.close()

    cleaned_texts = [t.strip() for t in texts if t.strip() and t.lower() != "loading"]

    # Download PDFs locally
    for pdf in pdf_links:
        pdf_url = pdf["href"]
        pdf_name = os.path.basename(pdf_url.split("?")[0])
        pdf_path = os.path.join(pdf_dir, pdf_name)
        if not os.path.exists(pdf_path):
            download_file(pdf_url, pdf_path)

    # Save JSON metadata
    page_name = url.split("//")[-1].replace("/", "_")
    result = {"url": url, "texts": cleaned_texts, "images": images, "pdfs": pdf_links}
    json_path = os.path.join(save_dir, f"all_text_images_pdfs_{page_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(
        f"✅ Extracted {len(cleaned_texts)} texts, {len(images)} images, {len(pdf_links)} PDFs -> saved at {json_path}"
    )
    return result


if __name__ == "__main__":
    urls = [
        "https://jiopay.com/business",
        "https://jiopay.com/business/partner-program",
        "https://jiopay.com/business/contact",
        "https://jiopay.com/business/about-us",
        "https://jiopay.com/business/paymentgateway",
        "https://jiopay.com/business/pointofsale",
        "https://jiopay.com/business/upi",
        "https://jiopay.com/business/biller",
        "https://jiopay.com/business/jio-pay-business",
        "https://jiopay.com/business/help-center",
        "https://jiopay.com/business/investor-relation",
        "https://jiopay.com/business/complaint-resolution-escalation-matrix",
        "https://jiopay.com/business/privacy-policy",
        "https://jiopay.com/business/terms-conditions",
        "https://jiopay.com/business/on-boarding-and-kyc-policy",
        "https://jiopay.com/business/billpay-terms-conditions",
        "https://jiopay.com/business/paymentgateway/1qr",
        "https://jiopay.com/business/paymentgateway/direct",
        "https://jiopay.com/business/paymentgateway/checkout",
        "https://jiopay.com/business/paymentgateway/vault",
        "https://jiopay.com/business/paymentgateway/collect",
        "https://jiopay.com/business/paymentgateway/repeat",
        "https://jiopay.com/business/paymentgateway/campaign",
        "https://jiopay.com/business/paymentgateway/console",
        "https://jiopay.com/business/increase-conversion",
        "https://jiopay.com/business/widen-presence",
        "https://jiopay.com/business/mitigate-risk",
        "https://jiopay.com/business/simplified-experience",
        
    ]
    for u in urls:
        data = scrape_all_text_images_pdfs(u)
        print(
            f"Extracted {len(data['texts'])} texts, {len(data['images'])} images, {len(data['pdfs'])} PDFs"
        )
