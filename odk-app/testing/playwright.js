const playwright = require('playwright');
require('dotenv').config();


// (async () => {
//     for (const browserType of ['firefox']) {
//         const browser = await playwright[browserType].launch({
//             headless: false,
//             ignoreHTTPSErrors: false,
//             slowMo: 250 // slow down by 250ms  
//         });
//         const context = await browser.newContext({
//         });
//         const page = await context.newPage();
//         await page.setViewportSize({
//             width: 360,
//             height: 740,
//         });
//         await page.goto(process.env.LOCAL_URL);

//         await page.waitForSelector("a")
//         await page.click("a")
//         await page.screenshot({
//             path: `./firefox/home-${browserType}.png`, fullPage: true
//         });
//         //CHECK Chrome manual
//         await page.waitForSelector("a#chrome")
//         await page.click("a#chrome")
//         await page.screenshot({
//             path: `./firefox/chrome-${browserType}.png`, fullPage: true
//         });
//         //CHECK Edge manual
//         await page.waitForSelector("a#edge")
//         await page.click("a#edge")
//         await page.screenshot({
//             path: `./firefox/edge-${browserType}.png`, fullPage: true
//         });
//         //Check ios manual
//         await page.waitForSelector("a#ios")
//         await page.click("a#ios")
//         await page.screenshot({
//             path: `./firefox/ios-${browserType}.png`, fullPage: true
//         });
//         //Check other browsers manual
//         await page.waitForSelector("a#other-browsers")
//         await page.click("a#other-browsers")
//         await page.screenshot({
//             path: `./firefox/other-browsers-${browserType}.png`, fullPage: true
//         });
//         await page.waitForSelector("a#desktop")
//         await page.click("a#desktop")
//         await page.screenshot({
//             path: `./firefox/desktop-${browserType}.png`, fullPage: true
//         });
//         //Go back to main screen
//         await page.waitForSelector("img#logo")
//         await page.click("img#logo")

//         // await browser.close();
//     }
// })();


(async () => {
    for (const browserType of ['chromium']) {
        const browser = await playwright[browserType].launch({
            headless: false,
            ignoreHTTPSErrors: false,
            // slowMo: 250 // slow down by 250ms  
        });
        const context = await browser.newContext({
        });
        const page = await context.newPage();
        await page.setViewportSize({
            width: 360,
            height: 740,
        });
        await page.goto(process.env.LOCAL_URL);

        await page.waitForSelector("a")
        await page.click("a")
        await page.screenshot({
            path: `./chromium/home-${browserType}.png`, fullPage: true
        });
        //CHECK Chrome manual
        await page.waitForSelector("a#firefox")
        await page.click("a#firefox")
        await page.screenshot({
            path: `./chromium/firefox-${browserType}.png`, fullPage: true
        });
        //CHECK Edge manual
        await page.waitForSelector("a#edge")
        await page.click("a#edge")
        await page.screenshot({
            path: `./chromium/edge-${browserType}.png`, fullPage: true
        });
        //Check ios manual
        await page.waitForSelector("a#ios")
        await page.click("a#ios")
        await page.screenshot({
            path: `./chromium/ios-${browserType}.png`, fullPage: true
        });
        //Check other browsers manual
        await page.waitForSelector("a#other-browsers")
        await page.click("a#other-browsers")
        await page.screenshot({
            path: `./chromium/other-browsers-${browserType}.png`, fullPage: true
        });
        await page.waitForSelector("a#desktop")
        await page.click("a#desktop")
        await page.screenshot({
            path: `./chromium/desktop-${browserType}.png`, fullPage: true
        });
        //Go back to main screen
        await page.waitForSelector("img#logo")
        await page.click("img#logo")

        // await browser.close();
    }
})();