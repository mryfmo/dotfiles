"""Throwaway probe for the official Sign in with ChatGPT route (plan 025 leg 1 step #S0).

Decides, with observed output, whether dynamic client registration + a Responses call
with store:false / stream:true works for this operator's ChatGPT account and a personal
local app, and which models the account lists. Tokens stay in memory and are never
printed or written. Run it OUTSIDE the agent sandbox (the operator's own terminal, e.g.
`! uv run --no-project siwc_probe.py`), because it binds 127.0.0.1 and opens a browser.

Sources (pasted 2026-10-23): developers.openai.com/siwc/token-sharing-open-source/{sign-in,
models-and-inference,preview-limitations,token-reference}.
"""

import argparse, base64, hashlib, http.server, json, os, secrets, sys, threading, time, urllib.parse, urllib.request, uuid, webbrowser

AUTHORIZE = "https://auth.openai.com/api/accounts/authorize"
# The token endpoint (SIWC docs "Token endpoint"). Named TOKEN_URL because the records sync masks a string
# assigned to a bare TOKEN name as a secret (validate-agent-assets.py SECRET_PATTERN), which had left this
# line a syntax error (U79).
TOKEN_URL = "https://auth.openai.com/api/accounts/oauth/token"
API = "https://api.openai.com/v1"
RESOURCE = API
SCOPES = "openid profile email offline_access resource.invoke chatgpt.tokens.use.direct"


def b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def pkce():
    verifier = b64url(secrets.token_bytes(48))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def authorize_url(port, host_id, name, state, nonce, challenge):
    q = {
        "response_type": "code",
        "client_id": "dynamic_agent_client",
        "redirect_uri": f"http://127.0.0.1:{port}/auth/callback",
        "scope": SCOPES,
        "resource": RESOURCE,
        "state": state,
        "nonce": nonce,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "ext_agent_host_id": host_id,
        "agent_name_hint": name,
    }
    return AUTHORIZE + "?" + urllib.parse.urlencode(q)


def wait_callback(port, timeout):
    got = {}
    done = threading.Event()

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            u = urllib.parse.urlparse(self.path)
            if u.path != "/auth/callback":  # lint-comparisons: allow the request target's exact route, no filesystem path
                self.send_response(404)
                self.end_headers()
                return
            got.update({k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()})
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"siwc probe: callback received, return to the terminal")
            done.set()

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", port), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    ok = done.wait(timeout)
    srv.shutdown()
    return got if ok else None


def post_form(url, data, timeout=30):
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read())


def get_json(url, token, timeout=30):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, json.loads(r.read())


def parse_sse(lines):
    """Yield (event_type, data_dict) from SSE text lines; tolerant of missing event: lines."""
    ev, buf = None, []
    for line in lines:
        line = line.rstrip("\r\n")
        if line.startswith("event:"):
            ev = line[6:].strip()
        elif line.startswith("data:"):
            buf.append(line[5:].strip())
        elif line == "" and buf:
            data = json.loads("\n".join(buf))
            yield (ev or data.get("type")), data
            ev, buf = None, []


