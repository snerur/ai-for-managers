"""
AI for Managers — Interactive Tutorial (Streamlit)
Created by Sridhar Nerur · Built with Claude (Anthropic)

Run:
  pip install -r requirements.txt
  streamlit run streamlit_app.py
"""

import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # no-op on Streamlit Cloud (no .env file), safe to keep

def _secret(key: str) -> str:
    """Read from st.secrets (Streamlit Cloud) with fallback to os.environ (.env / local)."""
    try:
        return st.secrets.get(key, "") or os.getenv(key, "")
    except Exception:
        return os.getenv(key, "")

_SERVER_OPENAI_KEY = _secret("OPENAI_API_KEY").strip()
_SERVER_GROQ_KEY   = _secret("GROQ_API_KEY").strip()
GROQ_BASE_URL      = "https://api.groq.com/openai/v1"
GROQ_FREE_MODEL    = "llama-3.1-8b-instant"

st.set_page_config(
    page_title="AI for Managers — Interactive Tutorial",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ────────────────────────────────────────────
def _init():
    defaults = {
        "section": 1,
        "completed": set(),
        "quiz": {},          # {section_num: {current_q, answers, complete}}
        "chat_msgs": [],
        "api_mode": "openai",
        "openai_key": "",
        "groq_key": "",
        "openai_model": "gpt-4o-mini",
        "show_chat": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--primary:#4f46e5;--secondary:#7c3aed;--accent:#06b6d4;--green:#10b981;--red:#ef4444;--amber:#f59e0b;--border:#e2e8f0;--text:#1e293b;--muted:#64748b;}
body,p,li,td,th{font-family:'Inter',sans-serif!important;color:var(--text);}
.card{background:#fff;border-radius:14px;padding:1.75rem;margin-bottom:1.5rem;box-shadow:0 2px 8px rgba(0,0,0,.06);border:1px solid #e2e8f0;}
.card h3{font-size:1.1rem;font-weight:700;color:#1e293b;margin-bottom:.85rem;}
.section-hero{background:linear-gradient(135deg,#4f46e5,#7c3aed);color:white;border-radius:16px;padding:2.5rem 2rem;margin-bottom:1.5rem;text-align:center;}
.section-hero .hero-icon{font-size:3rem;display:block;margin-bottom:.65rem;}
.section-hero h2{font-size:1.75rem;font-weight:800;margin-bottom:.65rem;color:#fff;}
.section-hero p{font-size:1rem;opacity:.9;max-width:680px;margin:0 auto;color:#fff;}
.highlight-box{background:#eef2ff;border-left:4px solid #4f46e5;border-radius:0 10px 10px 0;padding:1rem 1.25rem;margin:1rem 0;font-size:.9rem;}
.highlight-box.green{background:#f0fdf4;border-left-color:#10b981;}
.highlight-box.cyan{background:#ecfeff;border-left-color:#06b6d4;}
.highlight-box.amber{background:#fffbeb;border-left-color:#f59e0b;}
.highlight-box.red{background:#fef2f2;border-left-color:#ef4444;}
.badge{display:inline-block;background:#eef2ff;color:#4f46e5;border-radius:20px;padding:.2rem .6rem;font-size:.72rem;font-weight:600;margin-left:.5rem;}
.tag{display:inline-block;border-radius:20px;padding:.2rem .65rem;font-size:.75rem;font-weight:600;margin:.15rem;}
.tag-blue{background:#dbeafe;color:#1d4ed8;}.tag-purple{background:#ede9fe;color:#7c3aed;}
.tag-green{background:#d1fae5;color:#065f46;}.tag-cyan{background:#cffafe;color:#0e7490;}
.tag-red{background:#fee2e2;color:#dc2626;}.tag-amber{background:#fef3c7;color:#92400e;}
.example-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;margin:1rem 0;}
.example-card{background:#f8fafc;border-radius:12px;padding:1.1rem;border:1px solid #e2e8f0;}
.example-card .ex-icon{font-size:1.8rem;display:block;margin-bottom:.5rem;}
.example-card h5{font-size:.9rem;font-weight:700;color:#1e293b;margin-bottom:.35rem;}
.example-card p{font-size:.82rem;color:#475569;margin:0;line-height:1.5;}
.callout{background:#f8fafc;border-radius:12px;padding:1.1rem;border:1px solid #e2e8f0;display:flex;gap:1rem;align-items:flex-start;margin:.5rem 0;}
.callout-icon{font-size:1.5rem;flex-shrink:0;}
.callout-content h5{font-size:.9rem;font-weight:700;color:#1e293b;margin-bottom:.3rem;}
.callout-content p{font-size:.84rem;color:#475569;margin:0;line-height:1.55;}
.compare-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0;}
.compare-col.left{background:#eef2ff;border-radius:10px;padding:1.25rem;border:1px solid #c7d2fe;}
.compare-col.right{background:#ecfeff;border-radius:10px;padding:1.25rem;border:1px solid #a5f3fc;}
.styled-table{width:100%;border-collapse:collapse;font-size:.85rem;margin:1rem 0;}
.styled-table th{background:#f1f5f9;padding:.7rem .9rem;text-align:left;font-weight:600;color:#475569;border-bottom:2px solid #e2e8f0;}
.styled-table td{padding:.7rem .9rem;border-bottom:1px solid #f1f5f9;color:#374151;vertical-align:top;}
.timeline{position:relative;padding-left:2rem;}
.timeline::before{content:'';position:absolute;left:.45rem;top:.5rem;bottom:.5rem;width:2px;background:#e2e8f0;}
.timeline-item{position:relative;margin-bottom:1.1rem;}
.timeline-dot{position:absolute;left:-1.65rem;top:.4rem;width:12px;height:12px;border-radius:50%;background:#4f46e5;border:2px solid #fff;box-shadow:0 0 0 2px #c7d2fe;}
.timeline-year{font-size:.75rem;font-weight:700;color:#4f46e5;margin-bottom:.2rem;}
.timeline-content h5{font-size:.88rem;font-weight:700;color:#1e293b;margin-bottom:.25rem;}
.timeline-content p{font-size:.83rem;color:#475569;margin:0;}
.stat-row{display:flex;flex-wrap:wrap;gap:.75rem;margin:1rem 0;}
.stat-pill{background:#f1f5f9;border-radius:20px;padding:.5rem 1rem;font-size:.82rem;font-weight:600;color:#475569;border:1px solid #e2e8f0;}
.diagram-wrap{overflow-x:auto;margin:1.25rem 0;text-align:center;background:#f8fafc;border-radius:10px;padding:1rem;border:1px solid #e2e8f0;}
.section-divider{height:1px;background:#e2e8f0;margin:1.25rem 0;}
.sub-section-title{font-size:.95rem;font-weight:700;color:#1e293b;margin-bottom:.75rem;padding-bottom:.4rem;border-bottom:2px solid #e2e8f0;}
/* Streamlit tweaks */
section[data-testid="stSidebar"] .stButton>button{width:100%;text-align:left;border-radius:8px;}
</style>
""", unsafe_allow_html=True)

# ── Quiz data ────────────────────────────────────────────────
QUIZ = {
    1: {"title": "Quiz: Introduction to AI", "questions": [
        {"q": "What is the correct hierarchical relationship between AI, ML, and Deep Learning?",
         "opts": ["They are three separate, unrelated fields", "AI ⊃ ML ⊃ Deep Learning ⊃ Generative AI", "Deep Learning ⊃ ML ⊃ AI", "They are all the same thing"],
         "ans": 1, "exp": "AI is the broadest concept. Machine Learning is a subset of AI. Deep Learning is a subset of ML, and Generative AI leverages Deep Learning techniques."},
        {"q": "What makes Generative AI fundamentally different from earlier AI systems?",
         "opts": ["It is faster at calculations", "It creates new, original content such as text, images, and code", "It only works with structured data", "It requires no training data"],
         "ans": 1, "exp": "Generative AI can produce new content — not just analyze or classify existing data. Systems like ChatGPT, DALL-E, and Stable Diffusion are prime examples."},
        {"q": "The term 'Artificial Intelligence' was formally coined at which event?",
         "opts": ["The Turing Conference (1950)", "The Dartmouth Summer Research Project (1956)", "The MIT AI Lab founding (1970)", "The ImageNet competition (2012)"],
         "ans": 1, "exp": "John McCarthy coined the term 'Artificial Intelligence' at the 1956 Dartmouth Summer Research Project — widely regarded as the birth of AI as a field."},
        {"q": "Which of the following best describes a challenge (not an opportunity) of AI for businesses?",
         "opts": ["Automating repetitive tasks", "Improving customer personalization", "Data quality and governance concerns", "Faster fraud detection"],
         "ans": 2, "exp": "Data quality and governance is a key challenge — AI systems are only as good as the data they learn from. Poor or biased data leads to unreliable or harmful outcomes."},
        {"q": "A hospital uses AI to detect tumors in X-ray images. Which AI category does this fall under?",
         "opts": ["Generative AI", "Reinforcement Learning", "Deep Learning / Computer Vision", "Expert Systems"],
         "ans": 2, "exp": "Medical image analysis uses Deep Learning (specifically Convolutional Neural Networks) which can detect patterns in images that would take human radiologists much longer to spot."},
    ]},
    2: {"title": "Quiz: Supervised Learning", "questions": [
        {"q": "What does 'supervised' mean in supervised learning?",
         "opts": ["A human supervisor monitors the algorithm in real time", "The algorithm learns from labeled training data (input + known output)", "The algorithm supervises other algorithms", "No data is required — the algorithm self-supervises"],
         "ans": 1, "exp": "In supervised learning, the training data has labels — each input example comes with the correct answer. The model learns to map inputs to outputs by studying these examples."},
        {"q": "A bank wants to predict the loan amount a customer will need. This is best framed as a:",
         "opts": ["Classification problem", "Clustering problem", "Regression problem", "Reinforcement learning problem"],
         "ans": 2, "exp": "Predicting a continuous numerical value (loan amount in dollars) is a regression problem. If the bank only wanted to predict 'approve/deny,' that would be classification."},
        {"q": "Which of these is an example of a classification problem?",
         "opts": ["Forecasting next quarter's revenue", "Estimating delivery time in hours", "Detecting whether an email is spam or not spam", "Predicting a patient's blood pressure level"],
         "ans": 2, "exp": "Spam detection is a binary classification — is the email spam (yes) or not (no)? Revenue forecasting and blood pressure prediction are regression problems."},
        {"q": "Which algorithm is a powerful ensemble method widely used for both regression and classification?",
         "opts": ["K-Means Clustering", "Principal Component Analysis (PCA)", "Random Forest", "Q-Learning"],
         "ans": 2, "exp": "Random Forest builds many decision trees and combines their results. It's robust, handles missing data well, and is a go-to algorithm for supervised learning problems."},
        {"q": "A retailer uses an algorithm to predict which customers will stop buying (churn) in the next 30 days. This is:",
         "opts": ["Regression — predicting a continuous probability", "Classification — labeling customers as likely to churn or not", "Unsupervised — there are no labels needed", "Both A and B, depending on the output format"],
         "ans": 3, "exp": "If the output is a probability score (0–1), it's technically regression. If the output is a binary label (churn / no churn), it's classification. Many churn models do both!"},
    ]},
    3: {"title": "Quiz: Unsupervised Learning", "questions": [
        {"q": "What is the key distinction of unsupervised learning?",
         "opts": ["It requires more labeled data than supervised learning", "It finds patterns in data without predefined labels or correct answers", "It always produces better results than supervised learning", "It only works with image data"],
         "ans": 1, "exp": "Unsupervised learning discovers hidden structure in unlabeled data. No one tells the algorithm what to look for — it finds groups, patterns, or anomalies on its own."},
        {"q": "A marketing team wants to group customers into segments based on purchase behavior, with no predefined categories. This is:",
         "opts": ["Supervised learning (classification)", "Reinforcement learning", "Unsupervised learning (clustering)", "Deep learning only"],
         "ans": 2, "exp": "Customer segmentation without predefined groups is classic unsupervised clustering. Algorithms like K-Means discover natural groupings in the data."},
        {"q": "Which technique is used to detect unusual transactions that may indicate fraud?",
         "opts": ["Regression", "Clustering", "Anomaly Detection", "Sentiment Analysis"],
         "ans": 2, "exp": "Anomaly detection identifies data points that deviate significantly from normal patterns — making it ideal for fraud detection, cybersecurity, and equipment failure prediction."},
        {"q": "What does the K-Means algorithm's 'K' represent?",
         "opts": ["The number of training iterations", "The number of clusters to form", "The minimum data points required", "The learning rate"],
         "ans": 1, "exp": "In K-Means, K is the number of clusters you want the algorithm to find. Choosing the right K is an art — too few misses nuance, too many creates noise."},
        {"q": "Amazon's 'Customers who bought this also bought…' feature, which drives ~35% of its revenue, is built on which unsupervised learning technique?",
         "opts": ["Linear Regression", "K-Means Clustering", "Association Rule Mining", "Principal Component Analysis"],
         "ans": 2, "exp": "Amazon's recommendation engine uses item-to-item collaborative filtering — a form of association rule mining — to find products frequently bought together. The methodology was published by Amazon researchers in IEEE Internet Computing (Linden, Smith & York, 2003)."},
    ]},
    4: {"title": "Quiz: Reinforcement Learning", "questions": [
        {"q": "In reinforcement learning, what is the 'agent'?",
         "opts": ["The dataset used for training", "The algorithm or system that makes decisions and takes actions", "The reward signal that guides learning", "The human trainer monitoring the system"],
         "ans": 1, "exp": "The agent is the learner or decision-maker. It observes the environment, chooses actions, and receives rewards or penalties based on those actions."},
        {"q": "What does the agent aim to maximize in reinforcement learning?",
         "opts": ["The speed of individual decisions", "Cumulative long-term reward", "The size of the training dataset", "The number of possible actions"],
         "ans": 1, "exp": "RL agents optimize for cumulative reward over time — not just immediate gains. This is why RL can learn strategies that sacrifice short-term rewards for greater long-term payoffs."},
        {"q": "DeepMind's AlphaGo defeated world champion Go players. Which AI approach enabled this?",
         "opts": ["Supervised learning with expert game data", "Unsupervised clustering of game states", "Reinforcement learning through millions of self-play games", "Rule-based expert systems"],
         "ans": 2, "exp": "AlphaGo used reinforcement learning — playing millions of games against itself to discover strategies beyond human knowledge. It also used supervised learning from human games initially."},
        {"q": "A company uses AI to dynamically adjust its pricing based on demand, competition, and inventory. This is closest to:",
         "opts": ["Supervised classification", "Unsupervised clustering", "Reinforcement learning", "Generative AI"],
         "ans": 2, "exp": "Dynamic pricing is a sequential decision-making problem where actions (price changes) affect future state (demand, inventory). RL is well-suited for such problems."},
        {"q": "Why is reinforcement learning generally harder to deploy in business than supervised learning?",
         "opts": ["It requires much less data", "It only works in virtual environments", "Actions have delayed consequences, real-world trials can be costly, and rewards are hard to define", "It is slower to compute predictions"],
         "ans": 2, "exp": "RL challenges include: defining a good reward function, the cost of real-world exploration (wrong actions can be expensive or dangerous), and delayed feedback making it hard to attribute which action caused a reward."},
    ]},
    5: {"title": "Quiz: AI Ethics & Governance", "questions": [
        {"q": "The COMPAS recidivism algorithm scandal highlighted which key AI ethics concern?",
         "opts": ["The system was too slow to be useful", "The algorithm had racial bias, predicting higher recidivism for Black defendants than warranted", "The algorithm was too expensive for courts to use", "The algorithm violated copyright law"],
         "ans": 1, "exp": "ProPublica's 2016 investigation found COMPAS was twice as likely to falsely flag Black defendants as high risk compared to white defendants — a stark example of AI bias with life-changing consequences."},
        {"q": "Which ethical principle requires that AI decisions can be understood, audited, and explained?",
         "opts": ["Sustainability", "Fairness", "Transparency and Explainability", "Security"],
         "ans": 2, "exp": "Transparency means AI systems should be understandable — stakeholders should be able to know why a decision was made. This is especially critical in high-stakes domains like credit, hiring, and medicine."},
        {"q": "The EU AI Act classifies AI systems primarily based on:",
         "opts": ["The nationality of the developer", "The programming language used", "Risk levels — from unacceptable risk to minimal risk", "The size of the company deploying the AI"],
         "ans": 2, "exp": "The EU AI Act uses a risk-based approach: Unacceptable (banned), High-risk (strict requirements), Limited risk (transparency obligations), and Minimal risk (largely unregulated)."},
        {"q": "A large language model confidently states an incorrect historical fact as if it were true. This is known as:",
         "opts": ["Model drift", "Hallucination", "Adversarial attack", "Overfitting"],
         "ans": 1, "exp": "AI 'hallucination' refers to when LLMs generate plausible-sounding but factually incorrect content with apparent confidence. This is a critical concern for business use cases requiring accuracy."},
        {"q": "The NIST AI Risk Management Framework (AI RMF) organizes AI risk management into which four core functions?",
         "opts": ["Plan, Build, Test, Deploy", "Govern, Map, Measure, Manage", "Identify, Protect, Detect, Respond", "Collect, Process, Analyze, Act"],
         "ans": 1, "exp": "The NIST AI RMF uses GOVERN (culture & accountability), MAP (context & risk identification), MEASURE (risk analysis & assessment), and MANAGE (risk treatment and monitoring)."},
    ]},
    6: {"title": "Quiz: Organizational Readiness", "questions": [
        {"q": "What does an AI maturity model primarily help an organization assess?",
         "opts": ["Which AI vendor to purchase from", "Their current AI capabilities and a roadmap for advancement", "The technical specifications of AI hardware", "Legal compliance requirements"],
         "ans": 1, "exp": "AI maturity models provide a structured framework to assess where an organization currently stands on its AI journey and what capabilities it needs to develop to reach the next level."},
        {"q": "Which is the most foundational step when starting an AI transformation journey?",
         "opts": ["Hiring a Chief AI Officer immediately", "Purchasing the latest AI software tools", "Building a strong data foundation — quality, governance, and accessibility", "Training all employees on advanced ML algorithms"],
         "ans": 2, "exp": "AI systems are only as good as the data they're built on. Before anything else, organizations need high-quality, well-governed, accessible data. 'Garbage in, garbage out' is real."},
        {"q": "Which cultural characteristic is most critical for an AI-first organization?",
         "opts": ["Replacing all human judgment with AI decisions", "Fostering a data-driven, experiment-friendly, learning culture", "Keeping AI initiatives confidential to maintain competitive advantage", "Centralizing all AI work in the IT department"],
         "ans": 1, "exp": "Culture eats strategy for breakfast — and AI transformation. Organizations must foster curiosity, comfort with data, willingness to experiment, and cross-functional collaboration."},
        {"q": "What is the purpose of an 'AI Center of Excellence' in an organization?",
         "opts": ["To replace the IT department", "To centralize AI expertise, set standards, and support AI adoption across the organization", "To build and sell AI products to external customers", "To monitor employee performance using AI"],
         "ans": 1, "exp": "An AI Center of Excellence (CoE) acts as a hub for AI expertise, best practices, tools, and governance — enabling the whole organization to benefit from AI capabilities while maintaining standards."},
        {"q": "An organization that treats AI as a core strategic capability embedded in all products and decisions best represents which stage?",
         "opts": ["Level 1: AI Aware", "Level 2: AI Active", "Level 4: AI Systemic / Transformational", "Level 3: AI Operational"],
         "ans": 2, "exp": "At the Systemic/Transformational stage, AI is not just a tool for specific tasks — it's woven into the organization's DNA, driving competitive advantage, decision-making, and product development at scale."},
    ]},
}

SECTION_NAMES = {
    1: "Introduction to AI", 2: "Supervised Learning", 3: "Unsupervised Learning",
    4: "Reinforcement Learning", 5: "AI Ethics & Governance", 6: "Organizational Readiness",
    7: "References",
}

# ── Content functions ────────────────────────────────────────

def section1():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">🚀</span>
  <h2>Introduction to Artificial Intelligence</h2>
  <p>Understand the AI landscape — from foundational definitions to the historical breakthroughs that shaped today's technology — and discover how AI is transforming every industry.</p>
</div>

<div class="card">
  <h3>📖 Defining the AI Landscape <span class="badge">1a</span></h3>
  <p>These four terms are often used interchangeably in business conversations — but they have distinct meanings. Think of them as nested circles, each one living inside the previous.</p>
  <div class="diagram-wrap">
    <svg viewBox="0 0 520 320" width="480" height="300" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="260" cy="160" rx="240" ry="145" fill="#eef2ff" stroke="#4f46e5" stroke-width="2.5"/>
      <text x="60" y="56" font-size="14" font-weight="700" fill="#4f46e5" font-family="Inter,sans-serif">Artificial Intelligence</text>
      <text x="60" y="72" font-size="11" fill="#6366f1" font-family="Inter,sans-serif">Simulating human intelligence</text>
      <ellipse cx="280" cy="170" rx="175" ry="105" fill="#ede9fe" stroke="#7c3aed" stroke-width="2.5"/>
      <text x="130" y="102" font-size="13" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">Machine Learning</text>
      <text x="130" y="117" font-size="10" fill="#8b5cf6" font-family="Inter,sans-serif">Learning from data</text>
      <ellipse cx="295" cy="178" rx="110" ry="68" fill="#dbeafe" stroke="#2563eb" stroke-width="2.5"/>
      <text x="215" y="158" font-size="12" font-weight="700" fill="#1d4ed8" font-family="Inter,sans-serif">Deep Learning</text>
      <text x="215" y="172" font-size="10" fill="#3b82f6" font-family="Inter,sans-serif">Neural networks</text>
      <ellipse cx="305" cy="184" rx="58" ry="36" fill="#cffafe" stroke="#0891b2" stroke-width="2.5"/>
      <text x="270" y="181" font-size="10" font-weight="700" fill="#0e7490" font-family="Inter,sans-serif">Gen AI</text>
      <text x="267" y="194" font-size="9" fill="#0891b2" font-family="Inter,sans-serif">Creates content</text>
    </svg>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.25rem">
    <div style="background:#eef2ff;border-radius:10px;padding:1.1rem;border-left:4px solid #4f46e5">
      <h5 style="font-weight:700;color:#4f46e5;margin-bottom:.4rem">🤖 Artificial Intelligence (AI)</h5>
      <p style="font-size:.85rem;color:#374151;margin:0">The broad science of creating computer systems that can perform tasks requiring human-like intelligence — reasoning, learning, problem-solving, language understanding, and perception.</p>
    </div>
    <div style="background:#ede9fe;border-radius:10px;padding:1.1rem;border-left:4px solid #7c3aed">
      <h5 style="font-weight:700;color:#7c3aed;margin-bottom:.4rem">📊 Machine Learning (ML)</h5>
      <p style="font-size:.85rem;color:#374151;margin:0">A subset of AI where systems automatically learn and improve from <em>experience (data)</em> without being explicitly programmed. The more data they see, the better they get.</p>
    </div>
    <div style="background:#dbeafe;border-radius:10px;padding:1.1rem;border-left:4px solid #2563eb">
      <h5 style="font-weight:700;color:#1d4ed8;margin-bottom:.4rem">🧠 Deep Learning (DL)</h5>
      <p style="font-size:.85rem;color:#374151;margin:0">A subset of ML using artificial <em>neural networks</em> with many layers — inspired by the human brain. Excels at images, speech, and text. Powers facial recognition and voice assistants.</p>
    </div>
    <div style="background:#cffafe;border-radius:10px;padding:1.1rem;border-left:4px solid #0891b2">
      <h5 style="font-weight:700;color:#0e7490;margin-bottom:.4rem">✨ Generative AI (GenAI)</h5>
      <p style="font-size:.85rem;color:#374151;margin:0">AI that creates <em>new content</em> — text (ChatGPT), images (DALL-E), code (GitHub Copilot), and audio. Uses deep learning models trained on vast datasets.</p>
    </div>
  </div>
  <div class="highlight-box cyan" style="margin-top:1.25rem">
    <strong>Manager's Takeaway:</strong> When someone says "we should use AI," ask: do they mean ML (pattern recognition in data), deep learning (images/voice), or generative AI (content creation)? Each requires different data, skills, and investment.
  </div>
</div>

<div class="card">
  <h3>🕐 A Brief History of AI <span class="badge">1b</span></h3>
  <p>AI has evolved through cycles of excitement and disappointment — known as "AI winters" — before reaching today's transformational era.</p>
  <div class="timeline">
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">1950</div>
      <div class="timeline-content"><h5>Turing Test Proposed</h5><p>Alan Turing asks "Can machines think?" and proposes a test of machine intelligence — still debated today.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">1956</div>
      <div class="timeline-content"><h5>AI is Born — Dartmouth Conference</h5><p>John McCarthy coins "Artificial Intelligence." The field officially begins with great optimism.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">1970s–80s</div>
      <div class="timeline-content"><h5>Expert Systems Era</h5><p>Rule-based AI systems achieve narrow successes but scaling is hard — the first "AI winter" follows.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">1997</div>
      <div class="timeline-content"><h5>Deep Blue Defeats Kasparov</h5><p>IBM's Deep Blue defeats world chess champion Garry Kasparov — a landmark moment for AI.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">2012</div>
      <div class="timeline-content"><h5>Deep Learning Breakthrough — ImageNet</h5><p>AlexNet wins the ImageNet competition with deep neural networks. The modern AI era begins.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot"></div><div>
      <div class="timeline-year">2017</div>
      <div class="timeline-content"><h5>"Attention Is All You Need" — Transformers</h5><p>Google researchers publish the Transformer architecture — the foundation for GPT, BERT, and all modern LLMs.</p></div>
    </div></div>
    <div class="timeline-item"><div class="timeline-dot" style="background:#06b6d4"></div><div>
      <div class="timeline-year">2022–Now</div>
      <div class="timeline-content"><h5>The Generative AI Revolution</h5><p>ChatGPT reaches 100 million users in 60 days. GPT-4, Claude, Gemini, and Llama reshape every industry.</p></div>
    </div></div>
  </div>
</div>

<div class="card">
  <h3>💡 Opportunities &amp; Challenges <span class="badge">1c</span></h3>
  <div class="sub-section-title">Opportunities by Industry</div>
  <div class="example-grid">
    <div class="example-card"><span class="ex-icon">🏥</span><h5>Healthcare</h5><p>AI diagnoses cancers from scans with radiologist-level accuracy. AlphaFold solved the 50-year protein folding problem.</p></div>
    <div class="example-card"><span class="ex-icon">🏦</span><h5>Finance</h5><p>Real-time fraud detection saves billions annually. Algorithmic trading, credit scoring, and robo-advisors are mainstream.</p></div>
    <div class="example-card"><span class="ex-icon">🛍️</span><h5>Retail &amp; E-commerce</h5><p>Amazon's recommendation engine drives 35% of revenue. AI powers dynamic pricing and personalized marketing.</p></div>
    <div class="example-card"><span class="ex-icon">🏭</span><h5>Manufacturing</h5><p>Predictive maintenance reduces unplanned downtime by 30–50%. Computer vision detects defects faster than human inspectors.</p></div>
    <div class="example-card"><span class="ex-icon">🚗</span><h5>Transportation</h5><p>AI optimizes logistics routes (UPS saved 100M miles/year), powers autonomous vehicles, and manages traffic.</p></div>
    <div class="example-card"><span class="ex-icon">📚</span><h5>Education</h5><p>Personalized learning platforms adapt content to each student's pace. AI tutors provide 24/7 support.</p></div>
  </div>
  <div class="section-divider"></div>
  <div class="sub-section-title">Key Challenges</div>
  <div class="compare-grid">
    <div style="background:#fef2f2;border-radius:10px;padding:1.25rem">
      <h4 style="color:#ef4444;margin-bottom:.75rem">⚠️ Technical Challenges</h4>
      <ul style="color:#374151;font-size:.88rem;padding-left:1.1rem">
        <li><strong>Data quality:</strong> AI is only as good as its training data.</li>
        <li><strong>Explainability:</strong> Many AI systems are "black boxes."</li>
        <li><strong>Scalability:</strong> Moving from pilot to enterprise-wide deployment is non-trivial.</li>
        <li><strong>Talent gap:</strong> Demand for AI/ML skills far exceeds supply globally.</li>
      </ul>
    </div>
    <div style="background:#fffbeb;border-radius:10px;padding:1.25rem">
      <h4 style="color:#f59e0b;margin-bottom:.75rem">⚖️ Organizational &amp; Ethical Challenges</h4>
      <ul style="color:#374151;font-size:.88rem;padding-left:1.1rem">
        <li><strong>Bias &amp; fairness:</strong> Models can perpetuate past inequities.</li>
        <li><strong>Regulatory uncertainty:</strong> EU AI Act, US executive orders evolving rapidly.</li>
        <li><strong>Change management:</strong> Workforce reskilling and cultural resistance.</li>
        <li><strong>Security &amp; privacy:</strong> AI systems can be adversarial targets.</li>
      </ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def section2():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">🏷️</span>
  <h2>Supervised Learning</h2>
  <p>The most widely used form of machine learning in business. From predicting sales to detecting fraud, supervised learning powers decisions across every function.</p>
</div>

<div class="card">
  <h3>🎓 What is Supervised Learning? <span class="badge">2a</span></h3>
  <p>Supervised learning trains a model on <strong>labeled data</strong> — examples where both the input and the correct output are known. The algorithm learns to map inputs to outputs, then generalizes to new, unseen data.</p>
  <div class="diagram-wrap">
    <svg viewBox="0 0 680 130" width="640" height="120" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#94a3b8"/></marker></defs>
      <rect x="10" y="30" width="140" height="70" rx="12" fill="#eef2ff" stroke="#4f46e5" stroke-width="2"/>
      <text x="80" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#4f46e5" font-family="Inter,sans-serif">Labeled Training</text>
      <text x="80" y="76" text-anchor="middle" font-size="12" font-weight="700" fill="#4f46e5" font-family="Inter,sans-serif">Data</text>
      <text x="80" y="90" text-anchor="middle" font-size="10" fill="#6366f1" font-family="Inter,sans-serif">(input + known output)</text>
      <path d="M150 65 L190 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="190" y="30" width="140" height="70" rx="12" fill="#ede9fe" stroke="#7c3aed" stroke-width="2"/>
      <text x="260" y="63" text-anchor="middle" font-size="12" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">ML Algorithm</text>
      <text x="260" y="80" text-anchor="middle" font-size="10" fill="#8b5cf6" font-family="Inter,sans-serif">Learns patterns</text>
      <path d="M330 65 L370 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="370" y="30" width="130" height="70" rx="12" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>
      <text x="435" y="63" text-anchor="middle" font-size="12" font-weight="700" fill="#1d4ed8" font-family="Inter,sans-serif">Trained Model</text>
      <text x="435" y="79" text-anchor="middle" font-size="10" fill="#3b82f6" font-family="Inter,sans-serif">(learned function)</text>
      <path d="M500 65 L540 65" stroke="#94a3b8" stroke-width="2" marker-end="url(#arr)"/>
      <rect x="540" y="30" width="130" height="70" rx="12" fill="#d1fae5" stroke="#059669" stroke-width="2"/>
      <text x="605" y="60" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46" font-family="Inter,sans-serif">Predictions on</text>
      <text x="605" y="76" text-anchor="middle" font-size="12" font-weight="700" fill="#065f46" font-family="Inter,sans-serif">New Data</text>
    </svg>
  </div>
  <div class="highlight-box">
    <strong>Analogy:</strong> Think of supervised learning like training a new employee using past examples. You show them thousands of customer cases with the correct outcome. Over time, they learn the patterns and can handle new cases independently.
  </div>
</div>

<div class="card">
  <h3>🔀 Regression vs. Classification <span class="badge">2b</span></h3>
  <p>Supervised learning has two major flavors, distinguished by the type of output they predict:</p>
  <div class="compare-grid">
    <div class="compare-col left">
      <h4 style="color:#4f46e5">📈 Regression</h4>
      <p style="font-size:.88rem;color:#475569">Predicts a <strong>continuous numerical value</strong>.</p>
      <p style="font-size:.85rem;color:#475569"><strong>Think:</strong> "How much?" or "How many?"</p>
      <p style="font-size:.85rem;font-weight:700;margin-top:.75rem">Examples:</p>
      <ul style="font-size:.85rem;color:#475569;padding-left:1.1rem">
        <li>What will quarterly revenue be?</li>
        <li>What price should we charge?</li>
        <li>How long will delivery take?</li>
        <li>What will energy consumption be tomorrow?</li>
      </ul>
      <div style="margin-top:.75rem"><span class="tag tag-blue">Linear Regression</span><span class="tag tag-blue">Decision Tree</span><span class="tag tag-blue">Random Forest</span><span class="tag tag-blue">XGBoost</span></div>
    </div>
    <div class="compare-col right">
      <h4 style="color:#0e7490">🏷️ Classification</h4>
      <p style="font-size:.88rem;color:#475569">Predicts a <strong>category or label</strong>.</p>
      <p style="font-size:.85rem;color:#475569"><strong>Think:</strong> "Which group?" or "Is it X or Y?"</p>
      <p style="font-size:.85rem;font-weight:700;margin-top:.75rem">Examples:</p>
      <ul style="font-size:.85rem;color:#475569;padding-left:1.1rem">
        <li>Is this email spam or not spam?</li>
        <li>Will this customer churn? (Yes/No)</li>
        <li>Is this transaction fraudulent?</li>
        <li>Is this tumor benign or malignant?</li>
      </ul>
      <div style="margin-top:.75rem"><span class="tag tag-cyan">Logistic Regression</span><span class="tag tag-cyan">Decision Tree</span><span class="tag tag-cyan">Random Forest</span><span class="tag tag-cyan">SVM</span></div>
    </div>
  </div>
</div>

<div class="card">
  <h3>💼 Real-World Business Applications <span class="badge">2c</span></h3>
  <div class="sub-section-title">Regression in Action</div>
  <div class="example-grid">
    <div class="example-card"><span class="ex-icon">💰</span><h5>Sales Forecasting</h5><p>Predict future revenue based on marketing spend, seasonality, and economic indicators. Helps CFOs plan budgets accurately.</p></div>
    <div class="example-card"><span class="ex-icon">🏠</span><h5>Real Estate Pricing</h5><p>Zillow's "Zestimate" uses regression to value 100M+ homes from 200+ variables — location, size, amenities, recent sales.</p></div>
    <div class="example-card"><span class="ex-icon">⚡</span><h5>Energy Demand</h5><p>Utilities predict hourly electricity demand to balance the grid, reducing waste and preventing blackouts.</p></div>
  </div>
  <div class="sub-section-title" style="margin-top:1.25rem">Classification in Action</div>
  <div class="example-grid">
    <div class="example-card"><span class="ex-icon">🔒</span><h5>Fraud Detection</h5><p>Banks classify each transaction as legitimate or fraudulent in milliseconds. Visa and Mastercard prevent billions in annual losses.</p></div>
    <div class="example-card"><span class="ex-icon">📧</span><h5>Email Spam Filter</h5><p>Gmail's spam filter classifies 15 billion emails daily with 99.9% accuracy — saving professionals hours per week.</p></div>
    <div class="example-card"><span class="ex-icon">🏃</span><h5>Customer Churn</h5><p>Telecoms predict which customers will cancel service next month, enabling proactive retention offers before they leave.</p></div>
  </div>
</div>
""", unsafe_allow_html=True)


def section3():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">🔍</span>
  <h2>Unsupervised Learning</h2>
  <p>Discover hidden patterns and structure in data — no labels required. Unsupervised learning is how machines find customer segments, detect anomalies, and surface insights no human thought to look for.</p>
</div>

<div class="card">
  <h3>🔎 What is Unsupervised Learning? <span class="badge">3a</span></h3>
  <p>Unlike supervised learning, unsupervised learning works with <strong>unlabeled data</strong> — there's no correct answer to learn from. Instead, the algorithm discovers hidden structures, groupings, or patterns on its own.</p>
  <div class="compare-grid">
    <div style="background:#eef2ff;border-radius:10px;padding:1.1rem;border:1px solid #c7d2fe">
      <h5 style="font-weight:700;color:#4f46e5;margin-bottom:.5rem">Supervised Learning</h5>
      <p style="font-size:.85rem;color:#475569">Data is labeled: "This customer churned." "This transaction was fraud." The model learns from known examples.</p>
    </div>
    <div style="background:#d1fae5;border-radius:10px;padding:1.1rem;border:1px solid #6ee7b7">
      <h5 style="font-weight:700;color:#065f46;margin-bottom:.5rem">Unsupervised Learning</h5>
      <p style="font-size:.85rem;color:#475569">No labels. The model says "I notice these 5 customer types naturally cluster together" — without being told what to find.</p>
    </div>
  </div>
  <div class="highlight-box green" style="margin-top:1.25rem">
    <strong>Analogy:</strong> Imagine dropping a new employee into a large customer database with no instructions. They start noticing patterns: "These customers all buy premium products late at night..." That's unsupervised learning — self-directed pattern discovery.
  </div>
</div>

<div class="card">
  <h3>📊 Techniques, Algorithms &amp; Real-World Examples <span class="badge">3b</span></h3>
  <div class="diagram-wrap">
    <svg viewBox="0 0 520 220" width="480" height="210" xmlns="http://www.w3.org/2000/svg">
      <text x="260" y="22" text-anchor="middle" font-size="14" font-weight="700" fill="#1e293b" font-family="Inter,sans-serif">K-Means Clustering: Customer Segmentation</text>
      <circle cx="100" cy="80" r="40" fill="#ede9fe" stroke="#7c3aed" stroke-width="1.5" stroke-dasharray="5,3"/>
      <circle cx="90" cy="72" r="6" fill="#7c3aed"/><circle cx="108" cy="68" r="6" fill="#7c3aed"/>
      <circle cx="95" cy="88" r="6" fill="#7c3aed"/><circle cx="112" cy="82" r="6" fill="#7c3aed"/>
      <text x="100" y="135" text-anchor="middle" font-size="11" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">Premium Buyers</text>
      <circle cx="260" cy="130" r="45" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="5,3"/>
      <circle cx="248" cy="120" r="6" fill="#2563eb"/><circle cx="270" cy="115" r="6" fill="#2563eb"/>
      <circle cx="255" cy="138" r="6" fill="#2563eb"/><circle cx="272" cy="135" r="6" fill="#2563eb"/>
      <text x="260" y="187" text-anchor="middle" font-size="11" font-weight="700" fill="#2563eb" font-family="Inter,sans-serif">Regular Shoppers</text>
      <circle cx="420" cy="80" r="38" fill="#d1fae5" stroke="#059669" stroke-width="1.5" stroke-dasharray="5,3"/>
      <circle cx="410" cy="70" r="6" fill="#059669"/><circle cx="428" cy="68" r="6" fill="#059669"/>
      <circle cx="415" cy="85" r="6" fill="#059669"/><circle cx="432" cy="82" r="6" fill="#059669"/>
      <text x="420" y="130" text-anchor="middle" font-size="11" font-weight="700" fill="#059669" font-family="Inter,sans-serif">Bargain Hunters</text>
    </svg>
  </div>
  <table class="styled-table">
    <thead><tr><th>Technique</th><th>What It Does</th><th>Key Algorithms</th><th>Business Use Case</th></tr></thead>
    <tbody>
      <tr><td><span class="tag tag-purple">Clustering</span></td><td>Groups similar data points together</td><td>K-Means, DBSCAN, Hierarchical</td><td>Customer segmentation, document grouping</td></tr>
      <tr><td><span class="tag tag-blue">Dimensionality Reduction</span></td><td>Reduces variables while retaining information</td><td>PCA, t-SNE, UMAP, Autoencoders</td><td>Visualizing complex data, compressing features</td></tr>
      <tr><td><span class="tag tag-red">Anomaly Detection</span></td><td>Identifies unusual patterns that deviate from the norm</td><td>Isolation Forest, One-Class SVM</td><td>Fraud detection, equipment failure, cybersecurity</td></tr>
      <tr><td><span class="tag tag-green">Association Rules</span></td><td>Finds items that frequently co-occur</td><td>Apriori, FP-Growth</td><td>Market basket analysis, cross-selling</td></tr>
      <tr><td><span class="tag tag-amber">Topic Modeling</span></td><td>Discovers themes in collections of documents</td><td>LDA, NMF</td><td>Analyzing customer reviews, support tickets</td></tr>
    </tbody>
  </table>
  <div class="section-divider"></div>
  <div class="sub-section-title">Spotlight: Amazon's Recommendation Engine</div>
  <div class="callout">
    <span class="callout-icon">🛒</span>
    <div class="callout-content">
      <h5>"Customers Who Bought This Also Bought…"</h5>
      <p>Amazon's item-to-item collaborative filtering — a large-scale application of association rule mining — analyzes purchase and browsing patterns across hundreds of millions of transactions to surface products frequently bought together. Amazon's researchers published the methodology in <em>IEEE Internet Computing</em> (Linden, Smith &amp; York, 2003), and Amazon executives have publicly credited the recommendations feature with driving approximately 35% of total revenue. This is one of the most cited, peer-reviewed examples of association rule mining creating measurable business value at scale.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def section4():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">🎮</span>
  <h2>Reinforcement Learning</h2>
  <p>The AI paradigm closest to how humans and animals naturally learn — through trial, error, and reward. From game-playing champions to autonomous robots, RL pushes the frontiers of what AI can achieve.</p>
</div>

<div class="card">
  <h3>🤖 What is Reinforcement Learning? <span class="badge">4a</span></h3>
  <p>Reinforcement Learning (RL) is a type of machine learning where an <strong>agent</strong> learns to make decisions by interacting with an <strong>environment</strong>. The agent receives <strong>rewards</strong> for good actions and penalties for bad ones, learning a strategy (called a <em>policy</em>) that maximizes long-term cumulative reward.</p>
  <div class="highlight-box">
    <strong>Analogy:</strong> Think of training a dog. You don't show it labeled examples of "correct" behavior. Instead, you reward it with treats when it does something right. The dog learns which behaviors lead to rewards — that's reinforcement learning.
  </div>
</div>

<div class="card">
  <h3>🔑 Key Concepts in Reinforcement Learning <span class="badge">4b</span></h3>
  <div class="diagram-wrap">
    <svg viewBox="0 0 560 240" width="520" height="230" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="arr2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#7c3aed"/></marker>
        <marker id="arr3" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#ef4444"/></marker>
      </defs>
      <rect x="30" y="80" width="160" height="80" rx="14" fill="#eef2ff" stroke="#4f46e5" stroke-width="2.5"/>
      <text x="110" y="113" text-anchor="middle" font-size="20" font-family="sans-serif">🤖</text>
      <text x="110" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="#4f46e5" font-family="Inter,sans-serif">AGENT</text>
      <text x="110" y="150" text-anchor="middle" font-size="10" fill="#6366f1" font-family="Inter,sans-serif">Decision maker</text>
      <rect x="370" y="80" width="160" height="80" rx="14" fill="#d1fae5" stroke="#059669" stroke-width="2.5"/>
      <text x="450" y="113" text-anchor="middle" font-size="20" font-family="sans-serif">🌍</text>
      <text x="450" y="135" text-anchor="middle" font-size="13" font-weight="700" fill="#065f46" font-family="Inter,sans-serif">ENVIRONMENT</text>
      <text x="450" y="150" text-anchor="middle" font-size="10" fill="#059669" font-family="Inter,sans-serif">World / Context</text>
      <path d="M190 100 Q280 40 370 100" fill="none" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#arr2)"/>
      <text x="280" y="55" text-anchor="middle" font-size="11" font-weight="700" fill="#7c3aed" font-family="Inter,sans-serif">ACTION</text>
      <path d="M370 140 Q280 200 190 140" fill="none" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arr3)"/>
      <text x="280" y="195" text-anchor="middle" font-size="11" font-weight="700" fill="#ef4444" font-family="Inter,sans-serif">STATE + REWARD</text>
    </svg>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem">
    <div style="background:#eef2ff;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">🎯</div><h5 style="font-weight:700;color:#4f46e5;margin-bottom:.3rem">State</h5><p style="font-size:.82rem;color:#475569;margin:0">The current situation the agent perceives. Example: the current board position in chess.</p></div>
    <div style="background:#ede9fe;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">⚡</div><h5 style="font-weight:700;color:#7c3aed;margin-bottom:.3rem">Action</h5><p style="font-size:.82rem;color:#475569;margin:0">What the agent does in a given state. Example: moving a chess piece, adjusting a price.</p></div>
    <div style="background:#fef3c7;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">🏆</div><h5 style="font-weight:700;color:#92400e;margin-bottom:.3rem">Reward</h5><p style="font-size:.82rem;color:#475569;margin:0">Feedback signal after an action. The agent learns to maximize total reward over time.</p></div>
    <div style="background:#d1fae5;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">🗺️</div><h5 style="font-weight:700;color:#065f46;margin-bottom:.3rem">Policy</h5><p style="font-size:.82rem;color:#475569;margin:0">The agent's strategy — a mapping from states to actions. This is what the agent is learning.</p></div>
    <div style="background:#cffafe;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">🔭</div><h5 style="font-weight:700;color:#0e7490;margin-bottom:.3rem">Exploration</h5><p style="font-size:.82rem;color:#475569;margin:0">Trying new actions to discover potentially better strategies.</p></div>
    <div style="background:#fce7f3;border-radius:10px;padding:1rem;text-align:center"><div style="font-size:1.5rem;margin-bottom:.4rem">💡</div><h5 style="font-weight:700;color:#9d174d;margin-bottom:.3rem">Exploitation</h5><p style="font-size:.82rem;color:#475569;margin:0">Using known good actions to maximize reward. The fundamental tradeoff with exploration.</p></div>
  </div>
</div>

<div class="card">
  <h3>🏆 Real-World Applications of RL <span class="badge">4c</span></h3>
  <div class="example-grid">
    <div class="example-card"><span class="ex-icon">♟️</span><h5>AlphaGo &amp; AlphaZero</h5><p>DeepMind's AlphaZero mastered chess, Go, and shogi to superhuman level by playing millions of games against itself.</p></div>
    <div class="example-card"><span class="ex-icon">🤖</span><h5>Robotics</h5><p>Boston Dynamics and Google's robotics teams use RL to teach robots to walk, balance, and manipulate objects.</p></div>
    <div class="example-card"><span class="ex-icon">📱</span><h5>Content Recommendation</h5><p>YouTube, Netflix, and TikTok use RL to optimize what to show you next — maximizing watch time and engagement.</p></div>
    <div class="example-card"><span class="ex-icon">🏭</span><h5>Data Center Cooling</h5><p>Google DeepMind used RL to optimize data center cooling — reducing cooling energy by 40%.</p></div>
    <div class="example-card"><span class="ex-icon">💹</span><h5>Algorithmic Trading</h5><p>RL agents learn trading strategies by being rewarded for profitable trades and penalized for losses.</p></div>
    <div class="example-card"><span class="ex-icon">🚗</span><h5>Autonomous Vehicles</h5><p>Self-driving systems use RL combined with other techniques to learn safe driving policies through simulation.</p></div>
  </div>
  <div class="highlight-box amber" style="margin-top:1.25rem">
    <strong>Manager's Reality Check:</strong> RL is powerful but complex. Most business AI uses supervised or unsupervised learning; RL is for sequential decision-making problems. A poorly defined reward can lead to "reward hacking."
  </div>
</div>
""", unsafe_allow_html=True)


def section5():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">⚖️</span>
  <h2>AI Ethics &amp; Governance</h2>
  <p>With great power comes great responsibility. Understanding AI ethics isn't optional for managers — it's how you protect your customers, employees, and organization from real harm.</p>
</div>

<div class="card">
  <h3>⚠️ Why AI Ethics Matters <span class="badge">5a</span></h3>
  <p>AI systems make decisions that affect people's lives — hiring, lending, healthcare, criminal justice. When these systems are biased, opaque, or misused, the consequences are severe.</p>
  <div class="stat-row">
    <div class="stat-pill">⚠️ 78% of AI projects fail to deliver expected value</div>
    <div class="stat-pill">📉 Companies lose avg. 20% of market cap after major AI failures</div>
    <div class="stat-pill">⚖️ EU AI Act fines up to €35M or 7% of global revenue</div>
  </div>
  <div class="highlight-box red">
    <strong>Bottom Line:</strong> AI ethics is not a PR exercise or a compliance checkbox. Unethical AI causes real harm to real people — and exposes your organization to legal, financial, and reputational risk. It must be embedded into every AI project from day one.
  </div>
</div>

<div class="card">
  <h3>📚 Ethical Frameworks for AI <span class="badge">5b</span></h3>
  <p>Different philosophical traditions offer distinct lenses for evaluating AI decisions.</p>
  <table class="styled-table">
    <thead><tr><th>Theory</th><th>Core Principle</th><th>Applied to AI</th><th>Limitation</th></tr></thead>
    <tbody>
      <tr><td><strong>Utilitarianism</strong> <span class="tag tag-blue">Consequentialist</span></td><td>Greatest good for the greatest number</td><td>Optimize AI for overall societal benefit</td><td>Can justify harming minorities for majority benefit</td></tr>
      <tr><td><strong>Deontology</strong> <span class="tag tag-purple">Rules-Based</span></td><td>Actions are inherently right or wrong (Kant)</td><td>Some AI uses are intrinsically wrong regardless of benefit</td><td>Can be inflexible; rules may conflict</td></tr>
      <tr><td><strong>Virtue Ethics</strong> <span class="tag tag-green">Character-Based</span></td><td>What would a person of good character do? (Aristotle)</td><td>Build AI teams with strong ethical character</td><td>Harder to operationalize at scale</td></tr>
      <tr><td><strong>Contractualism</strong> <span class="tag tag-amber">Social Contract</span></td><td>Rules that all rational people would agree to (Rawls)</td><td>Design AI as if you don't know which group you'll be in</td><td>Assumes rational actors and consensus</td></tr>
    </tbody>
  </table>
  <div class="highlight-box cyan">
    <strong>Rawls' "Veil of Ignorance" Test:</strong> When designing an AI system, imagine you don't know which group you'll belong to — whether you'll be the one the algorithm approves or rejects. Would the system still seem fair?
  </div>
</div>

<div class="card">
  <h3>❌ Real-World AI Ethics Failures <span class="badge">5c</span></h3>
  <div style="display:grid;gap:1rem">
    <div class="callout"><span class="callout-icon">⚖️</span><div class="callout-content"><h5>COMPAS Recidivism Algorithm (2016)</h5><p>Used by US courts to predict reoffending likelihood, COMPAS was found to be twice as likely to falsely flag Black defendants as high-risk (ProPublica investigation). Judges used these scores in sentencing decisions — algorithmic bias directly affecting prison sentences.</p></div></div>
    <div class="callout"><span class="callout-icon">👩‍💼</span><div class="callout-content"><h5>Amazon Hiring Algorithm (2018)</h5><p>Amazon built an ML tool to screen resumes. It learned from 10 years of male-dominated hiring data and penalized resumes with "women's" (e.g., "women's chess club") and downgraded graduates of all-women's colleges. Amazon scrapped it when discovered.</p></div></div>
    <div class="callout"><span class="callout-icon">📸</span><div class="callout-content"><h5>Google Photos Misclassification (2015)</h5><p>Google Photos' image recognition tagged photos of Black users as "gorillas." The training data lacked diversity. Google's fix was to remove the "gorilla" label entirely.</p></div></div>
    <div class="callout"><span class="callout-icon">🏦</span><div class="callout-content"><h5>Apple Card Gender Discrimination (2019)</h5><p>Married couples reported Apple Card's algorithm offering husbands 10–20x higher credit limits than wives — even when wives had better credit scores. Apple and Goldman Sachs faced regulatory investigations.</p></div></div>
  </div>
</div>

<div class="card">
  <h3>🏛️ Key AI Governance Frameworks <span class="badge">5d</span></h3>
  <div style="display:grid;gap:1rem">
    <div style="border:2px solid #4f46e5;border-radius:12px;padding:1.25rem">
      <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.85rem">
        <div style="background:#4f46e5;color:#fff;border-radius:8px;padding:.4rem .8rem;font-size:.85rem;font-weight:700">🇺🇸 NIST AI RMF</div>
        <span style="font-size:.88rem;color:#64748b">AI Risk Management Framework (2023)</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem">
        <div style="background:#eef2ff;border-radius:8px;padding:.85rem;text-align:center"><div style="font-weight:800;color:#4f46e5;font-size:1.1rem">GOVERN</div><div style="font-size:.78rem;color:#475569;margin-top:.3rem">Culture, accountability, and risk policies</div></div>
        <div style="background:#ede9fe;border-radius:8px;padding:.85rem;text-align:center"><div style="font-weight:800;color:#7c3aed;font-size:1.1rem">MAP</div><div style="font-size:.78rem;color:#475569;margin-top:.3rem">Identify context, stakeholders, and risks</div></div>
        <div style="background:#dbeafe;border-radius:8px;padding:.85rem;text-align:center"><div style="font-weight:800;color:#1d4ed8;font-size:1.1rem">MEASURE</div><div style="font-size:.78rem;color:#475569;margin-top:.3rem">Analyze and quantify identified risks</div></div>
        <div style="background:#d1fae5;border-radius:8px;padding:.85rem;text-align:center"><div style="font-weight:800;color:#065f46;font-size:1.1rem">MANAGE</div><div style="font-size:.78rem;color:#475569;margin-top:.3rem">Treat, monitor, and respond to risks</div></div>
      </div>
    </div>
    <div style="border:2px solid #2563eb;border-radius:12px;padding:1.25rem">
      <div style="display:flex;align-items:center;gap:.75rem;margin-bottom:.85rem">
        <div style="background:#2563eb;color:#fff;border-radius:8px;padding:.4rem .8rem;font-size:.85rem;font-weight:700">🇪🇺 EU AI Act</div>
        <span style="font-size:.88rem;color:#64748b">First comprehensive AI law globally (2024)</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.75rem">
        <div style="background:#fef2f2;border-radius:8px;padding:.85rem;text-align:center;border-top:4px solid #ef4444"><div style="font-weight:700;color:#ef4444;font-size:.88rem">UNACCEPTABLE RISK</div><div style="font-size:.75rem;color:#475569;margin-top:.3rem">Banned: social scoring, real-time biometric surveillance</div></div>
        <div style="background:#fff7ed;border-radius:8px;padding:.85rem;text-align:center;border-top:4px solid #f97316"><div style="font-weight:700;color:#ea580c;font-size:.88rem">HIGH RISK</div><div style="font-size:.75rem;color:#475569;margin-top:.3rem">Strict requirements: hiring AI, credit scoring, medical devices</div></div>
        <div style="background:#fefce8;border-radius:8px;padding:.85rem;text-align:center;border-top:4px solid #eab308"><div style="font-weight:700;color:#ca8a04;font-size:.88rem">LIMITED RISK</div><div style="font-size:.75rem;color:#475569;margin-top:.3rem">Transparency obligations: chatbots must disclose they are AI</div></div>
        <div style="background:#f0fdf4;border-radius:8px;padding:.85rem;text-align:center;border-top:4px solid #22c55e"><div style="font-weight:700;color:#16a34a;font-size:.88rem">MINIMAL RISK</div><div style="font-size:.75rem;color:#475569;margin-top:.3rem">Largely unregulated: spam filters, video games</div></div>
      </div>
    </div>
  </div>
</div>

<div class="card">
  <h3>🛡️ Ethical Concerns with LLMs &amp; Generative AI <span class="badge">5e</span></h3>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
    <div class="callout"><span class="callout-icon">🌀</span><div class="callout-content"><h5>Hallucination</h5><p>LLMs confidently generate factually incorrect information. In business contexts — legal, medical, financial — this can cause serious harm. Always verify LLM-generated facts.</p></div></div>
    <div class="callout"><span class="callout-icon">📰</span><div class="callout-content"><h5>Misinformation &amp; Deepfakes</h5><p>GenAI lowers the cost of producing realistic fake images, videos, and text at scale — threatening elections, brand reputation, and public trust.</p></div></div>
    <div class="callout"><span class="callout-icon">🔒</span><div class="callout-content"><h5>Privacy &amp; Data Leakage</h5><p>Employees entering sensitive data into public LLMs risk exposing confidential information. LLMs may also reproduce training data containing personal information.</p></div></div>
    <div class="callout"><span class="callout-icon">⚖️</span><div class="callout-content"><h5>Copyright &amp; IP Issues</h5><p>LLMs trained on copyrighted content raise unresolved legal questions. Companies using AI-generated content face potential IP infringement liability.</p></div></div>
    <div class="callout"><span class="callout-icon">📣</span><div class="callout-content"><h5>Bias Amplification</h5><p>LLMs trained on internet text absorb and amplify societal biases — around gender, race, religion — perpetuating discrimination at unprecedented scale.</p></div></div>
    <div class="callout"><span class="callout-icon">🌍</span><div class="callout-content"><h5>Environmental Impact</h5><p>Training GPT-4 emitted an estimated 500+ metric tons of CO₂. A single ChatGPT conversation uses ~10x more energy than a Google search.</p></div></div>
  </div>
</div>
""", unsafe_allow_html=True)


def section6():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">🏢</span>
  <h2>Organizational Readiness</h2>
  <p>Technology is the easy part. The hard part is transforming people, processes, and culture to become an AI-driven organization. Here's your roadmap.</p>
</div>

<div class="card">
  <h3>📶 AI Maturity Models <span class="badge">6a</span></h3>
  <p>AI maturity models help organizations assess where they are on their AI journey and what it takes to advance. They generally describe five levels:</p>
  <div class="diagram-wrap">
    <svg viewBox="0 0 620 230" width="580" height="215" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="10" width="600" height="210" rx="12" fill="#f8fafc"/>
      <rect x="480" y="30" width="120" height="180" rx="0" fill="#4f46e5" opacity=".9"/>
      <text x="540" y="105" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Inter,sans-serif">LEVEL 5</text>
      <text x="540" y="120" text-anchor="middle" font-size="10" font-weight="800" fill="#fff" font-family="Inter,sans-serif">TRANSFORM-</text>
      <text x="540" y="133" text-anchor="middle" font-size="10" font-weight="800" fill="#fff" font-family="Inter,sans-serif">ATIONAL</text>
      <rect x="360" y="65" width="120" height="145" rx="0" fill="#7c3aed" opacity=".85"/>
      <text x="420" y="130" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Inter,sans-serif">LEVEL 4</text>
      <text x="420" y="145" text-anchor="middle" font-size="10" font-weight="800" fill="#fff" font-family="Inter,sans-serif">SYSTEMIC</text>
      <rect x="240" y="100" width="120" height="110" rx="0" fill="#0891b2" opacity=".85"/>
      <text x="300" y="157" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Inter,sans-serif">LEVEL 3</text>
      <text x="300" y="172" text-anchor="middle" font-size="10" font-weight="800" fill="#fff" font-family="Inter,sans-serif">OPERATIONAL</text>
      <rect x="120" y="135" width="120" height="75" rx="0" fill="#059669" opacity=".85"/>
      <text x="180" y="175" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Inter,sans-serif">LEVEL 2</text>
      <text x="180" y="190" text-anchor="middle" font-size="9" font-weight="800" fill="#fff" font-family="Inter,sans-serif">ACTIVE</text>
      <rect x="20" y="170" width="100" height="40" rx="0" fill="#94a3b8" opacity=".85"/>
      <text x="70" y="192" text-anchor="middle" font-size="9" font-weight="700" fill="#fff" font-family="Inter,sans-serif">LEVEL 1: AWARE</text>
      <rect x="10" y="210" width="600" height="8" rx="0" fill="#1e293b"/>
    </svg>
  </div>
  <table class="styled-table">
    <thead><tr><th>Level</th><th>Description</th><th>Characteristics</th></tr></thead>
    <tbody>
      <tr><td><span class="tag tag-blue">Level 1: Aware</span></td><td>Exploring AI possibilities</td><td>Leadership aware of AI; few or no AI initiatives; data silos; exploring use cases</td></tr>
      <tr><td><span class="tag tag-green">Level 2: Active</span></td><td>Running AI pilots and experiments</td><td>First AI pilots underway; small data science team; limited data governance; learning mode</td></tr>
      <tr><td><span class="tag tag-cyan">Level 3: Operational</span></td><td>AI in production; scaling</td><td>Multiple AI systems in production; MLOps practices; growing AI literacy; governance emerging</td></tr>
      <tr><td><span class="tag tag-purple">Level 4: Systemic</span></td><td>AI across business units</td><td>AI embedded in core processes; AI Center of Excellence; robust data platform; strong governance</td></tr>
      <tr><td><span class="tag tag-blue">Level 5: Transformational</span></td><td>AI is core organizational DNA</td><td>AI-first strategy; continuous innovation; competitive moat from AI; industry leadership</td></tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h3>🗺️ Becoming an AI-First Organization <span class="badge">6b</span></h3>
  <p>Being "AI-first" means AI is embedded in how you think, decide, and operate. Here are the six dimensions of AI transformation:</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem">
    <div style="background:#eef2ff;border-radius:12px;padding:1.25rem;border-left:4px solid #4f46e5"><h5 style="font-weight:700;color:#4f46e5;margin-bottom:.5rem">1. 📊 Data Foundation</h5><p style="font-size:.85rem;color:#475569;margin:0"><strong>The most critical step.</strong> Focus on data quality, unified data platforms, data governance policies, and breaking down data silos between departments.</p></div>
    <div style="background:#ede9fe;border-radius:12px;padding:1.25rem;border-left:4px solid #7c3aed"><h5 style="font-weight:700;color:#7c3aed;margin-bottom:.5rem">2. 🛠️ Technology &amp; Infrastructure</h5><p style="font-size:.85rem;color:#475569;margin:0">Cloud-based ML platforms (AWS SageMaker, Azure ML, GCP Vertex AI), MLOps for model deployment and monitoring, scalable compute.</p></div>
    <div style="background:#d1fae5;border-radius:12px;padding:1.25rem;border-left:4px solid #10b981"><h5 style="font-weight:700;color:#065f46;margin-bottom:.5rem">3. 👥 People &amp; Skills</h5><p style="font-size:.85rem;color:#475569;margin:0">Build a mix of data scientists, ML engineers, AI-literate business stakeholders, and translators who bridge technical and business teams.</p></div>
    <div style="background:#cffafe;border-radius:12px;padding:1.25rem;border-left:4px solid #06b6d4"><h5 style="font-weight:700;color:#0e7490;margin-bottom:.5rem">4. 🔄 Process Redesign</h5><p style="font-size:.85rem;color:#475569;margin:0">AI doesn't just automate old processes — it enables entirely new ways of working. Map current processes, identify AI integration points, redesign workflows.</p></div>
    <div style="background:#fef3c7;border-radius:12px;padding:1.25rem;border-left:4px solid #f59e0b"><h5 style="font-weight:700;color:#92400e;margin-bottom:.5rem">5. 🧭 Culture &amp; Leadership</h5><p style="font-size:.85rem;color:#475569;margin:0">The hardest dimension. Leaders must model data-driven decision making, celebrate experimentation, address fear of AI-driven job displacement transparently.</p></div>
    <div style="background:#fce7f3;border-radius:12px;padding:1.25rem;border-left:4px solid #db2777"><h5 style="font-weight:700;color:#9d174d;margin-bottom:.5rem">6. ⚖️ Governance &amp; Ethics</h5><p style="font-size:.85rem;color:#475569;margin:0">Establish an AI governance committee, create an AI use-case review process, implement ethics guidelines from day one, define acceptable AI use policies.</p></div>
  </div>
  <div class="section-divider"></div>
  <div class="sub-section-title">Manager's Action Plan</div>
  <div style="background:#f8fafc;border-radius:12px;padding:1.25rem;border:1px solid #e2e8f0">
    <div style="display:grid;gap:.65rem">
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#4f46e5;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">1</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Assess your maturity:</strong> Honestly evaluate where your organization sits on the maturity model. Most are at Level 1–2.</p></div>
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#7c3aed;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">2</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Audit your data:</strong> Start a data inventory and governance initiative before any AI project. "Garbage in, garbage out" is real.</p></div>
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#06b6d4;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">3</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Pick a high-value pilot:</strong> Choose a use case with clear business value, available data, and manageable risk. Prove value quickly.</p></div>
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#10b981;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">4</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Build your team:</strong> Hire or develop a data scientist / ML engineer. Identify business translators who can bridge tech and business.</p></div>
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#f59e0b;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">5</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Lead the culture change:</strong> Communicate openly, address concerns, celebrate learning, and visibly champion data-driven decision-making from the top.</p></div>
      <div style="display:flex;gap:.75rem;align-items:flex-start"><div style="background:#ef4444;color:#fff;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700;flex-shrink:0">6</div><p style="font-size:.88rem;color:#475569;margin:0"><strong>Establish governance early:</strong> Establish AI ethics and governance policies before you scale — it's much harder to retrofit.</p></div>
    </div>
  </div>
</div>

<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:16px;padding:2.5rem;margin-top:2rem;color:#fff;text-align:center">
  <div style="font-size:3rem;margin-bottom:1rem">🎉</div>
  <h3 style="font-size:1.5rem;font-weight:800;margin-bottom:.75rem;color:#fff">Congratulations! You've Completed the Tutorial</h3>
  <p style="opacity:.85;max-width:500px;margin:0 auto;line-height:1.65;color:#fff">You've covered the essential AI concepts every modern manager needs to know — from the foundations of ML to ethics, governance, and organizational transformation.</p>
</div>
""", unsafe_allow_html=True)


def section7():
    st.markdown("""
<div class="section-hero">
  <span class="hero-icon">📚</span>
  <h2>References &amp; Acknowledgments</h2>
  <p>This tutorial draws on foundational academic works, landmark research papers, authoritative governance frameworks, and award-winning investigative journalism.</p>
</div>

<div class="card">
  <h3>📗 Foundational Textbooks</h3>
  <div style="display:grid;gap:.85rem">
    <div class="callout"><span class="callout-icon">📗</span><div class="callout-content"><h5>Artificial Intelligence: A Modern Approach (4th ed.)</h5><p>Russell, S., &amp; Norvig, P. (2020). Pearson. — The definitive AI textbook. Covers all major AI paradigms. Used in hundreds of university AI courses worldwide.</p></div></div>
    <div class="callout"><span class="callout-icon">📘</span><div class="callout-content"><h5>Deep Learning</h5><p>Goodfellow, I., Bengio, Y., &amp; Courville, A. (2016). MIT Press. — The comprehensive reference for deep learning theory. Freely available at deeplearningbook.org.</p></div></div>
    <div class="callout"><span class="callout-icon">📙</span><div class="callout-content"><h5>Machine Learning</h5><p>Mitchell, T. M. (1997). McGraw-Hill. — The classic introduction to ML. Mitchell's definition of machine learning remains the standard in the field.</p></div></div>
    <div class="callout"><span class="callout-icon">📕</span><div class="callout-content"><h5>Reinforcement Learning: An Introduction (2nd ed.)</h5><p>Sutton, R. S., &amp; Barto, A. G. (2018). MIT Press. — The authoritative textbook on RL. Freely available at incompleteideas.net.</p></div></div>
    <div class="callout"><span class="callout-icon">📒</span><div class="callout-content"><h5>The Alignment Problem</h5><p>Christian, B. (2020). W. W. Norton. — A compelling narrative about the challenge of aligning AI systems with human values. Essential for managers concerned about AI ethics.</p></div></div>
    <div class="callout"><span class="callout-icon">📓</span><div class="callout-content"><h5>Weapons of Math Destruction</h5><p>O'Neil, C. (2016). Crown. — Investigates how mathematical models can reinforce inequality in hiring, lending, education, and criminal justice.</p></div></div>
  </div>
</div>

<div class="card">
  <h3>📜 Landmark Research Papers</h3>
  <table class="styled-table">
    <thead><tr><th>Year</th><th>Paper</th><th>Authors</th><th>Significance</th></tr></thead>
    <tbody>
      <tr><td>1950</td><td><em>Computing Machinery and Intelligence</em></td><td>Alan Turing</td><td>Proposed the "Turing Test"; foundational to the field of AI.</td></tr>
      <tr><td>2012</td><td><em>ImageNet Classification with Deep CNNs (AlexNet)</em></td><td>Krizhevsky, Sutskever, Hinton</td><td>Launched the deep learning revolution — won ImageNet with a huge margin.</td></tr>
      <tr><td>2014</td><td><em>Generative Adversarial Networks</em></td><td>Goodfellow et al.</td><td>Introduced GANs — the first approach capable of generating photorealistic synthetic images.</td></tr>
      <tr><td>2016</td><td><em>Mastering the game of Go with deep neural networks</em></td><td>Silver et al. (DeepMind)</td><td>AlphaGo defeats world champion Lee Sedol. Published in <em>Nature</em>.</td></tr>
      <tr><td>2017</td><td><em>Attention Is All You Need</em></td><td>Vaswani et al. (Google)</td><td>Introduced the Transformer architecture — the foundation for GPT, BERT, Claude, Gemini, and all modern LLMs.</td></tr>
      <tr><td>2018</td><td><em>Gender Shades</em></td><td>Buolamwini &amp; Gebru (MIT)</td><td>Documented significant racial and gender bias in commercial facial recognition systems.</td></tr>
      <tr><td>2020</td><td><em>Language Models are Few-Shot Learners (GPT-3)</em></td><td>Brown et al. (OpenAI)</td><td>Demonstrated that very large language models can perform diverse tasks with minimal examples.</td></tr>
      <tr><td>2021</td><td><em>Highly accurate protein structure prediction with AlphaFold</em></td><td>Jumper et al. (DeepMind)</td><td>Solved the 50-year protein folding problem — transforming biology and drug discovery.</td></tr>
    </tbody>
  </table>
</div>

<div class="card">
  <h3>🏛️ Governance Frameworks &amp; Industry Reports</h3>
  <div style="display:grid;gap:.85rem">
    <div class="callout"><span class="callout-icon">🇺🇸</span><div class="callout-content"><h5>NIST AI Risk Management Framework (AI RMF 1.0)</h5><p>National Institute of Standards and Technology. (2023). The U.S. voluntary framework for managing AI risk across four functions: Govern, Map, Measure, Manage.</p></div></div>
    <div class="callout"><span class="callout-icon">🇪🇺</span><div class="callout-content"><h5>EU Artificial Intelligence Act</h5><p>European Parliament. (2024). The world's first comprehensive legal framework for AI, using a risk-based tiered approach from unacceptable risk (banned) to minimal risk.</p></div></div>
    <div class="callout"><span class="callout-icon">🌐</span><div class="callout-content"><h5>OECD Principles on Artificial Intelligence</h5><p>OECD. (2019, updated 2024). Five principles for responsible AI stewardship adopted by 46 countries covering inclusive growth, transparency, robustness, and accountability.</p></div></div>
    <div class="callout"><span class="callout-icon">📊</span><div class="callout-content"><h5>McKinsey Global Institute: The Age of AI</h5><p>McKinsey &amp; Company. (2023). Estimates generative AI could add $2.6–4.4 trillion annually to the global economy with industry-by-industry analysis.</p></div></div>
    <div class="callout"><span class="callout-icon">🌱</span><div class="callout-content"><h5>Stanford AI Index Report</h5><p>Maslej, N., et al. (2024). Stanford HAI. Comprehensive annual report tracking AI research, technical progress, ethics, policy, and economic impact worldwide.</p></div></div>
  </div>
</div>

<div class="card" style="background:linear-gradient(135deg,#f8fafc,#eef2ff);border:2px solid #c7d2fe">
  <h3>ℹ️ About This Tutorial</h3>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem">
    <div>
      <p><strong>Creator:</strong> <span style="color:#4f46e5;font-weight:700">Sridhar Nerur</span></p>
      <p style="font-size:.88rem;color:#475569">This tutorial was designed and created by Sridhar Nerur as an interactive educational resource for managers and business leaders navigating the AI transformation era.</p>
    </div>
    <div>
      <p><strong>Built with:</strong> <span style="color:#7c3aed;font-weight:700">Claude (Anthropic)</span></p>
      <p style="font-size:.88rem;color:#475569">The application was developed using Claude, Anthropic's AI assistant, which aided in structuring content, writing explanations, generating SVG illustrations, and building the application.</p>
      <div style="margin-top:.75rem"><span class="tag tag-blue">Python / Streamlit</span><span class="tag tag-purple">OpenAI API</span><span class="tag tag-green">Groq API</span><span class="tag tag-amber">SVG Illustrations</span></div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Quiz renderer ────────────────────────────────────────────
def render_quiz(section_num: int):
    if section_num not in QUIZ:
        return
    qdata = QUIZ[section_num]
    questions = qdata["questions"]
    total = len(questions)
    key = f"quiz_{section_num}"

    if key not in st.session_state.quiz:
        st.session_state.quiz[key] = {"current_q": 0, "answers": {}, "complete": False}

    state = st.session_state.quiz[key]

    st.markdown(f"""
<div style="background:#fff;border-radius:14px;padding:1.75rem;border:2px solid #4f46e5;margin-top:1.5rem">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
    <h3 style="margin:0;color:#4f46e5;font-size:1.1rem">❓ {qdata['title']}</h3>
    <span style="font-size:.82rem;color:#64748b;background:#eef2ff;padding:.3rem .75rem;border-radius:20px;font-weight:600">
      {"Complete ✅" if state["complete"] else f"Question {state['current_q']+1} of {total}"}
    </span>
  </div>
""", unsafe_allow_html=True)

    if state["complete"]:
        score = sum(1 for qi, chosen in state["answers"].items() if chosen == questions[qi]["ans"])
        pct = round(score / total * 100)
        emoji = "🎉" if pct == 100 else "⭐" if pct >= 80 else "👍" if pct >= 60 else "📖"
        msg = "Perfect Score!" if pct == 100 else "Excellent!" if pct >= 80 else "Well Done!" if pct >= 60 else "Good Start!" if pct >= 40 else "Keep Studying!"
        st.markdown(f"""
<div style="text-align:center;padding:1.5rem 0">
  <div style="font-size:3rem;margin-bottom:.5rem">{emoji}</div>
  <div style="font-size:2.5rem;font-weight:800;color:#4f46e5">{score}/{total}</div>
  <div style="font-size:1.2rem;font-weight:700;color:#1e293b;margin:.5rem 0">{msg}</div>
  <div style="font-size:.9rem;color:#64748b">{pct}% correct</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("↩ Retake Quiz", key=f"retake_{section_num}"):
            st.session_state.quiz[key] = {"current_q": 0, "answers": {}, "complete": False}
            st.rerun()
        return

    qi = state["current_q"]
    q = questions[qi]
    letters = ["A", "B", "C", "D"]

    st.markdown(f"""
<p style="font-size:1rem;font-weight:600;color:#1e293b;margin-bottom:1rem">
  <span style="background:#4f46e5;color:#fff;border-radius:6px;padding:.2rem .5rem;font-size:.82rem;margin-right:.5rem">Q{qi+1}</span>
  {q['q']}
</p>
""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    already_answered = qi in state["answers"]
    chosen = state["answers"].get(qi, None)

    if already_answered:
        correct = q["ans"]
        for i, opt in enumerate(q["opts"]):
            if i == correct:
                color, icon = "#d1fae5", "✅"
                border = "2px solid #10b981"
            elif i == chosen:
                color, icon = "#fee2e2", "❌"
                border = "2px solid #ef4444"
            else:
                color, icon = "#f8fafc", ""
                border = "1px solid #e2e8f0"
            st.markdown(f"""
<div style="background:{color};border:{border};border-radius:10px;padding:.75rem 1rem;margin-bottom:.5rem;display:flex;align-items:center;gap:.65rem">
  <span style="background:#e2e8f0;border-radius:6px;padding:.15rem .45rem;font-size:.78rem;font-weight:700;color:#475569">{letters[i]}</span>
  <span style="font-size:.9rem;color:#374151">{opt}</span>
  <span style="margin-left:auto">{icon}</span>
</div>
""", unsafe_allow_html=True)
        st.markdown(f"""
<div style="background:#fffbeb;border-left:4px solid #f59e0b;border-radius:0 10px 10px 0;padding:.9rem 1.1rem;margin-top:.75rem;font-size:.88rem;color:#374151">
  💡 <strong>Explanation:</strong> {q['exp']}
</div>
""", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if qi > 0:
                if st.button("← Previous", key=f"prev_{section_num}_{qi}"):
                    st.session_state.quiz[key]["current_q"] = qi - 1
                    st.rerun()
        with col2:
            label = "Finish Quiz →" if qi == total - 1 else "Next Question →"
            if st.button(label, key=f"next_{section_num}_{qi}", type="primary"):
                if qi == total - 1:
                    st.session_state.quiz[key]["complete"] = True
                else:
                    st.session_state.quiz[key]["current_q"] = qi + 1
                st.rerun()
    else:
        for i, opt in enumerate(q["opts"]):
            if st.button(f"  {letters[i]}.  {opt}", key=f"opt_{section_num}_{qi}_{i}"):
                st.session_state.quiz[key]["answers"][qi] = i
                st.rerun()


# ── AI chat ──────────────────────────────────────────────────
def get_ai_response(message: str, context: str, history: list) -> str:
    mode = st.session_state.api_mode
    openai_key = st.session_state.openai_key.strip()
    groq_key   = st.session_state.groq_key.strip()

    if mode == "demo":
        if _SERVER_OPENAI_KEY:
            api_key, base_url, model = _SERVER_OPENAI_KEY, None, "gpt-4o-mini"
        elif _SERVER_GROQ_KEY:
            api_key, base_url, model = _SERVER_GROQ_KEY, GROQ_BASE_URL, GROQ_FREE_MODEL
        else:
            return "⚠ Demo mode is not configured on this server. Please enter your own API key in Settings."
    elif mode == "groq":
        if not groq_key:
            return "⚠ Please enter your Groq API key in Settings (sidebar). Get a free key at console.groq.com."
        api_key, base_url, model = groq_key, GROQ_BASE_URL, GROQ_FREE_MODEL
    else:
        if not openai_key:
            return "⚠ Please enter your OpenAI API key in Settings (sidebar)."
        api_key, base_url, model = openai_key, None, st.session_state.openai_model

    system_prompt = (
        "You are an expert AI tutor helping non-technical managers understand AI concepts.\n"
        f"The learner is currently studying: **{context}**.\n\n"
        "Guidelines:\n"
        "• Use plain, business-friendly language — avoid jargon unless you explain it.\n"
        "• Anchor explanations to real-world business examples managers can relate to.\n"
        "• Be concise: 2–4 short paragraphs unless more detail is truly needed.\n"
        "• Be encouraging, positive, and supportive."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for turn in history[-6:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    try:
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
        resp = client.chat.completions.create(model=model, messages=messages, max_tokens=700, temperature=0.7)
        return resp.choices[0].message.content
    except Exception as e:
        msg = str(e).lower()
        if "auth" in msg or "api_key" in msg or "invalid" in msg:
            return "⚠ Invalid API key. Please check your key in Settings."
        if "quota" in msg or "billing" in msg or "rate" in msg:
            return "⚠ API quota or rate limit reached. Try again shortly or switch access mode."
        return f"⚠ Unexpected error: {e}"


# ── Sidebar ──────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
<div style="padding:.5rem 0 1rem;border-bottom:1px solid #e2e8f0;margin-bottom:.75rem">
  <div style="font-size:1.1rem;font-weight:800;color:#4f46e5">🧠 AI for Managers</div>
  <div style="font-size:.72rem;color:#64748b;margin-top:.2rem">Interactive Tutorial · Sridhar Nerur</div>
</div>
""", unsafe_allow_html=True)

        # Progress
        total_sections = 6
        completed = len([s for s in range(1, 7) if s in st.session_state.completed])
        pct = int(completed / total_sections * 100)
        st.markdown(f"""
<div style="margin-bottom:1rem">
  <div style="font-size:.72rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.4rem">YOUR PROGRESS</div>
  <div style="background:#e2e8f0;border-radius:8px;height:8px;overflow:hidden">
    <div style="height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4);width:{pct}%;transition:width .5s"></div>
  </div>
  <div style="font-size:.72rem;color:#64748b;margin-top:.3rem">{completed}/{total_sections} modules visited · {pct}%</div>
</div>
""", unsafe_allow_html=True)

        # Navigation
        st.markdown('<div style="font-size:.68rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.4rem">MODULES</div>', unsafe_allow_html=True)

        nav_items = [
            (1, "🚀", "1. Introduction to AI"),
            (2, "🏷️", "2. Supervised Learning"),
            (3, "🔍", "3. Unsupervised Learning"),
            (4, "🎮", "4. Reinforcement Learning"),
            (5, "⚖️", "5. AI Ethics & Governance"),
            (6, "🏢", "6. Organizational Readiness"),
        ]
        for num, icon, label in nav_items:
            done = "✅ " if num in st.session_state.completed else ""
            is_active = st.session_state.section == num
            btn_style = "primary" if is_active else "secondary"
            if st.button(f"{done}{icon} {label}", key=f"nav_{num}", use_container_width=True, type=btn_style):
                st.session_state.section = num
                st.session_state.completed.add(num)
                st.rerun()

        st.markdown('<div style="font-size:.68rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.08em;margin:1rem 0 .4rem">RESOURCES</div>', unsafe_allow_html=True)
        if st.button("📚 References", key="nav_7", use_container_width=True,
                     type="primary" if st.session_state.section == 7 else "secondary"):
            st.session_state.section = 7
            st.rerun()

        # Settings
        st.markdown("---")
        with st.expander("⚙️ AI Tutor Settings", expanded=False):
            demo_available = bool(_SERVER_OPENAI_KEY or _SERVER_GROQ_KEY)
            mode_options = ["openai", "groq"]
            if demo_available:
                mode_options = ["demo"] + mode_options
            mode_labels = {"demo": "🎁 Free Demo", "openai": "🤖 OpenAI", "groq": "⚡ Groq (Free)"}
            current_idx = mode_options.index(st.session_state.api_mode) if st.session_state.api_mode in mode_options else 0
            selected = st.radio("Access Mode", mode_options, index=current_idx,
                                format_func=lambda x: mode_labels[x], key="mode_radio")
            st.session_state.api_mode = selected

            if selected == "openai":
                key_val = st.text_input("OpenAI API Key", value=st.session_state.openai_key,
                                        type="password", placeholder="sk-...", key="oai_key_input")
                st.session_state.openai_key = key_val
                model_choice = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], key="model_select",
                                            index=0 if st.session_state.openai_model == "gpt-4o-mini" else 1)
                st.session_state.openai_model = model_choice
                st.caption("Get a free key at platform.openai.com")
            elif selected == "groq":
                key_val = st.text_input("Groq API Key", value=st.session_state.groq_key,
                                        type="password", placeholder="gsk_...", key="groq_key_input")
                st.session_state.groq_key = key_val
                st.caption("Free key at console.groq.com — no payment needed")
            else:
                st.success("Demo mode — no API key required!")

        # Chat
        st.markdown("---")
        chat_label = "💬 Hide AI Tutor" if st.session_state.show_chat else "💬 Ask AI Tutor"
        if st.button(chat_label, use_container_width=True, key="chat_toggle"):
            st.session_state.show_chat = not st.session_state.show_chat
            st.rerun()


# ── Chat panel ───────────────────────────────────────────────
def render_chat():
    context = SECTION_NAMES.get(st.session_state.section, "AI for Managers")
    st.markdown(f"""
<div style="background:linear-gradient(135deg,#4f46e5,#7c3aed);border-radius:14px 14px 0 0;padding:1rem 1.25rem;display:flex;align-items:center;gap:.75rem">
  <span style="font-size:1.5rem">🤖</span>
  <div>
    <div style="font-size:1rem;font-weight:700;color:#fff">AI Tutor</div>
    <div style="font-size:.75rem;color:rgba(255,255,255,.75)">Topic: {context}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    if not st.session_state.chat_msgs:
        st.session_state.chat_msgs.append({
            "role": "assistant",
            "content": "👋 Hi! I'm your AI tutor. Ask me anything about the AI concepts in this tutorial — I'll explain them in plain business language."
        })

    for msg in st.session_state.chat_msgs:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything about AI…"):
        st.session_state.chat_msgs.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking…"):
                response = get_ai_response(prompt, context, st.session_state.chat_msgs[:-1])
            st.markdown(response)
        st.session_state.chat_msgs.append({"role": "assistant", "content": response})


# ── Main app ─────────────────────────────────────────────────
def main():
    render_sidebar()

    section = st.session_state.section
    section_fns = {1: section1, 2: section2, 3: section3, 4: section4, 5: section5, 6: section6, 7: section7}

    if st.session_state.show_chat:
        col_content, col_chat = st.columns([3, 2])
        with col_content:
            section_fns[section]()
            if section in QUIZ:
                render_quiz(section)
            _nav_buttons(section)
        with col_chat:
            render_chat()
    else:
        section_fns[section]()
        if section in QUIZ:
            render_quiz(section)
        _nav_buttons(section)


def _nav_buttons(section: int):
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    cols = st.columns([1, 4, 1])
    with cols[0]:
        if section > 1:
            prev = section - 1
            if st.button(f"← {SECTION_NAMES[prev]}", key="prev_nav"):
                st.session_state.section = prev
                st.session_state.completed.add(prev)
                st.rerun()
    with cols[2]:
        if section < 7:
            nxt = section + 1
            if st.button(f"{SECTION_NAMES[nxt]} →", key="next_nav", type="primary"):
                st.session_state.section = nxt
                st.session_state.completed.add(section)
                st.rerun()


if __name__ == "__main__":
    main()
