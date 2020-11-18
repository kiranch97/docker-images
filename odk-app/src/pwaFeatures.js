export function pwaDiscardDetection () {
  // If PWA was discarded (PWA was closed on users phone)
  if ("wasDiscarded" in document) {
    // Clear localStorage (to logout)
    localStorage.clear();
  }
}

export function pwaStateChangeDetection () {
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
  
  // Set current state of PWA
  var state = getState();

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
  
  // Add event listener
  ["pageshow", "focus", "blur", "visibilitychange", "resume"].forEach(function (type) {
    window.addEventListener(type, onPageStateChange, {capture: true});
  });
}