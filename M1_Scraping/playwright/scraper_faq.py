import os
import json
from playwright.sync_api import sync_playwright


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def scrape_faq(url, save_dir="scraped_data"):
    ensure_dir(save_dir)
    result = {"faq": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)  # headless=True for silent run
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(3000)  # let dynamic JS render

        # ✅ Only select real FAQ toggles (must contain chevron icon)
        toggles = page.query_selector_all(
            "div[tabindex='0']:has(div.css-146c3p1.r-kb43wt)"
        )
        print(f"Found {len(toggles)} FAQ toggles")
        # topics = page.query_selector_all("div.css-146c3p1.r-9daio6.r-8jdrp.r-1enofrn.r-1it3c9n")
        # # topic = topic.inner_text().strip() if topic else "General"
        # print(f"Topic: {topics}")
        topic_main = set()
        for i, toggle in enumerate(toggles, start=1):
            try:
                # Question text
                # q_el = toggle.query_selector("div.css-146c3p1.r-151f9q2")
                # topic = topics[i-1].inner_text().strip() if topics and len(topics) >= i else "General"
                # if topic in topic_main:
                #     print(f"⚠️ Skipping duplicate topic: {topic.inner_text().strip() if topic else 'N/A'}")
                #     continue
                # topic_main.add(topic)
                q_el = toggle.query_selector("div.css-146c3p1.r-op4f77:not(.r-kb43wt)")
                question = q_el.inner_text().strip() if q_el else f"Q{i}"
                print(f"❓Q{i}: {question}")

                # Expand answer
                toggle.click(force=True)
                page.wait_for_timeout(1200)

                # Extract answer
                ans_el = toggle.evaluate_handle(
                    """el => {
                        let wrapper = el.parentElement?.parentElement?.parentElement;
                        if (!wrapper) return "";
                        let ans = wrapper.querySelector("div.css-146c3p1.r-1xt3ije");
                        return ans ? ans.innerText : "";
                    }"""
                )
                answer = ans_el.json_value().strip() if ans_el else ""
                print(f"✅ A: {answer[:100]}...\n")

                result["faq"].append({"question": question, "answer": answer})

                # Collapse again (optional)
                try:
                    toggle.click(force=True)
                    page.wait_for_timeout(500)
                except:
                    pass

            except Exception as e:
                print(f"⚠️ Error at toggle {i}: {e}")

        browser.close()

    # Save JSON
    json_path = os.path.join(save_dir, "faq_help.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(result['faq'])} Q&A to {json_path}")
    return result


if __name__ == "__main__":
    url = "https://jiopay.com/business/help-center"
    scrape_faq(url)


