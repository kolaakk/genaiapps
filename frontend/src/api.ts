export type AnalyzeResponse = {
  request_id: string;
  analysis: {
    title: string;
    summary: string;
    risk_level: "low" | "medium" | "high";
    impacted_domains: string[];
    sensitive_data_involved: boolean;
    key_risks: string[];
    recommended_controls: { control_area: string; why: string }[];
    action_items: { title: string; owner_role: string; due_in_days: number }[];
    assumptions: string[];
  };
  related_policies: { policy_id: string; title: string; score: number; excerpt: string }[];
};

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const API_KEY = import.meta.env.VITE_APP_API_KEY || "";

export async function analyze(text: string, context?: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": API_KEY
    },
    body: JSON.stringify({ text, context })
  });

  if (!res.ok) {
    const msg = await res.text();
    throw new Error(`Backend error (${res.status}): ${msg}`);
  }

  return res.json();
}