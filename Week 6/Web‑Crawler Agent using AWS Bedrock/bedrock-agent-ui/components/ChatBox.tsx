"use client";

import { useState } from "react";

export default function ChatBox() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    setResponse("");

    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();
    setResponse(data.answer || data.error);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 800, margin: "40px auto" }}>
      <h1>🧠 Bedrock Web Crawler Agent</h1>

      <textarea
        rows={4}
        style={{ width: "100%", padding: 10 }}
        placeholder="Paste a URL and ask something (e.g. summarize)"
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />

      <button
        onClick={sendMessage}
        disabled={loading}
        style={{ marginTop: 10, padding: "10px 20px" }}
      >
        {loading ? "Thinking..." : "Ask Agent"}
      </button>

      {response && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>
          <h3>Response</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
