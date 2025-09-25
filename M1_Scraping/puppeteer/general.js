// import fs from "fs";
// import path from "path";
// import axios from "axios";
// import puppeteer from "puppeteer";

// // Ensure directory exists
// function ensureDir(dirPath) {
//   if (!fs.existsSync(dirPath)) {
//     fs.mkdirSync(dirPath, { recursive: true });
//   }
//   return dirPath;
// }

// // Download file using axios
// async function downloadFile(url, savePath) {
//   try {
//     const writer = fs.createWriteStream(savePath);
//     const response = await axios({
//       url,
//       method: "GET",
//       responseType: "stream",
//       timeout: 30000,
//     });

//     if (response.status === 200) {
//       response.data.pipe(writer);
//       await new Promise((resolve, reject) => {
//         writer.on("finish", resolve);
//         writer.on("error", reject);
//       });
//       console.log(`📥 Downloaded ${url} -> ${savePath}`);
//     } else {
//       console.log(`⚠️ Failed to download ${url} (status ${response.status})`);
//     }
//   } catch (error) {
//     console.log(`❌ Error downloading ${url}: ${error.message}`);
//   }
// }

// // Main scraping function
// async function scrapeAllTextImagesPdfs(url, saveDir = "scraped_data_general") {
//   ensureDir(saveDir);
//   const pdfDir = ensureDir(path.join(saveDir, "pdfs"));

//   const browser = await puppeteer.launch({
//     headless: false,
//     slowMo: 100,
//     args: ["--no-sandbox", "--disable-setuid-sandbox"],
//   });

//   const page = await browser.newPage();

//   try {
//     console.log(`🔗 Navigating to ${url}`);
//     await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });

//     // Wait until at least one of the target elements is present
//     try {
//       await page.waitForSelector("div.css-146c3p1, div.css-g5y9jx", {
//         timeout: 10000,
//       });
//     } catch (e) {
//       console.log("⚠️ Target text elements did not appear within 10s");
//     }

//     // Extract texts
//     let texts = [];
//     try {
//       const textElements = await page.$$("div.css-146c3p1, div.css-g5y9jx");
//       if (textElements.length > 0) {
//         texts = await page.$$eval("div.css-146c3p1, div.css-g5y9jx", (els) =>
//           els
//             .map((el) => el.innerText.trim())
//             .filter((txt) => txt && txt.toLowerCase() !== "loading")
//         );
//       } else {
//         console.log("⚠️ No text elements found");
//       }
//     } catch (err) {
//       console.log(`⚠️ Error extracting texts: ${err.message}`);
//     }

//     // Extract images
//     let images = [];
//     try {
//       const imgElements = await page.$$("img");
//       for (const img of imgElements) {
//         const src = await img.evaluate((el) => el.getAttribute("src"));
//         const alt = await img.evaluate((el) => el.getAttribute("alt") || "");
//         if (src) {
//           images.push({ src, alt });
//         }
//       }
//     } catch (err) {
//       console.log(`⚠️ Error extracting images: ${err.message}`);
//     }

//     // Extract PDFs from anchors
//     let pdfLinks = [];
//     try {
//       const pdfAnchors = await page.$$('a[href$=".pdf"]');
//       for (const a of pdfAnchors) {
//         const href = await a.evaluate((el) => el.href);
//         const text = await a.evaluate((el) => el.innerText.trim());
//         if (href && href.toLowerCase().endsWith(".pdf")) {
//           pdfLinks.push({ href, text });
//         }
//       }
//     } catch (err) {
//       console.log(`⚠️ Error extracting PDFs from anchors: ${err.message}`);
//     }

//     // Check divs for onclick or href containing PDFs
//     try {
//       const divs = await page.$$("div");
//       for (const div of divs) {
//         const text = await div.evaluate((el) => el.innerText.trim());
//         const onclick = await div.evaluate(
//           (el) => el.getAttribute("onclick") || ""
//         );
//         const href = await div.evaluate((el) => el.getAttribute("href") || "");
//         let candidate = null;
//         if (href && href.includes(".pdf")) {
//           candidate = href;
//         } else if (onclick && onclick.includes(".pdf")) {
//           const match = onclick.match(/(https?:\/\/[^\s'"]+\.pdf)/);
//           if (match) {
//             candidate = match[1];
//           }
//         }
//         if (candidate) {
//           pdfLinks.push({ href: candidate, text });
//         }
//       }
//     } catch (err) {
//       console.log(`⚠️ Error extracting PDFs from divs: ${err.message}`);
//     }

