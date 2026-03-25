/* ============================================================
   AI for Managers — App Logic
   Created by Sridhar Nerur · Built with Claude (Anthropic)
   ============================================================ */

// Server capability flags (populated on load from /api/status)
let serverDemoAvailable = false;

// ── Section Navigation ─────────────────────────────────────

let currentSection = 'section-0';
let sidebarVisible = true;
const completedSections = new Set();

function showSection(id) {
  document.querySelectorAll('.tutorial-section').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

  const target = document.getElementById(id);
  if (target) {
    target.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  const navEl = document.querySelector(`[data-section="${id}"]`);
  if (navEl) navEl.classList.add('active');

  currentSection = id;
  updateChatContext();
  updateProgress();
  markSectionVisited(id);
}

function markSectionVisited(id) {
  completedSections.add(id);
  const navEl = document.querySelector(`[data-section="${id}"]`);
  if (navEl) navEl.classList.add('completed');
  updateProgress();
}

function updateProgress() {
  const total = document.querySelectorAll('.nav-item[data-section]').length;
  const pct = total > 0 ? Math.round((completedSections.size / total) * 100) : 0;
  document.getElementById('progress-bar').style.width = pct + '%';
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const main = document.getElementById('main');
  sidebarVisible = !sidebarVisible;
  if (window.innerWidth <= 768) {
    sidebar.classList.toggle('mobile-open');
  } else {
    sidebar.classList.toggle('hidden');
    main.classList.toggle('expanded');
  }
}

// Sub-section scroll
function scrollToSub(subId) {
  const el = document.getElementById(subId);
  if (el) {
    const yOffset = -80;
    const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }
}

// ── Quiz Engine ─────────────────────────────────────────────

const quizData = {
  quiz1: {
    title: 'Quiz: Introduction to AI',
    questions: [
      {
        q: 'What is the correct hierarchical relationship between AI, ML, and Deep Learning?',
        options: ['They are three separate, unrelated fields', 'AI ⊃ ML ⊃ Deep Learning ⊃ Generative AI', 'Deep Learning ⊃ ML ⊃ AI', 'They are all the same thing'],
        correct: 1,
        exp: 'AI is the broadest concept. Machine Learning is a subset of AI. Deep Learning is a subset of ML, and Generative AI leverages Deep Learning techniques.'
      },
      {
        q: 'What makes Generative AI fundamentally different from earlier AI systems?',
        options: ['It is faster at calculations', 'It creates new, original content such as text, images, and code', 'It only works with structured data', 'It requires no training data'],
        correct: 1,
        exp: 'Generative AI can produce new content — not just analyze or classify existing data. Systems like ChatGPT, DALL-E, and Stable Diffusion are prime examples.'
      },
      {
        q: 'The term "Artificial Intelligence" was formally coined at which event?',
        options: ['The Turing Conference (1950)', 'The Dartmouth Summer Research Project (1956)', 'The MIT AI Lab founding (1970)', 'The ImageNet competition (2012)'],
        correct: 1,
        exp: 'John McCarthy coined the term "Artificial Intelligence" at the 1956 Dartmouth Summer Research Project — widely regarded as the birth of AI as a field.'
      },
      {
        q: 'Which of the following best describes a challenge (not an opportunity) of AI for businesses?',
        options: ['Automating repetitive tasks', 'Improving customer personalization', 'Data quality and governance concerns', 'Faster fraud detection'],
        correct: 2,
        exp: 'Data quality and governance is a key challenge — AI systems are only as good as the data they learn from. Poor or biased data leads to unreliable or harmful outcomes.'
      },
      {
        q: 'A hospital uses AI to detect tumors in X-ray images. Which AI category does this fall under?',
        options: ['Generative AI', 'Reinforcement Learning', 'Deep Learning / Computer Vision', 'Expert Systems'],
        correct: 2,
        exp: 'Medical image analysis uses Deep Learning (specifically Convolutional Neural Networks) which can detect patterns in images that would take human radiologists much longer to spot.'
      }
    ]
  },
  quiz2: {
    title: 'Quiz: Supervised Learning',
    questions: [
      {
        q: 'What does "supervised" mean in supervised learning?',
        options: ['A human supervisor monitors the algorithm in real time', 'The algorithm learns from labeled training data (input + known output)', 'The algorithm supervises other algorithms', 'No data is required — the algorithm self-supervises'],
        correct: 1,
        exp: 'In supervised learning, the training data has labels — each input example comes with the correct answer. The model learns to map inputs to outputs by studying these examples.'
      },
      {
        q: 'A bank wants to predict the loan amount a customer will need. This is best framed as a:',
        options: ['Classification problem', 'Clustering problem', 'Regression problem', 'Reinforcement learning problem'],
        correct: 2,
        exp: 'Predicting a continuous numerical value (loan amount in dollars) is a regression problem. If the bank only wanted to predict "approve/deny," that would be classification.'
      },
      {
        q: 'Which of these is an example of a classification problem?',
        options: ['Forecasting next quarter\'s revenue', 'Estimating delivery time in hours', 'Detecting whether an email is spam or not spam', 'Predicting a patient\'s blood pressure level'],
        correct: 2,
        exp: 'Spam detection is a binary classification — is the email spam (yes) or not (no)? Revenue forecasting and blood pressure prediction are regression problems.'
      },
      {
        q: 'Which algorithm is a powerful ensemble method widely used for both regression and classification?',
        options: ['K-Means Clustering', 'Principal Component Analysis (PCA)', 'Random Forest', 'Q-Learning'],
        correct: 2,
        exp: 'Random Forest builds many decision trees and combines their results. It\'s robust, handles missing data well, and is a go-to algorithm for supervised learning problems.'
      },
      {
        q: 'A retailer uses an algorithm to predict which customers will stop buying (churn) in the next 30 days. This is:',
        options: ['Regression — predicting a continuous probability', 'Classification — labeling customers as likely to churn or not', 'Unsupervised — there are no labels needed', 'Both A and B, depending on the output format'],
        correct: 3,
        exp: 'Great insight! If the output is a probability score (0–1), it\'s technically regression. If the output is a binary label (churn / no churn), it\'s classification. Many churn models do both!'
      }
    ]
  },
  quiz3: {
    title: 'Quiz: Unsupervised Learning',
    questions: [
      {
        q: 'What is the key distinction of unsupervised learning?',
        options: ['It requires more labeled data than supervised learning', 'It finds patterns in data without predefined labels or correct answers', 'It always produces better results than supervised learning', 'It only works with image data'],
        correct: 1,
        exp: 'Unsupervised learning discovers hidden structure in unlabeled data. No one tells the algorithm what to look for — it finds groups, patterns, or anomalies on its own.'
      },
      {
        q: 'A marketing team wants to group customers into segments based on purchase behavior, with no predefined categories. This is:',
        options: ['Supervised learning (classification)', 'Reinforcement learning', 'Unsupervised learning (clustering)', 'Deep learning only'],
        correct: 2,
        exp: 'Customer segmentation without predefined groups is classic unsupervised clustering. Algorithms like K-Means discover natural groupings in the data.'
      },
      {
        q: 'Which technique is used to detect unusual transactions that may indicate fraud?',
        options: ['Regression', 'Clustering', 'Anomaly Detection', 'Sentiment Analysis'],
        correct: 2,
        exp: 'Anomaly detection identifies data points that deviate significantly from normal patterns — making it ideal for fraud detection, cybersecurity, and equipment failure prediction.'
      },
      {
        q: 'What does the K-Means algorithm\'s "K" represent?',
        options: ['The number of training iterations', 'The number of clusters to form', 'The minimum data points required', 'The learning rate'],
        correct: 1,
        exp: 'In K-Means, K is the number of clusters you want the algorithm to find. Choosing the right K is an art — too few misses nuance, too many creates noise.'
      },
      {
        q: 'A retailer discovers that customers who buy diapers also tend to buy beer. Which technique revealed this insight?',
        options: ['Linear Regression', 'K-Means Clustering', 'Association Rule Mining', 'Principal Component Analysis'],
        correct: 2,
        exp: 'The famous "beer and diapers" insight came from association rule mining (market basket analysis). It finds rules like "if X is bought, Y is also bought" — used in product recommendations.'
      }
    ]
  },
  quiz4: {
    title: 'Quiz: Reinforcement Learning',
    questions: [
      {
        q: 'In reinforcement learning, what is the "agent"?',
        options: ['The dataset used for training', 'The algorithm or system that makes decisions and takes actions', 'The reward signal that guides learning', 'The human trainer monitoring the system'],
        correct: 1,
        exp: 'The agent is the learner or decision-maker. It observes the environment, chooses actions, and receives rewards or penalties based on those actions.'
      },
      {
        q: 'What does the agent aim to maximize in reinforcement learning?',
        options: ['The speed of individual decisions', 'Cumulative long-term reward', 'The size of the training dataset', 'The number of possible actions'],
        correct: 1,
        exp: 'RL agents optimize for cumulative reward over time — not just immediate gains. This is why RL can learn strategies that sacrifice short-term rewards for greater long-term payoffs.'
      },
      {
        q: 'DeepMind\'s AlphaGo defeated world champion Go players. Which AI approach enabled this?',
        options: ['Supervised learning with expert game data', 'Unsupervised clustering of game states', 'Reinforcement learning through millions of self-play games', 'Rule-based expert systems'],
        correct: 2,
        exp: 'AlphaGo used reinforcement learning — playing millions of games against itself to discover strategies beyond human knowledge. It also used supervised learning from human games initially.'
      },
      {
        q: 'A company uses AI to dynamically adjust its pricing based on demand, competition, and inventory. This is closest to:',
        options: ['Supervised classification', 'Unsupervised clustering', 'Reinforcement learning', 'Generative AI'],
        correct: 2,
        exp: 'Dynamic pricing is a sequential decision-making problem where actions (price changes) affect future state (demand, inventory). RL is well-suited for such problems.'
      },
      {
        q: 'Why is reinforcement learning generally harder to deploy in business than supervised learning?',
        options: ['It requires much less data', 'It only works in virtual environments', 'Actions have delayed consequences, real-world trials can be costly, and rewards are hard to define', 'It is slower to compute predictions'],
        correct: 2,
        exp: 'RL challenges include: defining a good reward function, the cost of real-world exploration (wrong actions can be expensive or dangerous), and delayed feedback making it hard to attribute which action caused a reward.'
      }
    ]
  },
  quiz5: {
    title: 'Quiz: AI Ethics & Governance',
    questions: [
      {
        q: 'The COMPAS recidivism algorithm scandal highlighted which key AI ethics concern?',
        options: ['The system was too slow to be useful', 'The algorithm had racial bias, predicting higher recidivism for Black defendants than warranted', 'The algorithm was too expensive for courts to use', 'The algorithm violated copyright law'],
        correct: 1,
        exp: 'ProPublica\'s 2016 investigation found COMPAS was twice as likely to falsely flag Black defendants as high risk compared to white defendants — a stark example of AI bias with life-changing consequences.'
      },
      {
        q: 'Which ethical principle requires that AI decisions can be understood, audited, and explained?',
        options: ['Sustainability', 'Fairness', 'Transparency and Explainability', 'Security'],
        correct: 2,
        exp: 'Transparency means AI systems should be understandable — stakeholders should be able to know why a decision was made. This is especially critical in high-stakes domains like credit, hiring, and medicine.'
      },
      {
        q: 'The EU AI Act classifies AI systems primarily based on:',
        options: ['The nationality of the developer', 'The programming language used', 'Risk levels — from unacceptable risk to minimal risk', 'The size of the company deploying the AI'],
        correct: 2,
        exp: 'The EU AI Act uses a risk-based approach: Unacceptable (banned), High-risk (strict requirements), Limited risk (transparency obligations), and Minimal risk (largely unregulated).'
      },
      {
        q: 'A large language model confidently states an incorrect historical fact as if it were true. This is known as:',
        options: ['Model drift', 'Hallucination', 'Adversarial attack', 'Overfitting'],
        correct: 1,
        exp: 'AI "hallucination" refers to when LLMs generate plausible-sounding but factually incorrect content with apparent confidence. This is a critical concern for business use cases requiring accuracy.'
      },
      {
        q: 'The NIST AI Risk Management Framework (AI RMF) organizes AI risk management into which four core functions?',
        options: ['Plan, Build, Test, Deploy', 'Govern, Map, Measure, Manage', 'Identify, Protect, Detect, Respond', 'Collect, Process, Analyze, Act'],
        correct: 1,
        exp: 'The NIST AI RMF uses GOVERN (culture & accountability), MAP (context & risk identification), MEASURE (risk analysis & assessment), and MANAGE (risk treatment and monitoring).'
      }
    ]
  },
  quiz6: {
    title: 'Quiz: Organizational Readiness',
    questions: [
      {
        q: 'What does an AI maturity model primarily help an organization assess?',
        options: ['Which AI vendor to purchase from', 'Their current AI capabilities and a roadmap for advancement', 'The technical specifications of AI hardware', 'Legal compliance requirements'],
        correct: 1,
        exp: 'AI maturity models provide a structured framework to assess where an organization currently stands on its AI journey and what capabilities it needs to develop to reach the next level.'
      },
      {
        q: 'Which is the most foundational step when starting an AI transformation journey?',
        options: ['Hiring a Chief AI Officer immediately', 'Purchasing the latest AI software tools', 'Building a strong data foundation — quality, governance, and accessibility', 'Training all employees on advanced ML algorithms'],
        correct: 2,
        exp: 'AI systems are only as good as the data they\'re built on. Before anything else, organizations need high-quality, well-governed, accessible data. "Garbage in, garbage out" is real.'
      },
      {
        q: 'Which cultural characteristic is most critical for an AI-first organization?',
        options: ['Replacing all human judgment with AI decisions', 'Fostering a data-driven, experiment-friendly, learning culture', 'Keeping AI initiatives confidential to maintain competitive advantage', 'Centralizing all AI work in the IT department'],
        correct: 1,
        exp: 'Culture eats strategy for breakfast — and AI transformation. Organizations must foster curiosity, comfort with data, willingness to experiment, and cross-functional collaboration.'
      },
      {
        q: 'What is the purpose of an "AI Center of Excellence" in an organization?',
        options: ['To replace the IT department', 'To centralize AI expertise, set standards, and support AI adoption across the organization', 'To build and sell AI products to external customers', 'To monitor employee performance using AI'],
        correct: 1,
        exp: 'An AI Center of Excellence (CoE) acts as a hub for AI expertise, best practices, tools, and governance — enabling the whole organization to benefit from AI capabilities while maintaining standards.'
      },
      {
        q: 'An organization that treats AI as a core strategic capability embedded in all products and decisions best represents which stage?',
        options: ['Level 1: AI Aware', 'Level 2: AI Active', 'Level 4: AI Systemic / Transformational', 'Level 3: AI Operational'],
        correct: 2,
        exp: 'At the Systemic/Transformational stage, AI is not just a tool for specific tasks — it\'s woven into the organization\'s DNA, driving competitive advantage, decision-making, and product development at scale.'
      }
    ]
  }
};

class Quiz {
  constructor(containerId, dataKey) {
    this.container = document.getElementById(containerId);
    this.data = quizData[dataKey];
    this.current = 0;
    this.score = 0;
    this.answered = false;
    this.render();
  }

  render() {
    if (!this.container || !this.data) return;
    const q = this.data.questions;
    const letters = ['A', 'B', 'C', 'D'];
    let html = `
      <div class="quiz-wrap">
        <div class="quiz-header">
          <h3><i class="fa-solid fa-circle-question"></i> ${this.data.title}</h3>
          <span class="quiz-progress-text" id="${this.container.id}-prog">Question 1 of ${q.length}</span>
        </div>`;

    q.forEach((item, qi) => {
      html += `<div class="question-block ${qi === 0 ? 'active' : ''}" id="${this.container.id}-q${qi}">
        <p class="question-text"><span class="question-number">Q${qi + 1}</span>${item.q}</p>`;
      item.options.forEach((opt, oi) => {
        html += `<button class="option-btn" data-quiz="${this.container.id}" data-q="${qi}" data-o="${oi}" onclick="quizzes['${this.container.id}'].answer(${qi},${oi})">
          <span class="option-letter">${letters[oi]}</span>${opt}
        </button>`;
      });
      html += `<div class="explanation" id="${this.container.id}-exp${qi}">💡 ${item.exp}</div></div>`;
    });

    html += `
      <div class="score-screen" id="${this.container.id}-score">
        <div class="score-circle" id="${this.container.id}-score-num">0/${q.length}</div>
        <h4 id="${this.container.id}-score-title">Quiz Complete!</h4>
        <p id="${this.container.id}-score-msg"></p>
        <button class="btn-primary" onclick="quizzes['${this.container.id}'].reset()">
          <i class="fa-solid fa-rotate-right"></i> Retake Quiz
        </button>
      </div>
      <div class="quiz-nav" id="${this.container.id}-nav">
        <button class="btn-secondary" id="${this.container.id}-prev" onclick="quizzes['${this.container.id}'].prev()" disabled>
          <i class="fa-solid fa-arrow-left"></i> Previous
        </button>
        <button class="btn-primary" id="${this.container.id}-next" onclick="quizzes['${this.container.id}'].next()" disabled>
          Next <i class="fa-solid fa-arrow-right"></i>
        </button>
      </div>
    </div>`;

    this.container.innerHTML = html;
    this.current = 0; this.score = 0; this.answered = false;
  }

  answer(qi, oi) {
    if (this.answered) return;
    this.answered = true;
    const q = this.data.questions[qi];
    const buttons = this.container.querySelectorAll(`[data-q="${qi}"]`);
    buttons.forEach((btn, i) => {
      btn.disabled = true;
      if (i === q.correct) btn.classList.add('correct');
      else if (i === oi) btn.classList.add('wrong');
    });
    const exp = document.getElementById(`${this.container.id}-exp${qi}`);
    if (exp) {
      exp.classList.add('show');
      if (oi !== q.correct) exp.classList.add('wrong-exp');
    }
    if (oi === q.correct) this.score++;
    const nextBtn = document.getElementById(`${this.container.id}-next`);
    if (nextBtn) nextBtn.disabled = false;
  }

  prev() {
    if (this.current <= 0) return;
    document.getElementById(`${this.container.id}-q${this.current}`).classList.remove('active');
    this.current--;
    document.getElementById(`${this.container.id}-q${this.current}`).classList.add('active');
    this.updateNav();
  }

  next() {
    const total = this.data.questions.length;
    document.getElementById(`${this.container.id}-q${this.current}`).classList.remove('active');
    if (this.current < total - 1) {
      this.current++;
      this.answered = false;
      document.getElementById(`${this.container.id}-q${this.current}`).classList.add('active');
      this.updateNav();
    } else {
      this.showScore();
    }
  }

  updateNav() {
    const total = this.data.questions.length;
    const prog = document.getElementById(`${this.container.id}-prog`);
    if (prog) prog.textContent = `Question ${this.current + 1} of ${total}`;
    const prevBtn = document.getElementById(`${this.container.id}-prev`);
    const nextBtn = document.getElementById(`${this.container.id}-next`);
    if (prevBtn) prevBtn.disabled = this.current === 0;
    if (nextBtn) nextBtn.disabled = !this.answered;
    // check if current question already answered
    const firstBtn = this.container.querySelector(`[data-q="${this.current}"]`);
    if (firstBtn && firstBtn.disabled) { this.answered = true; if (nextBtn) nextBtn.disabled = false; }
  }

  showScore() {
    const total = this.data.questions.length;
    const pct = Math.round((this.score / total) * 100);
    document.getElementById(`${this.container.id}-nav`).style.display = 'none';
    const scoreScreen = document.getElementById(`${this.container.id}-score`);
    scoreScreen.classList.add('show');
    document.getElementById(`${this.container.id}-score-num`).textContent = `${this.score}/${total}`;
    const titles = ['Keep Studying!', 'Good Start!', 'Well Done!', 'Excellent!', 'Perfect Score! 🎉'];
    const msgs = [
      'Review the section and try again — every expert started somewhere!',
      `You got ${this.score} right. Review the explanations and revisit the material.`,
      `Solid performance! You have a good grasp of the concepts.`,
      `Outstanding! You clearly understand this material well.`,
      `Flawless! You have mastered this section.`
    ];
    const idx = pct < 40 ? 0 : pct < 60 ? 1 : pct < 80 ? 2 : pct < 100 ? 3 : 4;
    document.getElementById(`${this.container.id}-score-title`).textContent = titles[idx];
    document.getElementById(`${this.container.id}-score-msg`).textContent = msgs[idx];
  }

  reset() {
    this.render();
  }
}

const quizzes = {};
function initQuizzes() {
  Object.keys(quizData).forEach(key => {
    const id = key + '-container';
    if (document.getElementById(id)) {
      quizzes[id] = new Quiz(id, key);
    }
  });
}

// ── Chat ────────────────────────────────────────────────────

const chatHistory = [];
let chatOpen = false;

function toggleChat() {
  chatOpen = !chatOpen;
  document.getElementById('chat-panel').classList.toggle('open', chatOpen);
  if (chatOpen && chatHistory.length === 0) {
    appendMessage('bot', "👋 Hi! I'm your AI tutor. Ask me anything about the concepts in this tutorial — I'll explain them in plain business language.");
  }
}

function closeChat() {
  chatOpen = false;
  document.getElementById('chat-panel').classList.remove('open');
}

function appendMessage(role, text) {
  const msgs = document.getElementById('chat-messages');
  const div = document.createElement('div');
  div.className = role === 'user' ? 'msg msg-user' : (role === 'error' ? 'msg msg-error' : 'msg msg-bot');
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return div;
}

function updateChatContext() {
  const sectionNames = {
    'section-0': 'Introduction to AI',
    'section-1': 'Introduction to AI',
    'section-2': 'Supervised Learning',
    'section-3': 'Unsupervised Learning',
    'section-4': 'Reinforcement Learning',
    'section-5': 'AI Ethics and Governance',
    'section-6': 'Organizational Readiness'
  };
  const ctx = sectionNames[currentSection] || 'AI for Managers';
  const ctxEl = document.getElementById('chat-context-label');
  if (ctxEl) ctxEl.textContent = 'Topic: ' + ctx;
}

async function sendChat() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;

  const mode  = sessionStorage.getItem('ai_mode')  || 'openai';
  const apiKey = sessionStorage.getItem('ai_key')  || '';
  const model = sessionStorage.getItem('ai_model') || 'gpt-4o-mini';

  if (mode !== 'demo' && !apiKey) {
    appendMessage('error', '⚠ No API key set. Please open ⚙ Settings to configure access.');
    openSettings();
    return;
  }

  appendMessage('user', msg);
  chatHistory.push({ role: 'user', content: msg });
  input.value = '';
  document.getElementById('chat-send-btn').disabled = true;

  const typing = appendMessage('bot', 'Thinking…');
  typing.classList.add('typing');

  const sectionNames = {
    'section-0': 'Introduction to AI',
    'section-1': 'Introduction to AI',
    'section-2': 'Supervised Learning',
    'section-3': 'Unsupervised Learning',
    'section-4': 'Reinforcement Learning',
    'section-5': 'AI Ethics and Governance',
    'section-6': 'Organizational Readiness'
  };

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode:    mode,
        api_key: apiKey,
        model:   model,
        message: msg,
        context: sectionNames[currentSection] || 'AI for Managers',
        history: chatHistory.slice(-6)
      })
    });
    const data = await res.json();
    typing.remove();
    if (data.error) {
      appendMessage('error', '⚠ ' + data.error);
    } else {
      appendMessage('bot', data.response);
      chatHistory.push({ role: 'assistant', content: data.response });
    }
  } catch (e) {
    typing.remove();
    appendMessage('error', '⚠ Network error. Make sure the server is running.');
  } finally {
    document.getElementById('chat-send-btn').disabled = false;
  }
}

