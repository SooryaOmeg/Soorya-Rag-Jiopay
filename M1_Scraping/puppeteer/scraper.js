import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";

console.log("Script starting...");

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}

// Helper sleep
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function scrapeFAQ(url, saveDir = "scraped_data") {
  console.log("scrapeFAQ function called with URL:", url);

  ensureDir(saveDir);
  const result = { faq: [] };

  console.log("Launching browser...");
  const browser = await puppeteer.launch({
    headless: false,
    slowMo: 200,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1366, height: 768 });

  try {
    console.log("Navigating to URL...");
    await page.goto(url, { waitUntil: "networkidle2" });
    await sleep(3000); // let dynamic content render

    // ✅ Grab FAQ toggles (should contain chevron icon)
    const toggles = await page.$$(
      "div[tabindex='0']:has(div.css-146c3p1.r-kb43wt)"
    );
    console.log(`Found ${toggles.length} FAQ toggles`);

    for (let i = 0; i < toggles.length; i++) {
      const toggle = toggles[i];

      try {
        // Extract question text
        const qEl = await toggle.$("div.css-146c3p1.r-op4f77:not(.r-kb43wt)");
        const question = qEl
          ? await page.evaluate((el) => el.innerText.trim(), qEl)
          : `Q${i + 1}`;
        console.log(`❓ Q${i + 1}: ${question}`);

        // Expand answer
        await toggle.click();
        await sleep(1200);

        // Extract answer
        const answer = await page.evaluate((toggleEl) => {
          const wrapper = toggleEl.parentElement?.parentElement?.parentElement;
          if (!wrapper) return "";
          const ans = wrapper.querySelector("div.css-146c3p1.r-1xt3ije");
          return ans ? ans.innerText.trim() : "";
        }, toggle);

        console.log(`✅ A: ${answer.substring(0, 100)}...\n`);

        result.faq.push({
          question,
          answer,
        });

        // Collapse again (optional)
        try {
          await toggle.click();
          await sleep(500);
        } catch (err) {
          // ignore collapse issues
        }
      } catch (error) {
        console.log(`⚠️ Error at toggle ${i + 1}: ${error.message}`);
      }
    }
  } catch (error) {
    console.error(`Error during scraping: ${error.message}`);
  } finally {
    await browser.close();
  }

  // Save JSON
  const jsonPath = path.join(saveDir, "faq_help.json");
  fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");

  console.log(`✅ Saved ${result.faq.length} Q&A to ${jsonPath}`);
  return result;
}

// Direct execution
console.log("About to call scrapeFAQ...");
const url = "https://jiopay.com/business/help-center";
scrapeFAQ(url).catch((error) => {
  console.error("Error occurred:", error);
});

console.log("Script setup complete.");
