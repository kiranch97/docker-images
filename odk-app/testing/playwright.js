const playwright = require('playwright');

(async () => {
  for (const browserType of ['chromium', 'firefox']) {
    const browser = await playwright[browserType].launchPersistent({
      args: ['--enable-features=NetworkService'],
      userDataDir: "Documents/comakership/master-copy/odk-app/testing/myUserDataDir",
      headless: false,
      ignoreHTTPSErrors: false,
    });
    console.log(browser.isConnected())
    console.log(browser)
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('localhost:8082/pwa');

    //START PAGE
    await page.click("button#transparent-button")
    //RECOMMENDATIONS PAGE
    await page.click("button#transparent-button")
    //CHECK LIST PAGE
    await page.click("button#loc-check-button")

  }
})();



// (async () => {
//   const browser = await chromium.launch({
//                 args: ['--enable-features=NetworkService'],
//                 headless: false,
//                 ignoreHTTPSErrors: false,
//             });
//   const context = await browser.newContext();
//   // await context.clearPermissionOverrides();
//   const page = await context.newPage();
//   await context.setPermissions('localhost:8082/checklist', ['geolocation', 'camera']);
//   console.log(context.setPermissions())
//   await page.goto('localhost:8082/pwa');
//   //START PAGE
//   await page.click("button#transparent-button")
//   //RECOMMENDATIONS PAGE
//   await page.click("button#transparent-button")
//   //CHECK LIST PAGE
//   await page.click("button#loc-check-button")
//   // await page.on('prompt', async dialog => {
//   //   console.log(prompt.message());
//   //   await prompt.accept();
//   //   // await browser.close();
//   // });
//   await page.click("button#camera-check-button")
// context.setPermissions('localhost:8082/checklist', ['camera']);



//     const granted = await page.evaluate(async () => {
//       return (await navigator.permissions.query({name: 'geolocation'})).state;
//     });
// console.log('Granted:', granted);


// })();