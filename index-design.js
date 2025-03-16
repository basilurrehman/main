const puppeteer = require('puppeteer');
const fs = require('fs');

async function run() {
    async function getRenderedHTML(url) {
        if (!url) {
            return '<html><title>nothing</title><body>nothing</body></html>';
        }

        async function launchBrowser() {
            return await puppeteer.launch({
                headless: true,
                executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--start-maximized',
                    '--disable-infobars',
                    '--disable-dev-shm-usage',
                    '--remote-debugging-port=9222'
                ],
                timeout: 30000
            });
        }

        let browser = await launchBrowser();
        let page; // Declare page outside the try block for scope access
        try {
            page = await browser.newPage();
            await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
            await page.setViewport({ width: 1920, height: 1080 });
            await page.setExtraHTTPHeaders({
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
                'accept-language': 'en-US,en;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'connection': 'keep-alive',
                'upgrade-insecure-requests': '1'
            });

            const maxRetries = 3;
            for (let attempt = 1; attempt <= maxRetries; attempt++) {
                try {
                    await page.goto(url, { waitUntil: 'load', timeout: 60000 });
                    await page.waitForSelector('body', { timeout: 60000 });
                    await autoScroll(page);
                    const html = await page.content();
                    return html;
                } catch (error) {
                    if (attempt === maxRetries) {
                        console.error(`Final attempt failed. Saving current HTML. Error: ${error.message}`);
                        // Return whatever HTML is available after the last attempt
                        const html = await page.content();
                        return html;
                    }
                    console.error(`Attempt ${attempt} failed: ${error.message}. Retrying...`);
                }
            }
        } catch (error) {
            let html = '<html><title>Error</title><body>Error occurred</body></html>';
            // Check if page exists and try to get HTML
            if (page) {
                try {
                    html = await page.content();
                } catch (innerError) {
                    console.error('Failed to retrieve HTML after error:', innerError);
                }
            }

            // Handle specific HTTP/2 error with a fresh browser instance
            if (error.message.includes('net::ERR_HTTP2_PROTOCOL_ERROR')) {
                console.error('HTTP/2 error encountered, retrying with new browser...');
                await browser.close();
                try {
                    browser = await launchBrowser();
                    const newPage = await browser.newPage();
                    // Reconfigure newPage settings
                    await newPage.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36');
                    await newPage.setViewport({ width: 1920, height: 1080 });
                    await newPage.setExtraHTTPHeaders({
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
                        'accept-language': 'en-US,en;q=0.9',
                        'accept-encoding': 'gzip, deflate, br',
                        'connection': 'keep-alive',
                        'upgrade-insecure-requests': '1'
                    });

                    await newPage.goto(url, { waitUntil: 'load', timeout: 60000 });
                    await newPage.waitForSelector('body', { timeout: 60000 });
                    await autoScroll(newPage);
                    html = await newPage.content();
                } catch (retryError) {
                    console.error('Retry after HTTP/2 error failed:', retryError);
                    // Attempt to capture HTML even if retry fails
                    if (newPage) {
                        try {
                            html = await newPage.content();
                        } catch (e) {
                            console.error('Failed to get HTML after retry:', e);
                        }
                    }
                }
            } else {
                console.error('Error occurred, saving available HTML:', error.message);
            }
            return html;
        } finally {
            await browser.close();
        }
    }

    async function autoScroll(page) {
        await page.evaluate(async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if (totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        });
    }

    const number = process.argv[2];
    const url = process.argv[3];

    if (!number) {
        console.error('Please provide a number as the first argument.');
        process.exit(1);
    }

    const html = await getRenderedHTML(url);
    const filename = `html-design${number}.html`;
    fs.writeFileSync(filename, html, 'utf-8');
    console.log(`Full HTML content saved to ${filename}`);
    process.exit(0);
}

run().catch(error => {
    console.error(error);
    process.exit(1);
});