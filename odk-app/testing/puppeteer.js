require('dotenv').config();
const puppeteer = require('puppeteer');
const pptrFirefox = require('puppeteer-firefox');
// const iPhoneLandscape = puppeteer.devices['iPhone X landscape'];
const iPhonePortrait = puppeteer.devices['iPhone X'];
const androidPortrait = puppeteer.devices['Pixel 2 XL'];

//---- SCENARIO 1 - DEMO USER FIRST TIME on Mobile
// (async () => {

//     /* Browser Settings */
//     const browser = await puppeteer.launch({
//         args: ['--enable-features=NetworkService'],
//         headless: false,
//         devtools: true,
//         ignoreHTTPSErrors: false,
//         // slowMo: 250 // slow down by 250ms  
//     });

//     /* Initialize Chrome browser instance */
//     const context = browser.defaultBrowserContext();
//     await context.overridePermissions(process.env.LOCAL_URL, ['geolocation', 'camera']);
//     const page = await context.newPage();
//     await page.emulate(iPhone);

//     //Read Logs in console
//     page.on('console', msg => {
//         for (let i = 0; i < msg.args().length; ++i)
//             console.log(`${i}: ${msg.args()[i]}`);
//     });

//     /* Skip Recommendations page (Low-priority because page is static) */
//     await page.goto(process.env.LOCAL_URL + '/recommendation');
//     await page.waitForSelector("button#transparent-button")
//     await page.click("button#transparent-button")


//     /* Check GPS and Camera permissions */
//     await page.waitForSelector("button#loc-check-button")
//     await page.click("button#loc-check-button")
//     await page.waitForSelector("button#camera-check-button")
//     await page.click("button#camera-check-button")

//     /* Choose Demo user */
//     await page.waitFor(5000)
//     await page.waitForSelector("button#transparent-button")
//     await page.click("button#transparent-button")
//     /* Log User type */
//     const localStorage = await page.evaluate(() => Object.assign({}, window.localStorage));
//     console.log(localStorage)

//     /* Check if camera angle can switch */
//     await page.waitForSelector("img.stream-flip")
//     await page.click("img.stream-flip")


//     //Test Play/Pause button
//     await page.waitForSelector("div.inner-circle")
//     await page.click("div.inner-circle")
//     await page.waitFor(5000)
//     await page.waitForSelector("div.inner-button")
//     await page.click("div.inner-button")

//     await page.waitForSelector("span.check")
//     await page.click("span.check")

//     page.close()


//     const context2 = browser.defaultBrowserContext();
//     const page2 = await context2.newPage()
//     await page2.emulate(iPhone);
//     await page2.goto(process.env.LOCAL_URL + '/user');

// })();

//User manual script

(async () => {
    const firefoxBrowser = await pptrFirefox.launch({
        args: ['--enable-features=NetworkService'],
        headless: false,
        devtools: true,
        ignoreHTTPSErrors: false,
        slowMo: 250 // slow down by 250ms  
    });

    // const chromeBrowser = await puppeteer.launch({
    //     args: ['--enable-features=NetworkService'],
    //     headless: false,
    //     devtools: true,
    //     ignoreHTTPSErrors: false,
    //     slowMo: 250 // slow down by 250ms  
    // });

    /* Initialize Firefox browser instance */
    const firefoxContext = firefoxBrowser.defaultBrowserContext();
    const firefoxPage = await firefoxContext.newPage();
    await firefoxPage.emulate(androidPortrait);


    //Read Logs in console
    // firefoxPage.on('console', msg => {
    //     for (let i = 0; i < msg.args().length; ++i)
    //         console.log(`${i}: ${msg.args()[i]}`);
    // });

    await firefoxPage.goto(process.env.PRODUCTION_URL);
    await firefoxPage.waitForSelector("a")
    await firefoxPage.click("a")
    //CHECK Chrome manual
    await firefoxPage.waitForSelector("a#chrome")
    await firefoxPage.click("a#chrome")
    //CHECK Edge manual
    await firefoxPage.waitForSelector("a#edge")
    await firefoxPage.click("a#edge")
    //Check ios manual
    await firefoxPage.waitForSelector("a#ios")
    await firefoxPage.click("a#ios")
    //Check other browsers manual
    await firefoxPage.waitForSelector("a#other-browsers")
    await firefoxPage.click("a#other-browsers")


    /* Initialize Chrome browser instance */
    // const chromeContext = chromeBrowser.defaultBrowserContext();
    // const chromePage = await chromeContext.newPage();
    // await chromePage.emulate(androidPortrait)

    // await chromePage.goto(process.env.LOCAL_URL);
    // await chromePage.waitForSelector("a")
    // await chromePage.click("a")
    // //CHECK Chrome manual
    // await chromePage.waitForSelector("a#firefox")
    // await chromePage.click("a#firefox")
    // //CHECK Edge manual
    // await chromePage.waitForSelector("a#edge")
    // await chromePage.click("a#edge")
    // //Check ios manual
    // await chromePage.waitForSelector("a#ios")
    // await chromePage.click("a#ios")
    // //Check other browsers manual
    // await chromePage.waitForSelector("a#other-browsers")
    // await chromePage.click("a#other-browsers")

})();