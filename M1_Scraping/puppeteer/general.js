import fs from "fs";
import path from "path";
import axios from "axios";
import puppeteer from "puppeteer";

// Ensure directory exists
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}

// Download file using axios
async function downloadFile(url, savePath) {
  try {
    const writer = fs.createWriteStream(savePath);
    const response = await axios({
      url,
      method: "GET",
      responseType: "stream",
      timeout: 30000,
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
      },
    });

    if (response.status === 200) {
      response.data.pipe(writer);
      await new Promise((resolve, reject) => {
        writer.on("finish", resolve);
        writer.on("error", reject);
      });
      console.log(`📥 Downloaded ${url} -> ${savePath}`);
    } else {
      console.log(`⚠️ Failed to download ${url} (status ${response.status})`);
    }
  } catch (error) {
    console.log(`❌ Error downloading ${url}: ${error.message}`);
  }
}

// Check if page is still valid and accessible
async function isPageAccessible(page) {
  try {
    if (!page || page.isClosed()) {
      return false;
    }
    await page.evaluate(() => document.readyState);
    return true;
  } catch (error) {
    return false;
  }
}

// Extract all data in one go to avoid context issues
async function extractAllData(page) {
  return await page.evaluate(() => {
    const result = {
      texts: [],
      images: [],
      pdfLinks: [],
    };

    // Extract texts
    try {
      const specificSelectors = ["div.css-146c3p1", "div.css-g5y9jx"];
      let textElements = [];

      specificSelectors.forEach((selector) => {
        const elements = document.querySelectorAll(selector);
        textElements.push(...Array.from(elements));
      });

      if (textElements.length > 0) {
        result.texts = textElements
          .map((el) => el.innerText?.trim())
          .filter(
            (txt) => txt && txt.toLowerCase() !== "loading" && txt.length > 3
          );
      } else {
        // Fallback to general selectors
        const fallbackSelectors = [
          "p",
          "h1",
          "h2",
          "h3",
          "h4",
          "h5",
          "h6",
          'div[class*="content"]',
          "main",
          "article",
        ];
        const allTexts = new Set();

        fallbackSelectors.forEach((selector) => {
          const elements = document.querySelectorAll(selector);
          elements.forEach((el) => {
            const text = el.innerText?.trim();
            if (
              text &&
              text.length > 10 &&
              !text.toLowerCase().includes("loading")
            ) {
              allTexts.add(text);
            }
          });
        });

        result.texts = Array.from(allTexts); // ✅ no limit
      }
    } catch (e) {
      console.log("Text extraction error in page context:", e.message);
    }

    // Extract images
    try {
      const imgElements = document.querySelectorAll("img");
      result.images = Array.from(imgElements)
        .map((img) => ({
          src: img.src || img.getAttribute("src"),
          alt: img.alt || img.getAttribute("alt") || "",
        }))
        .filter((img) => img.src);
    } catch (e) {
      console.log("Image extraction error in page context:", e.message);
    }

    // Extract PDF links
    try {
      const allLinks = [];

      const anchors = document.querySelectorAll("a");
      anchors.forEach((a) => {
        const href = a.href || a.getAttribute("href");
        if (href && href.toLowerCase().includes(".pdf")) {
          allLinks.push({
            href: href,
            text: a.innerText?.trim() || "PDF Document",
          });
        }
      });

      const allElements = document.querySelectorAll("*");
      allElements.forEach((el) => {
        const onclick = el.getAttribute("onclick") || "";
        const href = el.getAttribute("href") || "";

        [onclick, href].forEach((attr) => {
          if (attr && attr.includes(".pdf")) {
            const matches = attr.match(/(https?:\/\/[^\s'"]+\.pdf)/g);
            if (matches) {
              matches.forEach((match) => {
                allLinks.push({
                  href: match,
                  text: el.innerText?.trim() || "PDF Document",
                });
              });
            }
          }
        });
      });

      const uniqueLinks = allLinks.filter(
        (link, index, self) =>
          index === self.findIndex((l) => l.href === link.href)
      );

      result.pdfLinks = uniqueLinks;
    } catch (e) {
      console.log("PDF extraction error in page context:", e.message);
    }

    return result;
  });
}

// Main scraping function
async function scrapeAllTextImagesPdfs(url, saveDir = "scraped_data_general") {
  ensureDir(saveDir);
  const pdfDir = ensureDir(path.join(saveDir, "pdfs"));

  let browser;
  let page;

  try {
    browser = await puppeteer.launch({
      headless: false,
      slowMo: 100,
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
      defaultViewport: { width: 1280, height: 800 },
    });

    page = await browser.newPage();
    await page.setUserAgent(
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    );
    page.setDefaultTimeout(90000);
    page.setDefaultNavigationTimeout(90000);

    console.log(`🔗 Navigating to ${url}`);
    await page.goto(url, { waitUntil: ["domcontentloaded"], timeout: 60000 });
    await new Promise((resolve) => setTimeout(resolve, 3000));

    if (!(await isPageAccessible(page))) {
      throw new Error("Page inaccessible");
    }

    console.log("📊 Extracting all data...");
    let extractedData = await extractAllData(page);

    console.log(`📝 Extracted ${extractedData.texts.length} texts`);
    console.log(`🖼️ Extracted ${extractedData.images.length} images`);
    console.log(`📄 Extracted ${extractedData.pdfLinks.length} PDF links`);

    // Download PDFs
    for (const pdf of extractedData.pdfLinks) {
      try {
        const pdfUrl = pdf.href;
        const pdfName =
          path.basename(pdfUrl.split("?")[0]) || `pdf_${Date.now()}.pdf`;
        const pdfPath = path.join(pdfDir, pdfName);

        if (!fs.existsSync(pdfPath)) {
          await downloadFile(pdfUrl, pdfPath);
        }
      } catch (error) {
        console.log(`❌ Error downloading PDF ${pdf.href}: ${error.message}`);
      }
    }

    const pageName = url.replace(/^https?:\/\//, "").replace(/[\/\?#]/g, "_");
    const result = {
      url,
      timestamp: new Date().toISOString(),
      texts: extractedData.texts, // ✅ no limit
      images: extractedData.images,
      pdfs: extractedData.pdfLinks,
    };

    const jsonPath = path.join(saveDir, `scraped_${pageName}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");

    console.log(`✅ Saved: ${jsonPath}`);
    return result;
  } catch (error) {
    console.error(`❌ Error scraping ${url}: ${error.message}`);
    return { url, error: error.message, texts: [], images: [], pdfs: [] };
  } finally {
    if (page && !page.isClosed()) await page.close();
    if (browser) await browser.close();
  }
}

// Run
(async () => {
  const urls = [
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
  ];

  for (const url of urls) {
    await scrapeAllTextImagesPdfs(url);
  }
})();