//     // Download PDFs
//     for (const pdf of pdfLinks) {
//       const pdfUrl = pdf.href;
//       const pdfName = path.basename(pdfUrl.split("?")[0]);
//       const pdfPath = path.join(pdfDir, pdfName);
//       if (!fs.existsSync(pdfPath)) {
//         await downloadFile(pdfUrl, pdfPath);
//       }
//     }

//     // Save result
//     const pageName = url.replace(/^https?:\/\//, "").replace(/[\/]/g, "_");
//     const result = { url, texts, images, pdfs: pdfLinks };
//     const jsonPath = path.join(
//       saveDir,
//       `all_text_images_pdfs_${pageName}.json`
//     );
//     fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");

//     console.log(
//       `✅ Extracted ${texts.length} texts, ${images.length} images, ${pdfLinks.length} PDFs -> saved at ${jsonPath}`
//     );

//     return result;
//   } catch (error) {
//     console.error(`❌ Error scraping ${url}: ${error.message}`);
//     return { url, texts: [], images: [], pdfs: [] };
//   } finally {
//     await browser.close();
//   }
// }

// // Main execution
// (async () => {
//   const urls = [
//     "https://jiopay.com/business",
//     "https://jiopay.com/business/partner-program",
//     "https://jiopay.com/business/contact",
//     "https://jiopay.com/business/about-us",
//     "https://jiopay.com/business/paymentgateway",
//     "https://jiopay.com/business/pointofsale",
//     "https://jiopay.com/business/upi",
//     "https://jiopay.com/business/biller",
//     "https://jiopay.com/business/jio-pay-business",
//     "https://jiopay.com/business/help-center",
//     "https://jiopay.com/business/investor-relation",
//     "https://jiopay.com/business/complaint-resolution-escalation-matrix",
//     "https://jiopay.com/business/privacy-policy",
//     "https://jiopay.com/business/terms-conditions",
//     "https://jiopay.com/business/on-boarding-and-kyc-policy",
//     "https://jiopay.com/business/billpay-terms-conditions",
//     "https://jiopay.com/business/paymentgateway/1qr",
//     "https://jiopay.com/business/paymentgateway/direct",
//     "https://jiopay.com/business/paymentgateway/checkout",
//     "https://jiopay.com/business/paymentgateway/vault",
//     "https://jiopay.com/business/paymentgateway/collect",
//     "https://jiopay.com/business/paymentgateway/repeat",
//     "https://jiopay.com/business/paymentgateway/campaign",
//     "https://jiopay.com/business/paymentgateway/console",
//     "https://jiopay.com/business/increase-conversion",
//     "https://jiopay.com/business/widen-presence",
//     "https://jiopay.com/business/mitigate-risk",
//     "https://jiopay.com/business/simplified-experience",
//   ];

//   for (const url of urls) {
//     const data = await scrapeAllTextImagesPdfs(url);
//     console.log(
//       `✔ Final: Extracted ${data.texts.length} texts, ${data.images.length} images, ${data.pdfs.length} PDFs`
//     );
//   }
// })();

// import fs from "fs";
// import path from "path";
// import axios from "axios";
// import puppeteer from "puppeteer";

// // Ensure directory exists
// function ensureDir(dirPath) {
//   if (!fs.existsSync(dirPath)) {
//     fs.mkdirSync(dirPath, { recursive: true });
//   }
//   return dirPath;
// }

// // Download file using axios
// async function downloadFile(url, savePath) {
//   try {
//     const writer = fs.createWriteStream(savePath);
//     const response = await axios({
//       url,
//       method: "GET",
//       responseType: "stream",
//       timeout: 30000,
//       headers: {
//         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
//       }
//     });

//     if (response.status === 200) {
//       response.data.pipe(writer);
//       await new Promise((resolve, reject) => {
//         writer.on("finish", resolve);
//         writer.on("error", reject);
//       });
//       console.log(`📥 Downloaded ${url} -> ${savePath}`);
//     } else {
//       console.log(`⚠️ Failed to download ${url} (status ${response.status})`);
//     }
//   } catch (error) {
//     console.log(`❌ Error downloading ${url}: ${error.message}`);
//   }
// }

// // Check if page is still valid and accessible
// async function isPageAccessible(page) {
//   try {
//     if (!page || page.isClosed()) {
//       return false;
//     }
//     await page.evaluate(() => document.readyState);
//     return true;
//   } catch (error) {
//     return false;
//   }
// }

// // Extract all data in one go to avoid context issues
// async function extractAllData(page) {
//   return await page.evaluate(() => {
//     const result = {
//       texts: [],
//       images: [],
//       pdfLinks: []
//     };

