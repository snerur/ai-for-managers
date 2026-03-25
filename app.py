"""
AI for Managers – Interactive Tutorial
Created by Sridhar Nerur · Built with Claude (Anthropic)

Run:
  pip install -r requirements.txt
  python app.py
Then open http://localhost:5000 in your browser.

Optional — server-side demo key (so visitors need no API key):
  Copy .env.example → .env and fill in OPENAI_API_KEY or GROQ_API_KEY.
"""

import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Server-side keys (optional — enables demo/free mode for visitors) ──
_SERVER_OPENAI_KEY = os.getenv("OPENAI_API_KEY", "").strip()
_SERVER_GROQ_KEY   = os.getenv("GROQ_API_KEY",   "").strip()

GROQ_BASE_URL   = "https://api.groq.com/openai/v1"
GROQ_FREE_MODEL = "llama-3.1-8b-instant"   # current Groq free-tier fast model


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/status")
def status():
    """Tells the frontend which access modes are available."""
    return jsonify({
        "demo_openai": bool(_SERVER_OPENAI_KEY),
        "demo_groq":   bool(_SERVER_GROQ_KEY),
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data     = request.get_json(force=True)
        mode     = data.get("mode", "openai")          # "openai" | "groq" | "demo"
        user_key = (data.get("api_key") or "").strip()
        message  = (data.get("message") or "").strip()
        model    = data.get("model", "gpt-4o-mini")
        context  = data.get("context", "Introduction to AI")
        history  = data.get("history", [])

        if not message:
            return jsonify({"error": "Message cannot be empty."}), 400

        # ── Resolve which API key + base URL to use ──────────────────────
        if mode == "demo":
            # Use server-side key; pick provider based on what's configured
            if _SERVER_OPENAI_KEY:
                api_key  = _SERVER_OPENAI_KEY
                base_url = None
                model    = "gpt-4o-mini"
            elif _SERVER_GROQ_KEY:
                api_key  = _SERVER_GROQ_KEY
                base_url = GROQ_BASE_URL
                model    = GROQ_FREE_MODEL
            else:
                return jsonify({
                    "error": "Demo mode is not configured on this server. "
                             "Please enter your own API key in ⚙ Settings."
                }), 503

        elif mode == "groq":
            if not user_key:
                return jsonify({
                    "error": "Please enter your Groq API key in ⚙ Settings. "
                             "Get a free key at console.groq.com (no payment needed)."
                }), 400
            api_key  = user_key
            base_url = GROQ_BASE_URL
            model    = GROQ_FREE_MODEL

        else:  # openai (free tier or paid)
            if not user_key:
                return jsonify({
                    "error": "Please enter your OpenAI API key in ⚙ Settings."
                }), 400
            api_key  = user_key
            base_url = None
            # model already set from request

        # ── Build client ──────────────────────────────────────────────────
        client = OpenAI(api_key=api_key, base_url=base_url) if base_url \
                 else OpenAI(api_key=api_key)

        system_prompt = (
            "You are an expert AI tutor helping non-technical managers understand AI concepts.\n"
            f"The learner is currently studying: **{context}**.\n\n"
            "Guidelines:\n"
            "• Use plain, business-friendly language — avoid jargon unless you explain it.\n"
            "• Anchor explanations to real-world business examples managers can relate to.\n"
            "• Be concise: 2–4 short paragraphs unless more detail is truly needed.\n"
            "• Be encouraging, positive, and supportive.\n"
            "• When relevant, connect ideas back to practical business value."
        )

        messages = [{"role": "system", "content": system_prompt}]
        for turn in history[-6:]:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=700,
            temperature=0.7,
        )

        return jsonify({
            "response": response.choices[0].message.content,
            "model_used": model,
        })

    except Exception as exc:
        msg = str(exc)
        if "auth" in msg.lower() or "api_key" in msg.lower() or "invalid" in msg.lower():
            return jsonify({"error": "Invalid API key. Please check your key in ⚙ Settings."}), 401
        if "quota" in msg.lower() or "billing" in msg.lower() or "rate" in msg.lower():
            return jsonify({"error": "API quota or rate limit reached. Try again shortly, or switch to a different access mode."}), 429
        return jsonify({"error": f"Unexpected error: {msg}"}), 500


if __name__ == "__main__":
    demo_note = ""
    if _SERVER_OPENAI_KEY:
        demo_note = "  Demo mode: ON  (server OpenAI key loaded)"
    elif _SERVER_GROQ_KEY:
        demo_note = "  Demo mode: ON  (server Groq key loaded)"
    else:
        demo_note = "  Demo mode: OFF (set OPENAI_API_KEY or GROQ_API_KEY in .env to enable)"

    print("\n" + "=" * 55)
    print("  AI for Managers — Interactive Tutorial")
    print("  Created by Sridhar Nerur · Built with Claude")
    print("=" * 55)
    print("  Open http://localhost:5000 in your browser")
    print(demo_note)
    print("  Press Ctrl+C to stop")
    print("=" * 55 + "\n")
    app.run(debug=False, port=5000)