// ── Settings ────────────────────────────────────────────────

function openSettings() {
  document.getElementById('settings-modal').classList.add('open');
  // Restore saved values
  const mode  = sessionStorage.getItem('ai_mode')  || 'openai';
  const key   = sessionStorage.getItem('ai_key')   || '';
  const model = sessionStorage.getItem('ai_model') || 'gpt-4o-mini';

  // Show/hide demo tab based on server capability
  const demoTab = document.getElementById('tab-demo');
  if (demoTab) demoTab.style.display = serverDemoAvailable ? '' : 'none';

  switchTab(mode === 'demo' && serverDemoAvailable ? 'demo' : mode);
  document.getElementById('settings-key').value = key;
  if (document.getElementById('settings-model')) {
    document.getElementById('settings-model').value = model;
  }
}

function switchTab(tab) {
  ['demo', 'openai', 'groq'].forEach(t => {
    const btn = document.getElementById('tab-' + t);
    const pane = document.getElementById('pane-' + t);
    if (btn)  btn.classList.toggle('tab-active', t === tab);
    if (pane) pane.style.display = (t === tab) ? '' : 'none';
  });
  sessionStorage.setItem('ai_mode', tab);
}

function closeSettings() {
  document.getElementById('settings-modal').classList.remove('open');
}

