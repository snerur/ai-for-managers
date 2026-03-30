# AI for Managers — Interactive Tutorial

An interactive tutorial on Artificial Intelligence designed for **non-technical managers and business leaders**. Built by **Sridhar Nerur** using **Claude** (Anthropic).

The application is built with **Streamlit** — run it with a single command, no web server configuration required.

---

## Overview

This tutorial demystifies AI through clear explanations, visual diagrams, real-world business examples, and interactive quizzes — no prior technical background required. An embedded AI tutor (powered by OpenAI or Groq) answers questions in plain business language throughout the learning experience.

---

## Modules

| # | Module | Topics Covered |
|---|--------|----------------|
| 1 | **Introduction to AI** | Definitions (AI, ML, Deep Learning, GenAI), brief history from 1950 to present, opportunities and challenges across industries |
| 2 | **Supervised Learning** | Regression vs. classification, common algorithms, real-world business applications |
| 3 | **Unsupervised Learning** | Clustering, anomaly detection, association rules, dimensionality reduction |
| 4 | **Reinforcement Learning** | Agents, environments, rewards, policies, real-world examples (AlphaGo, robotics, recommendations) |
| 5 | **LLMs & Generative AI** | How large language models work, transformer architecture, AI assistants vs. agents, multi-agent systems, ethical concerns |
| 6 | **Basics of Prompting** | Zero-shot, few-shot, chain-of-thought, and role prompting; prompt engineering best practices for business users |
| 7 | **AI Use Cases** | Industry-by-industry overview of AI applications across healthcare, finance, retail, manufacturing, and more |
| 8 | **AI Ethics & Governance** | Ethical theories, real-world AI failures, NIST AI RMF, EU AI Act, OECD principles, LLM-specific concerns |
| 9 | **Organizational Readiness** | AI maturity models, becoming an AI-first organization, the AI Center of Excellence |
| 10 | **References** | Textbooks, landmark research papers, governance frameworks, journalism and case studies |

Each module includes:
- Inline **SVG diagrams** and visual explainers
- **Real-world business examples**
- A **5-question interactive quiz** with per-question feedback and explanations

---

## Features

- **Three AI tutor access modes** — choose the option that fits your situation:
  - **Demo mode** — no API key needed (enabled by setting a key in `.env`)
  - **OpenAI** — use your own key; supports `gpt-4o-mini` (free tier) and `gpt-4o` (paid)
  - **Groq (free)** — use a free Groq API key; no payment required, powered by Llama 3.1
- **Context-aware AI tutor** — knows which module you are studying and tailors responses accordingly
- **Progress tracking** — sidebar shows completion percentage and per-module checkmarks
- **Sidebar navigation** — jump to any module or the References page instantly
- **Inline quizzes** — one question at a time with immediate correct/incorrect feedback, explanations, and a score screen with retake option
- **Split-view chat** — toggle the AI tutor alongside the content without leaving the page

---

## Prerequisites

- Python 3.9 or higher
- `pip` (Python package manager)
- An internet connection (to load fonts from Google Fonts CDN)
- An API key from **OpenAI** or **Groq** to use the AI tutor (optional — see Access Modes below)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/snerur/ai-for-managers.git
cd ai-for-managers
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Configure a server-side demo key

If you want users to access the AI tutor without entering their own API key, copy the example environment file and add your key:

```bash
cp .env.example .env
```

Then open `.env` and fill in one of the following:

```env
# Option A — OpenAI (uses gpt-4o-mini)
OPENAI_API_KEY=sk-proj-...

# Option B — Groq (completely free tier)
GROQ_API_KEY=gsk_...
```

If neither key is set, the AI tutor is still fully functional — users simply enter their own key in the Settings panel.

### 4. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

Streamlit will automatically open the app in your default browser at `http://localhost:8501`.

---

## Getting an API Key

### OpenAI (Free Tier or Paid)

1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to **API keys** → **Create new secret key**
4. New accounts receive free usage credits — no payment needed to get started
5. For more usage, add a payment method and select `gpt-4o` in Settings

### Groq (Completely Free — No Payment Required)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account (no credit card required)
3. Go to **API Keys** → **Create API Key**
4. Paste the key into the tutorial's Settings panel in the sidebar

---

## Using the AI Tutor

1. In the sidebar, click **⚙️ AI Tutor Settings** to expand the settings panel
2. Choose your access mode:
   - **Free Demo** — appears automatically if a server-side key is configured in `.env`
   - **OpenAI** — paste your `sk-...` key; select `gpt-4o-mini` (free tier) or `gpt-4o` (paid)
   - **Groq (Free)** — paste your `gsk_...` key; uses Llama 3.1 at no cost
3. Click **💬 Ask AI Tutor** in the sidebar to open the chat panel alongside the current module
4. Ask any question about the material — the tutor knows which module you are viewing and responds in plain business language

> **Privacy note:** API keys are stored only in Streamlit's session state for the duration of your browser session. They are never written to disk or logged on the server.

---

## Project Structure

```
ai-for-managers/
├── streamlit_app.py        # Streamlit application — all modules, quizzes, chat, and settings
├── app.py                  # Original Flask version (still functional)
├── requirements.txt        # Python dependencies
├── .env.example            # Template for server-side demo key configuration
├── .gitignore
├── templates/
│   └── index.html          # Flask SPA — all 9 modules, quizzes, diagrams
└── static/
    ├── style.css           # CSS for the Flask version
    └── app.js              # JavaScript for the Flask version
```

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | Python · Streamlit |
| AI Providers | OpenAI API (`gpt-4o-mini`, `gpt-4o`) · Groq API (`llama-3.1-8b-instant`) |
| Diagrams | Inline SVG (rendered via `unsafe_allow_html`) |
| Typography | Inter (Google Fonts) |
| State Management | Streamlit `session_state` |

---

## References

A full bibliography is available in the **References** module (Section 10) within the tutorial. Key sources include:

**Textbooks**
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
- O'Neil, C. (2016). *Weapons of Math Destruction*. Crown.

**Governance Frameworks**
- NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*. U.S. Department of Commerce.
- European Parliament (2024). *EU Artificial Intelligence Act*.
- OECD (2024). *Recommendation of the Council on Artificial Intelligence*.

**Landmark Research**
- Vaswani et al. (2017). Attention Is All You Need. *NeurIPS*.
- Silver et al. (2016). Mastering the game of Go with deep neural networks. *Nature*.
- Linden, G., Smith, B., & York, J. (2003). Amazon.com Recommendations: Item-to-Item Collaborative Filtering. *IEEE Internet Computing*.
- Buolamwini & Gebru (2018). Gender Shades. *FAT Conference*.

**Journalism & Case Studies**
- Angwin et al. (2016). Machine Bias. *ProPublica*.
- Dastin, J. (2018). Amazon scraps secret AI recruiting tool that showed bias against women. *Reuters*.

---

## License

This project is released for **educational use**. You are welcome to use, share, and adapt the material with attribution.

---

## Author

**Sridhar Nerur**
Built with [Claude](https://claude.ai) (Anthropic)

---

*For issues or suggestions, please open a GitHub issue at [github.com/snerur/ai-for-managers](https://github.com/snerur/ai-for-managers).*
