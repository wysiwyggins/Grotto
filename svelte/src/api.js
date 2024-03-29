const base = "/api/";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function send({ method, path, data }) {
  const fetch = window.fetch;
  const opts = { method, headers: {} };

  if (data) {
    opts.headers["Content-Type"] = "application/json";
    opts.headers["X-CSRFToken"] = getCookie("csrftoken");
    opts.body = JSON.stringify(data);
  }
  let url = `${base}${path}`;
  return await fetch(url, opts)
    .then((r) => r.text())
    .then((json) => {
      try {
        return JSON.parse(json);
      } catch (err) {
        throw "Bad response";
      }
    })
    .catch((e) => {
      console.log(`[${e}]: ${url} with ${JSON.stringify(opts)} failed`);
      throw "Bad response";
    });
}

export function get(path) {
  return send({ method: "GET", path });
}

export function del(path) {
  return send({ method: "DELETE", path });
}

export function post(path, data) {
  return send({ method: "POST", path, data });
}

export function put(path, data) {
  return send({ method: "PUT", path, data });
}

export function patch(path, data) {
  return send({ method: "PATCH", path, data });
}
