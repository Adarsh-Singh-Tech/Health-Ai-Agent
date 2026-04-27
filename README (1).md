# 🩺 AI Health Report Analyzer

> An intelligent, Flask-based healthcare assistant that analyzes uploaded medical reports, extracts key insights, generates structured health summaries, visualizes health data, and produces downloadable PDF reports — powered by LLMs via the OpenRouter API.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-purple)](https://openrouter.ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE.md)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange)](VERSION.md)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Challenges & Solutions](#challenges--solutions)
- [Future Improvements](#future-improvements)
- [Versioning](#versioning)
- [License](#license)

---

## Overview

**AI Health Report Analyzer** is a production-ready web application that allows users to upload their medical reports (PDF or DOCX format) and receive a structured, AI-generated health analysis within seconds.

The application leverages a **single-call AI architecture** to extract text from uploaded reports, analyze it through a large language model, and return a clean, formatted health summary — complete with risk assessments, actionable recommendations, and visualized health data. The analysis can then be downloaded as a formatted PDF report.

This project is designed for personal health awareness use-cases and serves as a foundation for more advanced healthcare AI tooling.

---

## Features

- **📂 Multi-format Upload** — Accepts both PDF and DOCX medical reports
- **🧠 AI-Powered Analysis** — Single optimized LLM call for fast, accurate health insights
- **📋 Structured Output** — Organized sections: Summary, Findings, Risk Level, and Action Plan
- **📊 Data Visualization** — Automatically generated pie charts and line charts from report data
- **📄 PDF Export** — Download a professionally formatted PDF of the AI-generated analysis
- **🖥️ Clean Dashboard UI** — Responsive HTML/CSS frontend with a minimal, intuitive interface
- **🛡️ Robust Error Handling** — Graceful fallbacks for API failures, malformed input, and token limit errors

---

## Architecture

The application follows a lean, single-call architecture optimized for speed and cost efficiency.

```
User Upload (PDF/DOCX)
        │
        ▼
Text Extraction Layer
   ├── PyMuPDF  (PDF)
   └── python-docx (DOCX)
        │
        ▼
Input Preprocessing
   └── Text trimming + sanitization
        │
        ▼
AI Analysis (Single Call)
   └── OpenRouter API → LLM
       └── Structured Prompt → Structured Response
        │
        ▼
Output Processing
   ├── Health Summary Parser
   ├── Chart Generator (matplotlib)
   └── PDF Generator (reportlab)
        │
        ▼
Dashboard Render + Download
```

**Key Design Decision:** The original multi-agent pipeline (multiple sequential API calls) was replaced with a **single-call architecture** that includes a structured prompt template. This reduced latency significantly and eliminated cascading API failure risks.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask (Python) |
| AI / LLM | OpenRouter API |
| PDF Extraction | PyMuPDF (fitz) |
| DOCX Extraction | python-docx |
| Chart Generation | matplotlib (Agg backend) |
| PDF Generation | reportlab |
| Markdown Rendering | markdown / flask-markdown |
| Frontend | HTML5 + CSS3 |

---

## Installation

### Prerequisites

- Python 3.10 or higher
- An active [OpenRouter API key](https://openrouter.ai/)
- `pip` (Python package manager)

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/your-username/ai-health-report-analyzer.git
cd ai-health-report-analyzer
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
FLASK_ENV=development
FLASK_DEBUG=1
```

**5. Run the application**

```bash
flask run
```

The app will be available at `http://127.0.0.1:5000`.

---

## Usage

1. Open the application in your browser at `http://127.0.0.1:5000`
2. Click **Upload Report** and select a `.pdf` or `.docx` medical file
3. Click **Analyze** to trigger the AI analysis
4. Review the structured health summary on the dashboard:
   - **Summary** — High-level overview of the report
   - **Key Findings** — Extracted medical observations
   - **Risk Assessment** — Flagged concerns and severity
   - **Action Plan** — Suggested next steps
5. View the auto-generated **pie chart** and **line chart** for visual data representation
6. Click **Download PDF Report** to save a formatted copy of the analysis

---

## Screenshots

> 📸 Screenshots will be added after the UI finalization phase.

| View | Description |
|---|---|
| `dashboard.png` | Main upload dashboard |
| `analysis.png` | Structured health analysis output |
| `charts.png` | Pie + line chart visualizations |
| `pdf_export.png` | Sample downloaded PDF report |

---

## Challenges & Solutions

| Challenge | Root Cause | Solution Implemented |
|---|---|---|
| Slow response time | Multiple sequential API calls | Consolidated to a single optimized AI call |
| 402 Token Limit Error | OpenRouter token cap exceeded | Added `max_tokens=500–600` limit + input text trimming |
| Matplotlib crash on macOS | GUI threading conflict | Switched to `matplotlib.use('Agg')` non-interactive backend |
| Unstructured AI output | Freeform LLM responses | Designed strict structured prompt templates |
| App crashes on API failure | Unhandled exceptions | Implemented `safe_ai_call()` wrapper with fallback responses |

---

## Future Improvements

The roadmap for upcoming versions is fully documented in [VERSION.md](VERSION.md).

High-priority improvements planned:

- AI-based JSON extraction for accurate, dynamic charting
- Database integration for user history and report tracking
- Authentication system (user accounts)
- Async processing for non-blocking UX
- Cloud deployment on Render or Railway
- Advanced analytics with trend comparison across reports
- Doctor recommendation engine
- Multi-language report support

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/).

Current version: **v1.0.0**

See the full changelog and roadmap in [VERSION.md](VERSION.md).

---

## License

This project is licensed under the **MIT License**.

See [LICENSE.md](LICENSE.md) for the full license text.

---

<p align="center">Built with ❤️ for better health awareness through AI</p>
