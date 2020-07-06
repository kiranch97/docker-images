// Browsers

export function isChrome () {
  return /Chrome/i.test(navigator.userAgent) && /Google Inc/i.test(navigator.vendor);
}

export function isFirefox () {
  return /Firefox/i.test(navigator.userAgent);
}

export function isMSEdge () {
  return /Edge/i.test(navigator.userAgent);
}

export function isMSIE () {
  return ((navigator.appName == "Microsoft Internet Explorer") || ((navigator.appName == "Netscape") && (new RegExp("Trident/.*rv:([0-9]{1,}[.0-9]{0,})").exec(navigator.userAgent) != null)));
}

export function isSafari () {
  return /Safari/i.test(navigator.userAgent) && /Apple Computer/i.test(navigator.vendor);
}

export function isWebKit () {
  return /^((?!chrome|android).)*safari/i.test(window.navigator.userAgent);
}

// Platforms

export function isAndroid () {
  return /Android/i.test(navigator.userAgent);
}

export function isiOS () {
  return /iPad|iPhone|iPod/i.test(navigator.userAgent) && !window.MSStream;
}
