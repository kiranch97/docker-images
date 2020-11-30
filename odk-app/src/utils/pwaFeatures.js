export function pwaDiscardDetection () {
  // Frist, check if user uses PWA
  const checkMedia = window.matchMedia("(display-mode: standalone)").matches;
  if (!checkMedia) {
    return;
  }

  // If PWA was discarded (PWA was closed on users phone)
  if ("wasDiscarded" in document) {
    // Clear localStorage (to logout)
    console.log("App was discarded");
    localStorage.clear();
  }
}

// ----

export function pwaStateChangeDetection () {
  // Frist, check if user uses PWA
  const checkMedia = window.matchMedia("(display-mode: standalone)").matches;
  if (!checkMedia) {
    return;
  }

  // Set current state of PWA
  var state = getState();
  
  // Add event listener
  ["pageshow", "focus", "blur", "visibilitychange", "resume"].forEach(function (type) {
    window.addEventListener(type, onPageStateChange, {capture: true});
  });

  // Get current state of PWA
  function getState () {
    if (document.visibilityState === "hidden") {
      return "hidden";
    }
    if (document.hasFocus()) {
      return "focused";
    }
    return "not focused";
  }

  // Log change state
  function logStateChange (nextState) {
    var prevState = state;
    if (nextState !== prevState) {
      var newLog = " State changed from " + prevState + " to " + nextState + ".";
      console.log(newLog);
      state = nextState;
    }
  }

  // Do x when state changes
  function onPageStateChange () {
    logStateChange(getState());
  }
}