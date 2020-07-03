// Browsers

export function isChrome () {
  return /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
}

export function isFirefox () {
  return /Firefox/.test(navigator.userAgent);
}

export function isMSEdge () {
  return /Edge/.test(navigator.userAgent);
}

export function isMSIE () {
  return ((navigator.appName == "Microsoft Internet Explorer") || ((navigator.appName == "Netscape") && (new RegExp("Trident/.*rv:([0-9]{1,}[.0-9]{0,})").exec(navigator.userAgent) != null)));
}

export function isSafari () {
  return /Safari/.test(navigator.userAgent) && /Apple Computer/.test(navigator.vendor);
}

export function isWebKit () {
  return /^((?!chrome|android).)*safari/i.test(window.navigator.userAgent);
}

// Platforms

export function isAndroid () {
  return /android/.test(navigator.userAgent);
}

export function isiOS () {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
}
