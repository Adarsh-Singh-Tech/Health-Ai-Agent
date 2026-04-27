from flask import Flask, render_template, request, send_file
import os
import fitz
from docx import Document
import matplotlib

# FIX: No GUI backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import re
import markdown

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from openai import OpenAI

app = Flask(__name__)

# ===== CONFIG =====
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = "openrouter/auto"


# ===== SAFE AI CALL =====
def safe_ai_call(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        if response and response.choices:
            return response.choices[0].message.content

        return "⚠️ AI response empty"

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


# ===== TEXT EXTRACTION =====
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return " ".join([page.get_text() for page in doc])

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


# ===== VALUE EXTRACTION =====
def extract_values(text):
    values = {}

    patterns = {
        "Hemoglobin": r"Hemoglobin\s*[:=]?\s*(\d+\.?\d*)",
        "Glucose": r"Glucose\s*[:=]?\s*(\d+\.?\d*)",
        "Cholesterol": r"Cholesterol\s*[:=]?\s*(\d+\.?\d*)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            values[key] = float(match.group(1))

    return values


# ===== MULTI-AGENT =====
def analyze_report(text):

    extractor = safe_ai_call(f"Extract medical values:\n{text}")

    interpreter = safe_ai_call(f"""
Format into clean report:

## SUMMARY
## KEY FINDINGS
## ABNORMAL VALUES
## NORMAL VALUES

DATA:
{extractor}
""")

    risk = safe_ai_call(f"""
Give:

## RISK LEVEL
## WHY

DATA:
{extractor}
""")

    advice = safe_ai_call("""
Give:

## DIET
## EXERCISE
## FOLLOW-UP
## SUPPLEMENTS
""")

    return extractor, interpreter, risk, advice


# ===== PIE CHART =====
def generate_pie(values):
    path = "static/pie.png"

    if not values:
        return None

    labels = list(values.keys())
    sizes = list(values.values())

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Health Distribution")
    plt.savefig(path)
    plt.close()

    return path


# ===== LINE CHART =====
def generate_line(values):
    path = "static/line.png"

    if not values:
        return None

    labels = list(values.keys())
    sizes = list(values.values())

    plt.figure()
    plt.plot(labels, sizes, marker='o')
    plt.title("Health Trend")
    plt.savefig(path)
    plt.close()

    return path


# ===== PDF =====
def generate_pdf(text):
    path = "static/report.pdf"

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    content = []
    for line in text.split("\n"):
        content.append(Paragraph(line, styles["Normal"]))

    doc.build(content)

    return path


# ===== ROUTE =====
@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["file"]
        path = os.path.join("uploads", file.filename)
        file.save(path)

        raw_text = extract_text(path)

        extractor, interpreter, risk, advice = analyze_report(raw_text)

        values = extract_values(raw_text)

        pie = generate_pie(values)
        line = generate_line(values)

        interpreter_html = markdown.markdown(interpreter)
        risk_html = markdown.markdown(risk)
        advice_html = markdown.markdown(advice)

        pdf = generate_pdf(interpreter + "\n\n" + risk + "\n\n" + advice)

        return render_template(
            "index.html",
            interpreter=interpreter_html,
            risk=risk_html,
            advice=advice_html,
            pie=pie,
            line=line,
            pdf=pdf
        )

    return render_template("index.html")


@app.route("/download")
def download():
    return send_file("static/report.pdf", as_attachment=True)


if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)