function selectTier(tier) {
  const freeEl = document.getElementById('tier-free');
  const paidEl = document.getElementById('tier-paid');
  const modelEl = document.getElementById('settings-model');
  if (freeEl) freeEl.style.borderColor = tier === 'free' ? 'var(--primary)' : 'transparent';
  if (paidEl) paidEl.style.borderColor = tier === 'paid' ? 'var(--secondary)' : 'transparent';
  if (modelEl) modelEl.value = tier === 'free' ? 'gpt-4o-mini' : 'gpt-4o';
}

function saveSettings() {
  const mode = sessionStorage.getItem('ai_mode') || 'openai';

  let key = '', model = 'gpt-4o-mini';

  if (mode === 'groq') {
    key = (document.getElementById('settings-groq-key').value || '').trim();
    model = 'llama3-8b-8192';
  } else if (mode === 'openai') {
    key   = (document.getElementById('settings-key').value || '').trim();
    model = document.getElementById('settings-model')
              ? document.getElementById('settings-model').value
              : 'gpt-4o-mini';
  }
  // demo mode: no key needed

  sessionStorage.setItem('ai_key',   key);
  sessionStorage.setItem('ai_model', model);
  closeSettings();

  const modeLabel = mode === 'demo' ? 'Demo (free)' : mode === 'groq' ? `Groq · ${model}` : `OpenAI · ${model}`;
  appendMessage('bot', `✅ Connected! Mode: ${modeLabel}. Ask me anything about what you're learning!`);
  if (!chatOpen) toggleChat();
}

// ── Keyboard & Init ─────────────────────────────────────────

document.addEventListener('DOMContentLoaded', async () => {
  showSection('section-1');
  initQuizzes();
  updateChatContext();

  // Check server capabilities (demo mode availability)
  try {
    const st = await fetch('/api/status').then(r => r.json());
    serverDemoAvailable = !!(st.demo_openai || st.demo_groq);
    if (serverDemoAvailable && !sessionStorage.getItem('ai_mode')) {
      sessionStorage.setItem('ai_mode', 'demo');
    }
  } catch (_) { /* server key check failed silently */ }

  document.getElementById('chat-input').addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
  });

  document.getElementById('settings-modal').addEventListener('click', function(e) {
    if (e.target === this) closeSettings();
  });
});
