const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        args: ['--enable-features=NetworkService'],
        userDataDir: "Documents/comakership/master-copy/odk-app/testing/myUserDataDir",
        headless: false,
        devtools: true,
        ignoreHTTPSErrors: false,
    });

    const context = browser.defaultBrowserContext();
    
    // context.clearPermissionOverrides();
    const page = await context.newPage();
    await page.goto('http://localhost:8082/pwa');
    // await context.overridePermissions('localhost:8082', ['geolocation', 'camera']);

    //START PAGE
    await page.click("button#transparent-button")
    const localStorage = await page.evaluate(() =>  Object.assign({}, window.localStorage));
    console.log(localStorage)
    //RECOMMENDATIONS PAGE
    await page.click("button#transparent-button")
    //CHECK LIST PAGE
    await page.click("button#loc-check-button")
    await page.click("button#camera-check-button")
})();