def responses_call(token, model, prompt, instructions=None, timeout=120):
    body = {
        "model": model,
        "store": False,
        "stream": True,
        "input": [
            {"role": "user", "content": [{"type": "input_text", "text": prompt}]}
        ],
    }
    if instructions:
        body["instructions"] = instructions
    req = urllib.request.Request(
        API + "/responses",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    types, text, completed, rid = [], [], False, None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for ev, data in parse_sse(line.decode() for line in r):
            types.append(ev)
            if ev == "response.output_text.delta":
                text.append(data.get("delta", ""))
            if ev == "response.completed":
                completed = True
                rid = (data.get("response") or {}).get("id")
                usage = (data.get("response") or {}).get("usage")
                break
    return {
        "completed": completed,
        "event_types": sorted(set(types)),
        "n_events": len(types),
        "text": "".join(text)[:200],
        "response_id_present": bool(rid),
        "usage": usage if completed else None,
    }


def http_error_summary(e):
    body = e.read().decode(errors="replace")[:400] if hasattr(e, "read") else ""
    return f"HTTP {getattr(e, 'code', '?')}: {body}"


def listed_models(body):
    """The documented model list: a `models` array whose entries carry `slug` and `visibility`.

    developers.openai.com/siwc/llms-full.txt, "Models and inference" step 1:
    `jq '[.models[] | select(.visibility == "list") | {slug, display_name}]'`. #S0 read `data[].id`
    (the platform API's shape), which this route does not return, and so counted 0 (U79).
    """
    models = body.get("models", []) if isinstance(body, dict) else []
    listed = [m["slug"] for m in models if m.get("visibility") == "list"]
    return listed, len(models)


def selftest():
    v, c = pkce()
    assert len(v) >= 43 and c == b64url(hashlib.sha256(v.encode()).digest()), "pkce"
    u = urllib.parse.urlparse(authorize_url(1455, "h", "n", "s", "o", c))
    q = urllib.parse.parse_qs(u.query)
    assert q["client_id"] == ["dynamic_agent_client"] and q["redirect_uri"] == [
        "http://127.0.0.1:1455/auth/callback"
    ], "authorize url"
    assert "chatgpt.tokens.use.direct" in q["scope"][0] and q["resource"] == [
        RESOURCE
    ], "scopes/resource"
    sample = [
        "event: response.created",
        'data: {"type":"response.created"}',
        "",
        "event: response.output_text.delta",
        'data: {"type":"response.output_text.delta","delta":"OK"}',
        "",
        "event: response.completed",
        'data: {"type":"response.completed","response":{"id":"resp_1","usage":{"total_tokens":3}}}',
        "",
    ]
    evs = list(parse_sse(sample))
    assert [e for e, _ in evs] == [
        "response.created",
        "response.output_text.delta",
        "response.completed",
    ], "sse"
    documented = {
        "models": [
            {"slug": "gpt-6.1-sol", "display_name": "GPT-6.1 Sol", "visibility": "list"},
            {"slug": "gpt-reserve", "display_name": "Reserve", "visibility": "hide"},
        ]
    }
    assert listed_models(documented) == (["gpt-6.1-sol"], 2), "models"
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=1455)
    ap.add_argument("--name", default="omp-dotfiles-probe")
    ap.add_argument(
        "--model",
        default=None,
        help="default: first listed model, preferring gpt-6.1-sol",
    )
    ap.add_argument("--prompt", default="Reply with the single word PONG.")
    ap.add_argument(
        "--test-instructions",
        action="store_true",
        help="second call with an `instructions` field",
    )
    ap.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="seconds to wait for the browser callback",
    )
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return 0

    report = {"started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    verifier, challenge = pkce()
    # The sign-in page's sample credential shows the host id as "urn:uuid:..."; a bare uuid was
    # refused with invalid_authorize_request (param ext_agent_host_id) on 2026-10-23.
    state, nonce, host_id = (
        secrets.token_urlsafe(24),
        secrets.token_urlsafe(24),
        "urn:uuid:" + str(uuid.uuid4()),
    )
    try:
        probe_sock = http.server.HTTPServer(
            ("127.0.0.1", a.port), http.server.BaseHTTPRequestHandler
        )
        probe_sock.server_close()
    except OSError:
        tmp = http.server.HTTPServer(
            ("127.0.0.1", 0), http.server.BaseHTTPRequestHandler
        )
        a.port = tmp.server_address[1]
        tmp.server_close()
        print(
            f"[0] port 1455 busy (an earlier probe may still be waiting); using 127.0.0.1:{a.port}",
            flush=True,
        )
    url = authorize_url(a.port, host_id, a.name, state, nonce, challenge)
    print(
        f"[1] open this URL in the browser (also trying webbrowser.open):\n{url}\n",
        flush=True,
    )
    try:
        webbrowser.open(url)
    except Exception:
        pass
    cb = wait_callback(a.port, a.timeout)
    if not cb:
        print("FAIL: no callback within timeout")
        return 2
    report["callback_keys"] = sorted(cb.keys())
    if cb.get("state") != state:
        print("FAIL: state mismatch")
        return 2
    if "error" in cb:
        print(
            f"FAIL: authorize error={cb.get('error')} description={cb.get('error_description', '')[:200]}"
        )
        return 2
    client_id = cb.get("client_id")
    report["issued_client_id_present"] = bool(client_id)
    report["issued_client_id_prefix"] = (client_id or "")[:6]
    try:
        status, tok = post_form(
            TOKEN_URL,
            {
                "grant_type": "authorization_code",
                "client_id": client_id,
                "code": cb["code"],
                "code_verifier": verifier,
                "redirect_uri": f"http://127.0.0.1:{a.port}/auth/callback",
                "resource": RESOURCE,
            },
        )
    except urllib.error.HTTPError as e:
        print("FAIL token exchange:", http_error_summary(e))
        return 3
    access = tok.get("access_token", "")
    report["token"] = {
        "status": status,
        "expires_in": tok.get("expires_in"),
        "scope": tok.get("scope"),
        "has_refresh": bool(tok.get("refresh_token")),
        "has_id_token": bool(tok.get("id_token")),
        "access_len": len(access),
    }
    granted = (tok.get("scope") or "").split()
    report["plan_usage_scope_granted"] = "chatgpt.tokens.use.direct" in granted
    try:
        _, models = get_json(API + "/models", access)
        listed, total = listed_models(models)
        report["models_listed"] = listed
        report["models_total"] = total
        # Top-level keys only, never values: the shape a parser change would need.
        report["models_keys"] = sorted(models) if isinstance(models, dict) else type(models).__name__
    except urllib.error.HTTPError as e:
        report["models_error"] = http_error_summary(e)
        listed = []
    model = a.model or (
        "gpt-6.1-sol"
        if "gpt-6.1-sol" in listed
        else (listed[0] if listed else "gpt-6.1-sol")
    )
    report["model_used"] = model
    try:
        report["responses"] = responses_call(access, model, a.prompt)
    except urllib.error.HTTPError as e:
        report["responses_error"] = http_error_summary(e)
    if a.test_instructions and "responses" in report:
        try:
            report["responses_with_instructions"] = responses_call(
                access, model, a.prompt, instructions="Answer in uppercase only."
            )
        except urllib.error.HTTPError as e:
            report["responses_with_instructions_error"] = http_error_summary(e)
    del access, tok
    report["note"] = (
        "tokens discarded; the registered agent appears in the ChatGPT account under the name given by --name"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("responses", {}).get("completed") else 4


if __name__ == "__main__":
    sys.exit(main())
