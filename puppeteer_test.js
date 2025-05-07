const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Opera.app/Contents/MacOS/Opera',
    headless: true,
  });
  const page = await browser.newPage();
  await page.goto('http://localhost:3000/login');
  console.log('Page title:', await page.title());
  await browser.close();
})();
