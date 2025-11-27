const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  try {
    // Connect to the existing browser instance
    const browser = await chromium.connectOverCDP('http://localhost:9222');
    const contexts = browser.contexts();
    
    if (contexts.length === 0) {
      console.error('No browser contexts found');
      process.exit(1);
    }
    
    const pages = await contexts[0].pages();
    
    // Find the Amazon page
    let amazonPage = null;
    for (const page of pages) {
      const url = page.url();
      if (url.includes('amazon.com')) {
        amazonPage = page;
        break;
      }
    }
    
    if (!amazonPage) {
      console.error('Amazon page not found');
      process.exit(1);
    }
    
    console.log('Found Amazon page:', amazonPage.url());
    
    // Get the full HTML content
    const htmlContent = await amazonPage.content();
    
    // Save to file
    const filePath = '/home/divyanshu/.gemini/antigravity/playground/binary-quasar/amazon.html';
    fs.writeFileSync(filePath, htmlContent, 'utf-8');
    
    console.log(`Successfully saved Amazon page source to amazon.html`);
    console.log(`File size: ${htmlContent.length} characters`);
    console.log(`File location: ${filePath}`);
    
    await browser.close();
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
