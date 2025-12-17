import React, { useState } from "react";
import { register, login, plan } from "./api";

type TokenResp = { access_token: string; token_type?: string };

export default function App() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("pass1234");
  const [token, setToken] = useState("");
  const [text, setText] = useState(
    "Plan my week: gym Mon/Wed/Fri, finish thesis draft by Friday, call mom Sunday, buy groceries Saturday morning."
  );
  const [out, setOut] = useState<any>(null);
  const [err, setErr] = useState("");

  async function doRegister() {
    setErr(""); setOut(null);
    try {
      const t: TokenResp = await register(email, password);
      setToken(t.access_token);
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function doLogin() {
    setErr(""); setOut(null);
    try {
      const t: TokenResp = await login(email, password);
      setToken(t.access_token);
    } catch (e: any) {
      setErr(e.message);
    }
  }

  async function doPlan() {
    setErr(""); setOut(null);
    try {
      const o = await plan(token, text);
      setOut(o);
    } catch (e: any) {
      setErr(e.message);
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "40px auto", fontFamily: "ui-sans-serif, system-ui" }}>
      <h2>Smart Task Planner</h2>

      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", alignItems: "center" }}>
        <input style={{ padding: 8, minWidth: 220 }} value={email} onChange={(e) => setEmail(e.target.value)} placeholder="email" />
        <input style={{ padding: 8, minWidth: 220 }} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="password" type="password" />
        <button onClick={doRegister} style={{ padding: "8px 12px" }}>Register</button>
        <button onClick={doLogin} style={{ padding: "8px 12px" }}>Login</button>
      </div>

      <div style={{ marginTop: 10 }}>
        <div>
          Token: <code>{token ? token.slice(0, 28) + "..." : "(none)"}</code>
        </div>
      </div>

      <div style={{ marginTop: 16 }}>
        <label style={{ fontWeight: 600 }}>Plan text</label>
        <textarea
          style={{ width: "100%", height: 120, marginTop: 8, padding: 10 }}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button onClick={doPlan} disabled={!token} style={{ padding: "10px 14px" }}>
          Generate tasks
        </button>
      </div>

      {err && <pre style={{ color: "crimson", whiteSpace: "pre-wrap" }}>{err}</pre>}
      {out && (
        <pre style={{ background: "#f6f6f6", padding: 12, overflow: "auto" }}>
          {JSON.stringify(out, null, 2)}
        </pre>
      )}

      <div style={{ marginTop: 18, fontSize: 12, color: "#444" }}>
        Tip: if you want to configure the API base URL for the frontend, create <code>frontend/.env</code> with:
        <div><code>VITE_API_BASE=http://localhost:8000</code></div>
      </div>
    </div>
  );
}
