// scraper_partner_faq.js
import fs from "fs";
import path from "path";
import puppeteer from "puppeteer";

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}

// Helper sleep function
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function scrapeFaq(url, saveDir = "scraped_data") {
  ensureDir(saveDir);
  const result = { faq: [] };

  const browser = await puppeteer.launch({
    headless: false, // set true for silent run
    slowMo: 200,
  });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded" });
  await sleep(3000);

  // Find all question toggles
  const toggles = await page.$$("div[tabindex='0']");
  console.log(`Found ${toggles.length} Q&A toggles`);

  for (let i = 0; i < toggles.length; i++) {
    const toggle = toggles[i];
    try {
      // Extract question text
      const qEl = await toggle.$("div.css-146c3p1.r-op4f77");
      const question = qEl
        ? (await page.evaluate((el) => el.innerText.trim(), qEl))
        : `Q${i + 1}`;
      console.log(`\n❓ Q${i + 1}: ${question}`);

      // Locate chevron inside this toggle
      const chevron = await toggle.$("div.css-146c3p1.r-kb43wt");
      if (!chevron) {
        console.log("⚠️ No chevron found, skipping");
        continue;
      }

      // Click chevron via JS
      await page.evaluate((el) => el.click(), chevron);
      await sleep(500);

      // Extract answer
      const answer = await page.evaluate((el) => {
        const wrapper = el.parentElement?.parentElement;
        if (!wrapper) return "";
        const ansBlock = wrapper.querySelector("div[data-testid='ViewTestId']");
        return ansBlock ? ansBlock.innerText.trim() : "";
      }, toggle);

      if (!answer) {
        console.log("⚠️ No answer extracted");
      } else {
        console.log(`✅ A: ${answer.slice(0, 100)}...\n`);
      }

      if (question !== `Q${i + 1}`) {
        result.faq.push({ question, answer });
      }

      // Collapse again
      try {
        await page.evaluate((el) => el.click(), chevron);
        await sleep(300);
      } catch (err) {
        // ignore
      }
    } catch (err) {
      console.log(`⚠️ Error at toggle ${i + 1}: ${err}`);
    }
  }

  await browser.close();

  // Save JSON
  const jsonPath = path.join(saveDir, "faq_combined.json");
  fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");

  console.log(`✅ Saved ${result.faq.length} Q&A to ${jsonPath}`);
  return result;
}

// Run directly
const url = "https://jiopay.com/business/partner-program";
scrapeFaq(url);
