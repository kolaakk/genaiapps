import React, { useState } from "react";
import { analyze, AnalyzeResponse } from "./api";

export default function App() {
  const [text, setText] = useState("");
  const [context, setContext] = useState("Netherlands retail banking | internal app");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const r = await analyze(text, context);
      setResult(r);
    } catch (err: any) {
      setError(err?.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="header">
        <h1>Policy Impact Analyzer</h1>
        <p>Paste a change request / incident / procedure. Get structured risk & control output + related policies.</p>
      </header>

      <main className="grid">
        <section className="card">
          <h2>Input</h2>
          <form onSubmit={onSubmit} className="form">
            <label>
              Context (optional)
              <input
                value={context}
                onChange={(e) => setContext(e.target.value)}
                placeholder="e.g., country, system, domain"
              />
            </label>

            <label>
              Text to analyze
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Example: We will enable a new vendor integration to process customer documents..."
                rows={12}
              />
            </label>

            <button disabled={loading || text.trim().length < 20}>
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </form>

          {error && <div className="error">⚠️ {error}</div>}
        </section>

        <section className="card">
          <h2>Output</h2>
          {!result && <div className="muted">No results yet.</div>}

          {result && (
            <>
              <div className="meta">
                <span><b>Request ID:</b> {result.request_id}</span>
                <span className={`pill ${result.analysis.risk_level}`}>
                  Risk: {result.analysis.risk_level.toUpperCase()}
                </span>
                {result.analysis.sensitive_data_involved && (
                  <span className="pill warn">Sensitive Data: YES</span>
                )}
              </div>

              <h3>{result.analysis.title}</h3>
              <p>{result.analysis.summary}</p>

              <h4>Impacted domains</h4>
              <ul>
                {result.analysis.impacted_domains.map((d, i) => <li key={i}>{d}</li>)}
              </ul>

              <h4>Key risks</h4>
              <ul>
                {result.analysis.key_risks.map((r, i) => <li key={i}>{r}</li>)}
              </ul>

              <h4>Recommended controls</h4>
              <ul>
                {result.analysis.recommended_controls.map((c, i) => (
                  <li key={i}>
                    <b>{c.control_area}</b>: {c.why}
                  </li>
                ))}
              </ul>

              <h4>Action items</h4>
              <ul>
                {result.analysis.action_items.map((a, i) => (
                  <li key={i}>
                    <b>{a.title}</b> — Owner: {a.owner_role} — Due: {a.due_in_days} days
                  </li>
                ))}
              </ul>

              <h4>Related policies (embeddings)</h4>
              <ul>
                {result.related_policies.map((p) => (
                  <li key={p.policy_id}>
                    <b>{p.policy_id} — {p.title}</b> (score: {p.score})<br/>
                    <span className="muted">{p.excerpt}</span>
                  </li>
                ))}
              </ul>

              {result.analysis.assumptions?.length > 0 && (
                <>
                  <h4>Assumptions / notes</h4>
                  <ul>
                    {result.analysis.assumptions.map((a, i) => <li key={i}>{a}</li>)}
                  </ul>
                </>
              )}
            </>
          )}
        </section>
      </main>

      <footer className="footer">
        <span>GenAI app • REST backend • Azure OpenAI</span>
      </footer>
    </div>
  );
}