//     // Extract texts - try specific selectors first, then fallback
//     try {
//       const specificSelectors = ['div.css-146c3p1', 'div.css-g5y9jx'];
//       let textElements = [];

//       specificSelectors.forEach(selector => {
//         const elements = document.querySelectorAll(selector);
//         textElements.push(...Array.from(elements));
//       });

//       if (textElements.length > 0) {
//         result.texts = textElements
//           .map(el => el.innerText?.trim())
//           .filter(txt => txt && txt.toLowerCase() !== "loading" && txt.length > 3);
//       } else {
//         // Fallback to general selectors
//         const fallbackSelectors = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'div[class*="content"]', 'main', 'article'];
//         const allTexts = new Set();

//         fallbackSelectors.forEach(selector => {
//           const elements = document.querySelectorAll(selector);
//           elements.forEach(el => {
//             const text = el.innerText?.trim();
//             if (text && text.length > 10 && !text.toLowerCase().includes('loading')) {
//               allTexts.add(text);
//             }
//           });
//         });

//         result.texts = Array.from(allTexts).slice(0, 100);
//       }
//     } catch (e) {
//       console.log('Text extraction error in page context:', e.message);
//     }

//     // Extract images
//     try {
//       const imgElements = document.querySelectorAll('img');
//       result.images = Array.from(imgElements)
//         .map(img => ({
//           src: img.src || img.getAttribute('src'),
//           alt: img.alt || img.getAttribute('alt') || ''
//         }))
//         .filter(img => img.src);
//     } catch (e) {
//       console.log('Image extraction error in page context:', e.message);
//     }

//     // Extract PDF links
//     try {
//       const allLinks = [];

//       // Check anchor tags
//       const anchors = document.querySelectorAll('a');
//       anchors.forEach(a => {
//         const href = a.href || a.getAttribute('href');
//         if (href && href.toLowerCase().includes('.pdf')) {
//           allLinks.push({
//             href: href,
//             text: a.innerText?.trim() || 'PDF Document'
//           });
//         }
//       });

//       // Check for PDFs in onclick attributes and other attributes
//       const allElements = document.querySelectorAll('*');
//       allElements.forEach(el => {
//         const onclick = el.getAttribute('onclick') || '';
//         const href = el.getAttribute('href') || '';

//         [onclick, href].forEach(attr => {
//           if (attr && attr.includes('.pdf')) {
//             const matches = attr.match(/(https?:\/\/[^\s'"]+\.pdf)/g);
//             if (matches) {
//               matches.forEach(match => {
//                 allLinks.push({
//                   href: match,
//                   text: el.innerText?.trim() || 'PDF Document'
//                 });
//               });
//             }
//           }
//         });
//       });

//       // Remove duplicates
//       const uniqueLinks = allLinks.filter((link, index, self) =>
//         index === self.findIndex(l => l.href === link.href)
//       );

//       result.pdfLinks = uniqueLinks;
//     } catch (e) {
//       console.log('PDF extraction error in page context:', e.message);
//     }

//     return result;
//   });
// }

// // Main scraping function with improved error handling
// async function scrapeAllTextImagesPdfs(url, saveDir = "scraped_data_general") {
//   ensureDir(saveDir);
//   const pdfDir = ensureDir(path.join(saveDir, "pdfs"));

//   let browser;
//   let page;

//   try {
//     browser = await puppeteer.launch({
//       headless: false,
//       slowMo: 100,
//       args: [
//         "--no-sandbox",
//         "--disable-setuid-sandbox",
//         "--disable-web-security",
//         "--disable-features=VizDisplayCompositor",
//         "--disable-dev-shm-usage",
//         "--disable-background-timer-throttling",
//         "--disable-backgrounding-occluded-windows",
//         "--disable-renderer-backgrounding"
//       ],
//       defaultViewport: { width: 1280, height: 800 },
//       ignoreDefaultArgs: ['--disable-extensions'],
//     });

//     page = await browser.newPage();

//     // Set user agent and headers
//     await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');

//     // Set generous timeouts
//     page.setDefaultTimeout(90000);
//     page.setDefaultNavigationTimeout(90000);

//     // Prevent page from closing unexpectedly
//     await page.evaluateOnNewDocument(() => {
//       // Override window.close to prevent unexpected closures
//       window.close = () => {
//         console.log('Prevented window.close()');
//       };
//     });

//     console.log(`🔗 Navigating to ${url}`);

