export function checkLoggedIn () {
  // Return true if user is logged in
  if (localStorage.userType && localStorage.userType === "demo" || localStorage.userType && localStorage.userType === "worker") {
    return true;
  }
  return false;
}