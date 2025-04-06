import React, { useState, useEffect } from "react";

function App() {
  const [tab, setTab] = useState("dashboard");
  const [releases, setReleases] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [chatResponse, setChatResponse] = useState("");

  useEffect(() => {
    fetch("/api/releases")
      .then((res) => res.json())
      .then((data) => setReleases(data));
  }, []);

  const simulateIncident = async () => {
    const res = await fetch("/api/simulate-incident", { method: "POST" });
    const data = await res.json();
    setIncidents([data, ...incidents]);
  };

  const sendMessage = async () => {
    const msg = document.getElementById("user-msg").value;
    const res = await fetch("/api/ai-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });
    const data = await res.json();
    setChatResponse(data.response);
  };

  return (
    <div className="p-4 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">🚀 Enginuity AI Nexus</h1>

      <div className="flex space-x-4 mb-4">
        {["dashboard", "release", "incident", "greenops", "chat"].map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className="bg-gray-200 px-4 py-2 rounded"
          >
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      {tab === "dashboard" && (
        <div>
          <p>Welcome to Enginuity AI. Use the tabs above to explore your DevOps insights.</p>
          <a
            href="/api/export-pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block mt-4 bg-green-600 text-white px-4 py-2 rounded"
          >
            📄 Export Report to PDF
          </a>
        </div>
      )}

      {tab === "release" && (
        <div>
          <h2 className="text-xl font-semibold">Release DNA</h2>
          <pre>{JSON.stringify(releases, null, 2)}</pre>
        </div>
      )}

      {tab === "incident" && (
        <div>
          <h2 className="text-xl font-semibold">Incidents</h2>
          <button
            onClick={simulateIncident}
            className="bg-red-600 text-white px-3 py-1 rounded my-2"
          >
            Simulate Incident
          </button>
          <div>
            {incidents.map((i, idx) => (
              <pre key={idx}>{JSON.stringify(i, null, 2)}</pre>
            ))}
          </div>
        </div>
      )}

      {tab === "greenops" && (
        <div>
          <h2 className="text-xl font-semibold">GreenOps</h2>
          <p>
            Carbon cost for last release:{" "}
            {releases[0]?.carbon_cost ?? "Loading..."} kgCO₂
          </p>
        </div>
      )}

      {tab === "chat" && (
        <div>
          <h2 className="text-xl font-semibold">AI Chat Copilot</h2>
          <input
            id="user-msg"
            type="text"
            className="border p-2 w-full"
            placeholder="Ask something..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-600 text-white px-4 py-2 mt-2 rounded"
          >
            Send
          </button>
          <pre className="mt-3 bg-gray-100 p-2">{chatResponse}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