//     // Navigate with better error handling
//     let navigationSuccessful = false;
//     const maxNavigationRetries = 3;

//     for (let i = 0; i < maxNavigationRetries; i++) {
//       try {
//         await page.goto(url, {
//           waitUntil: ["domcontentloaded"],
//           timeout: 60000
//         });

//         // Wait for page to stabilize
//         await new Promise(resolve => setTimeout(resolve, 3000));

//         if (await isPageAccessible(page)) {
//           navigationSuccessful = true;
//           console.log(`✅ Successfully navigated to ${url}`);
//           break;
//         } else {
//           throw new Error(`Page became inaccessible after navigation attempt ${i + 1}`);
//         }
//       } catch (error) {
//         console.log(`Navigation attempt ${i + 1}/${maxNavigationRetries} failed: ${error.message}`);
//         if (i === maxNavigationRetries - 1) {
//           throw error;
//         }
//         await new Promise(resolve => setTimeout(resolve, 2000));
//       }
//     }

//     if (!navigationSuccessful) {
//       throw new Error("Failed to navigate after all retry attempts");
//     }

//     // Try to wait for content to load
//     const possibleSelectors = [
//       "div.css-146c3p1",
//       "div.css-g5y9jx",
//       "main",
//       "body"
//     ];

//     let contentReady = false;
//     for (const selector of possibleSelectors) {
//       try {
//         await page.waitForSelector(selector, { timeout: 10000 });
//         console.log(`✅ Found content selector: ${selector}`);
//         contentReady = true;
//         break;
//       } catch (e) {
//         console.log(`⚠️ Selector ${selector} not found within timeout`);
//       }
//     }

//     // Additional wait for dynamic content
//     await new Promise(resolve => setTimeout(resolve, 2000));

//     // Final accessibility check with additional wait
//     await new Promise(resolve => setTimeout(resolve, 1000));
//     if (!(await isPageAccessible(page))) {
//       throw new Error("Page became inaccessible before data extraction");
//     }

//     console.log("📊 Extracting all data...");

//     // Extract all data in one operation to minimize context switching
//     let extractedData = { texts: [], images: [], pdfLinks: [] };

//     try {
//       extractedData = await extractAllData(page);
//       console.log(`📝 Extracted ${extractedData.texts.length} texts`);
//       console.log(`🖼️ Extracted ${extractedData.images.length} images`);
//       console.log(`📄 Extracted ${extractedData.pdfLinks.length} PDF links`);
//     } catch (error) {
//       console.log(`⚠️ Error during data extraction: ${error.message}`);
//       // Try a simpler extraction as fallback
//       try {
//         extractedData.texts = await page.$$eval('*', elements => {
//           const texts = [];
//           elements.forEach(el => {
//             const text = el.innerText?.trim();
//             if (text && text.length > 10 && text.length < 50000000) {
//               texts.push(text);
//             }
//           });
//           return [...new Set(texts)].slice(0, 50);
//         });
//         console.log(`📝 Fallback extraction: ${extractedData.texts.length} texts`);
//       } catch (fallbackError) {
//         console.log(`⚠️ Fallback extraction also failed: ${fallbackError.message}`);
//       }
//     }

//     // Download PDFs
//     for (const pdf of extractedData.pdfLinks) {
//       try {
//         const pdfUrl = pdf.href;
//         const pdfName = path.basename(pdfUrl.split("?")[0]) || `pdf_${Date.now()}.pdf`;
//         const pdfPath = path.join(pdfDir, pdfName);

//         if (!fs.existsSync(pdfPath)) {
//           await downloadFile(pdfUrl, pdfPath);
//         } else {
//           console.log(`📄 PDF already exists: ${pdfName}`);
//         }
//       } catch (error) {
//         console.log(`❌ Error downloading PDF ${pdf.href}: ${error.message}`);
//       }
//     }

//     // Save results
//     const pageName = url.replace(/^https?:\/\//, "").replace(/[\/\?#]/g, "_");
//     const result = {
//       url,
//       timestamp: new Date().toISOString(),
//       texts: extractedData.texts.slice(0, 100),
//       images: extractedData.images,
//       pdfs: extractedData.pdfLinks,
//       contentReady,
//       extractionMethod: "unified"
//     };

//     const jsonPath = path.join(saveDir, `scraped_${pageName}.json`);
//     fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2), "utf-8");

//     console.log(`✅ Successfully scraped ${url}`);
//     console.log(`   📝 Texts: ${extractedData.texts.length}, 🖼️ Images: ${extractedData.images.length}, 📄 PDFs: ${extractedData.pdfLinks.length}`);
//     console.log(`   💾 Saved to: ${jsonPath}\n`);

