export async function fetchEndpoint (endpoint, fetchMethod, headers, params) {
  // DATA
  let fullEndpoint = process.env.VUE_APP_API_HTTP_URL + endpoint;
  const auth = {
    Authorization: `Bearer ${localStorage.accessToken}`,
  };
  let fetchObject = {
    method: fetchMethod,
  };

  // Check if there are params given
  if (params) {
    if (fetchMethod == "GET" || fetchMethod == "DELETE") {
      fullEndpoint = fullEndpoint + params;
    } else {
      const fetchObjectBody = {
        body: params,
      };
      fetchObject = { ...fetchObject, ...fetchObjectBody };
    }
  }

  // Check if headers must be added
  if (headers) {
    const fetchObjectHeaders = {
      headers: auth,
    };
    fetchObject = { ...fetchObject, ...fetchObjectHeaders };
  }

  // ----

  // Fetch function - start
  async function getData (fullEndpoint, fetchObject) {
    // Fetch
    const res = await fetch(fullEndpoint, fetchObject);

    // Fetched correctly without errors
    if (res.ok) {
      const contentType = res.headers.get("Content-Type");

      // Define Content-Type
      if (contentType && contentType == "application/json") {
        return await res.json();
      } else if (contentType && contentType.includes("image")) {
        return await res.blob();
      } else {
        console.log("Content-Type not supported yet!");
      }
    }

    // If fetched with errors
    // Get error from backend
    let errorRes = await res.json();

    // If no error response from backend given,
    // give general error response
    if (!errorRes) {
      errorRes = {
        "detail": {
          "loc": ["api"],
          "msg": "An error has occured. If this error keeps occuring, contact administrator.",
          "status_code": res.status,
        },
      };
    }

    // Log error
    console.log(errorRes);

    // Return error response
    return errorRes;
  }

  // ----

  // Start fetch and return data
  return await getData(fullEndpoint, fetchObject);
}