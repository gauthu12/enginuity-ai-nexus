from flask import Flask, jsonify, request, render_template, send_file
import random
import datetime
import io
from fpdf import FPDF

app = Flask(__name__)

# --- Simulated Data ---
releases = [
    {
        "id": f"rel-2025-{i:03}",
        "author": random.choice(["alice", "bob", "carol"]),
        "tests_passed": random.randint(40, 50),
        "tests_failed": random.randint(0, 5),
        "risk_score": round(random.uniform(0.3, 0.9), 2),
        "carbon_cost": round(random.uniform(1.0, 2.0), 2),
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat(),
        "summary": f"Release {i} includes performance and security fixes"
    } for i in range(1, 6)
]

incidents = []

# --- Utility Function ---
def simulate_incident():
    related_release = random.choice(releases)
    incident = {
        "id": f"inc-{random.randint(1000, 9999)}",
        "release_id": related_release['id'],
        "detected_at": datetime.datetime.now().isoformat(),
        "summary": "CPU spike detected in service",
        "root_cause": "Memory leak introduced in caching layer",
        "resolved": True,
        "postmortem": f"Incident linked to {related_release['id']}. Root cause identified as memory leak. Fix deployed by {related_release['author']}."
    }
    incidents.append(incident)
    return incident

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/releases')
def get_releases():
    return jsonify(releases)

@app.route('/api/incidents')
def get_incidents():
    return jsonify(incidents)

@app.route('/api/simulate-incident', methods=['POST'])
def post_simulate_incident():
    incident = simulate_incident()
    return jsonify(incident)

@app.route('/api/ai-chat', methods=['POST'])
def ai_chat():
    user_input = request.json.get("message", "").lower()
    response = "I'm your DevOps AI. Ask about incidents, carbon cost, or deployments."
    if "deployment" in user_input:
        response = "Last deployment included updates to 3 services and triggered a minor incident."
    elif "incident" in user_input:
        response = "The last incident was due to a memory leak in the caching layer, now resolved."
    elif "carbon" in user_input:
        avg = sum(r['carbon_cost'] for r in releases) / len(releases)
        response = f"Average carbon cost across releases is {avg:.2f} kgCO₂. Consider reducing cold starts."
    return jsonify({"response": response})

@app.route('/api/export-pdf')
def export_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Enginuity AI Nexus Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt="Recent Releases:", ln=True)
    for r in releases:
        pdf.multi_cell(0, 10, txt=f"{r['id']} by {r['author']} | Risk: {r['risk_score']} | Carbon: {r['carbon_cost']} kgCO₂")

    pdf.ln(10)
    pdf.cell(200, 10, txt="Incidents:", ln=True)
    for i in incidents:
        pdf.multi_cell(0, 10, txt=f"{i['id']} | {i['summary']} | Resolved: {i['resolved']}\nPostmortem: {i['postmortem']}")

    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="enginuity_report.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
