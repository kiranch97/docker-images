require('dotenv').config();
const puppeteer = require('puppeteer');
// const devices = require('puppeteer/DeviceDescriptors');
const iPhone = puppeteer.devices['iPhone X landscape'];



//---- SCENARIO 1 - DEMO USER FIRST TIME on Mobile
(async () => {

    /* Browser Settings */
    const browser = await puppeteer.launch({
        args: ['--enable-features=NetworkService'],
        headless: false,
        devtools: true,
        ignoreHTTPSErrors: false,
        slowMo: 250 // slow down by 250ms  
    });

    /* Initialize Chrome browser instance */
    const context = browser.defaultBrowserContext();
    await context.overridePermissions(process.env.LOCAL_URL , ['geolocation', 'camera']);
    const page = await context.newPage();
    await page.emulate(iPhone);

    /* Choose Demo user on Welcome Page */
    await page.goto(process.env.LOCAL_URL + '/pwa');
    await page.waitForSelector("button#transparent-button")
    await page.click("button#transparent-button")
    /* Log User type */
    const localStorage = await page.evaluate(() => Object.assign({}, window.localStorage));
    console.log(localStorage)

    /* Skip Recommendations page (Low-priority because page is static) */
    await page.waitForSelector("button#transparent-button")
    await page.click("button#transparent-button")
    /* Check GPS and Camera permissions */
    await page.waitForSelector("button#loc-check-button")
    await page.click("button#loc-check-button")
    await page.waitForSelector("button#camera-check-button")
    await page.click("button#camera-check-button")

    /* Check if camera angle can switch */
    await page.waitForSelector("img.stream-flip")
    await page.click("img.stream-flip")

    page.on('console', msg => {
        for (let i = 0; i < msg.args().length; ++i)
          console.log(`${i}: ${msg.args()[i]}`);
      });

    //Test Play/Pause button
    await page.waitForSelector("div.inner-circle")
    await page.click("div.inner-circle")
    await page.waitFor(5000)
    // await page.waitFor(5000)
    await page.waitForSelector("div.inner-button")
    await page.click("div.inner-button")

    await page.waitForSelector("span.check")
    await page.click("span.check")

    // page.close()


    // const context2 = browser.defaultBrowserContext();
    // const page2 = await context2.newPage()
    // await page2.emulate(iPhone);
    // await page2.goto(process.env.LOCAL_URL + '/pwa');

    //-- Check if videostream is working and has resolution of 1280 x 720
    //-- Check if Streaming mode matches with User Type
    //-- Try Camera flip
    //-- Try Mode Switch button



})();


//---- SCENARIO 2 - WASTE DRIVER FIRST TIME




//---- SCENARIO 2.1 - REGULAR WASTE DRIVER