//     return result;

//   } catch (error) {
//     console.error(`❌ Error scraping ${url}: ${error.message}`);
//     return {
//       url,
//       timestamp: new Date().toISOString(),
//       error: error.message,
//       texts: [],
//       images: [],
//       pdfs: []
//     };
//   } finally {
//     // Improved cleanup
//     try {
//       if (page && !page.isClosed()) {
//         await page.close();
//       }
//     } catch (closeError) {
//       console.log(`⚠️ Error closing page: ${closeError.message}`);
//     }

//     try {
//       if (browser) {
//         await browser.close();
//       }
//     } catch (closeError) {
//       console.log(`⚠️ Error closing browser: ${closeError.message}`);
//     }
//   }
// }

// // Main execution
// (async () => {
//   /*const urls = [
//     "https://jiopay.com/business",
//     "https://jiopay.com/business/partner-program",
//     "https://jiopay.com/business/contact",
//     "https://jiopay.com/business/about-us",
//     "https://jiopay.com/business/paymentgateway",
//     "https://jiopay.com/business/pointofsale",
//     "https://jiopay.com/business/upi",
//     "https://jiopay.com/business/biller",
//     "https://jiopay.com/business/jio-pay-business",
//     "https://jiopay.com/business/help-center",
//     "https://jiopay.com/business/investor-relation",
//     "https://jiopay.com/business/complaint-resolution-escalation-matrix",
//     "https://jiopay.com/business/privacy-policy",
//     "https://jiopay.com/business/terms-conditions",
//     "https://jiopay.com/business/on-boarding-and-kyc-policy",
//     "https://jiopay.com/business/billpay-terms-conditions",
//     "https://jiopay.com/business/paymentgateway/1qr",
//     "https://jiopay.com/business/paymentgateway/direct",
//     "https://jiopay.com/business/paymentgateway/checkout",
//     "https://jiopay.com/business/paymentgateway/vault",
//     "https://jiopay.com/business/paymentgateway/collect",
//     "https://jiopay.com/business/paymentgateway/repeat",
//     "https://jiopay.com/business/paymentgateway/campaign",
//     "https://jiopay.com/business/paymentgateway/console",
//     "https://jiopay.com/business/increase-conversion",
//     "https://jiopay.com/business/widen-presence",
//     "https://jiopay.com/business/mitigate-risk",
//     "https://jiopay.com/business/simplified-experience",
//   ];*/

//   const urls = ["https://jiopay.com/business/increase-conversion"];

//   console.log(`🚀 Starting to scrape ${urls.length} URLs...\n`);

//   const results = [];
//   let successCount = 0;
//   let errorCount = 0;

//   for (let i = 0; i < urls.length; i++) {
//     const url = urls[i];
//     console.log(`\n[${i + 1}/${urls.length}] Processing: ${url}`);

//     try {
//       const data = await scrapeAllTextImagesPdfs(url);
//       results.push(data);

//       if (data.error) {
//         errorCount++;
//       } else {
//         successCount++;
//       }

//       // Add delay between requests
//       if (i < urls.length - 1) {
//         console.log("⏳ Waiting 5 seconds before next URL...");
//         await new Promise(resolve => setTimeout(resolve, 5000));
//       }

//     } catch (error) {
//       console.error(`💥 Fatal error processing ${url}: ${error.message}`);
//       errorCount++;
//       results.push({
//         url,
//         timestamp: new Date().toISOString(),
//         fatalError: error.message,
//         texts: [],
//         images: [],
//         pdfs: []
//       });
//     }
//   }

//   // Save summary
//   const summary = {
//     totalUrls: urls.length,
//     successCount,
//     errorCount,
//     timestamp: new Date().toISOString(),
//     results: results.map(r => ({
//       url: r.url,
//       textsCount: r.texts?.length || 0,
//       imagesCount: r.images?.length || 0,
//       pdfsCount: r.pdfs?.length || 0,
//       hasError: !!(r.error || r.fatalError)
//     }))
//   };

//   fs.writeFileSync(
//     "scraped_data_general/summary.json",
//     JSON.stringify(summary, null, 2),
//     "utf-8"
//   );

//   console.log(`\n🏁 SCRAPING COMPLETE!`);
//   console.log(`✅ Successful: ${successCount}`);
//   console.log(`❌ Errors: ${errorCount}`);
//   console.log(`📊 Summary saved to: scraped_data_general/summary.json`);
// })();

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
