# AI for Managers — Interactive Tutorial

An interactive, browser-based tutorial on Artificial Intelligence designed for **non-technical managers and business leaders**. Built by **Sridhar Nerur** using **Claude** (Anthropic).

---

## Overview

This tutorial demystifies AI through clear explanations, visual diagrams, real-world business examples, and interactive quizzes — no prior technical background required. An embedded AI tutor (powered by OpenAI or Groq) answers questions in plain business language throughout the learning experience.

---

## Modules

| # | Module | Topics Covered |
|---|--------|---------------|
| 1 | **Introduction to AI** | Definitions (AI, ML, Deep Learning, GenAI), brief history from 1950 to present, opportunities and challenges across industries |
| 2 | **Supervised Learning** | Regression vs. classification, common algorithms, real-world business applications |
| 3 | **Unsupervised Learning** | Clustering, anomaly detection, association rules, dimensionality reduction |
| 4 | **Reinforcement Learning** | Agents, environments, rewards, policies, real-world examples (AlphaGo, robotics, recommendations) |
| 5 | **AI Ethics & Governance** | Ethical theories, real-world AI failures, NIST AI RMF, EU AI Act, OECD principles, LLM-specific concerns |
| 6 | **Organizational Readiness** | AI maturity models, becoming an AI-first organization, the AI Center of Excellence |
| 7 | **References** | Textbooks, landmark research papers, governance frameworks, journalism and case studies |

Each module includes:
- Inline **SVG diagrams** and visual explainers
- **Real-world business examples**
- A **5-question interactive quiz** with immediate feedback and explanations

---

## Features

- **Three AI tutor access modes** — choose the option that fits your situation:
  - **Demo mode** — no API key needed (enabled by the server owner via `.env`)
  - **OpenAI** — use your own key; supports the free tier (`gpt-4o-mini`) and paid models (`gpt-4o`)
  - **Groq (free)** — use a free Groq API key; no payment required, powered by Llama 3.1
- **Context-aware AI tutor** — knows which module you are studying and tailors responses accordingly
- **Progress tracking** — sidebar shows completion status across all modules
- **Smooth single-page navigation** with collapsible sidebar
- **Fully responsive** — works on desktop and mobile browsers

---

## Prerequisites

- Python 3.9 or higher
- `pip` (Python package manager)
- An internet connection (to load fonts and icons from CDN)
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

If you want visitors to use the AI tutor without entering their own API key, copy the example environment file and add your key:

```bash
cp .env.example .env
```

Then open `.env` in a text editor and fill in one of the following:

```env
# Option A — OpenAI (uses gpt-4o-mini)
OPENAI_API_KEY=sk-proj-...

# Option B — Groq (completely free tier)
GROQ_API_KEY=gsk_...
```

If neither key is set, the AI tutor is still fully functional — users simply enter their own key in the Settings panel.

### 4. Start the server

```bash
python app.py
```

### 5. Open in your browser

```
http://localhost:5000
```

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
4. Paste the key into the tutorial's Settings panel under the **Groq (Free)** tab

---

## Using the AI Tutor

1. Click the **⚙ Settings** button in the top-right corner of the header
2. Choose your access mode:
   - **Free Demo** — appears automatically if the server owner has configured a key in `.env`
   - **OpenAI** — paste your `sk-proj-...` key; select Free Tier (`gpt-4o-mini`) or Paid (`gpt-4o`)
   - **Groq (Free)** — paste your `gsk_...` key; uses Llama 3.1 at no cost
3. Click **Save & Connect**
4. Click the **💬 Ask AI** button (or the chat bubble in the bottom-right corner) at any time to ask questions about the current module

> **Privacy note:** API keys are stored in your browser's `sessionStorage` only. They are never logged or stored on the server and are automatically cleared when you close the browser tab.

---

## Project Structure

```
ai-for-managers/
├── app.py                  # Flask server — routes, OpenAI/Groq API proxy
├── requirements.txt        # Python dependencies
├── .env.example            # Template for server-side demo key configuration
├── .gitignore
├── templates/
│   └── index.html          # Single-page application — all 7 modules, quizzes, diagrams
└── static/
    ├── style.css           # Custom CSS — layout, components, quiz, chat, modals
    └── app.js              # Navigation, quiz engine, chat client, settings logic
```

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Flask |
| AI Providers | OpenAI API (`gpt-4o-mini`, `gpt-4o`) · Groq API (`llama-3.1-8b-instant`) |
| Frontend | Vanilla JavaScript (no framework) |
| Styling | Custom CSS with CSS variables |
| Diagrams | Inline SVG |
| Icons | Font Awesome 6 |
| Typography | Inter (Google Fonts) |

---

## References

This tutorial draws on the following key sources. A full bibliography is available in the **References** module (Section 7) within the tutorial itself.

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
- Buolamwini & Gebru (2018). Gender Shades. *FAT Conference*.

**Journalism & Case Studies**
- Angwin et al. (2016). Machine Bias. *ProPublica*.
- Dastin, J. (2018). Amazon scraps secret AI recruiting tool that showed bias against women. Reuters (2018).

---

## License

This project is released for **educational use**. You are welcome to use, share, and adapt the material with attribution.

---

## Author

**Sridhar Nerur**
Built with [Claude](https://claude.ai) (Anthropic)

---

*For issues or suggestions, please open a GitHub issue at [github.com/snerur/ai-for-managers](https://github.com/snerur/ai-for-managers).*
