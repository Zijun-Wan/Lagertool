/**
 * fetchJson
 * A small helper to make HTTP requests and parse JSON responses.
 *
 * - Uses the native fetch API.
 * - Throws an Error if the HTTP status is not 2xx.
 * - Returns the parsed JSON body on success.
 *
 * @param {string} url - The endpoint to request.
 * @param {Object} [options] - Optional fetch configuration (method, headers, body, etc.).
 * @returns {Promise<any>} Parsed JSON from the response body.
 * @throws {Error} If the response status is not OK or if parsing fails.
 *
 * Example:
 * ```js
 * const data = await fetchJson('/api/data', { method: 'POST', body: JSON.stringify(payload) });
 * ```
 */

async function fetchJson(url, options = {}) {
  const res = await fetch(url, options);
  const isJson = (res.headers.get('content-type') || '').includes('application/json');
  const payload = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    const msg =
      (isJson && payload?.error) ||
      (typeof payload === 'string' && payload) ||
      'Request failed';
    const err = new Error(msg);
    err.status = res.status;
    err.payload = payload;
    throw err;  // throws the error for other handlers
  }

  return payload;  // happy path: parsed response
}
// try {
//   const me = await fetchJson('/api/me', { credentials: 'include' });
//   setUser(me);                                  // success
// } catch (err) {
//   if (err.status === 401) {                     // not authenticated
//     alert(err.message || 'Please log in first');
//     navigate('/login');
//   } else {
//     setError(err.message);                      // other errors
//   }
// }

export default fetchJson;
