const fs = require('fs');
let manifestTemplate;

try {
    manifestTemplate = fs.readFileSync('manifest-template.json', 'utf8');
} catch (err) {
    console.error(err);
    return;
}

let appName = process.env.APP_NAME
console.log("App name from environment:", appName)
if (appName === undefined) {
    appName = 'ODK'
}
let res = manifestTemplate.replace(/APP_NAME/g, appName);

try {
    const data = fs.writeFileSync('./public/manifest.json', res);
} catch (err) {
    console.error(err);
    return;
}