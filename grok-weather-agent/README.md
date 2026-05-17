# 🚀 A Multi-Tool Agent using Grok

A live, interactive agent powered by **xAI Grok-4** with real tool calling.

**Live Demo**: [https://svikgrokweatheragent.streamlit.app](https://svikgrokweatheragent.streamlit.app)

## ✨ Features

- **5 Real Tools**:
  - Weather (any city)
  - Calculator (math expressions)
  - Current Time (city-aware: New Delhi, Toronto, London, etc.)
  - Web Search (DuckDuckGo)
  - Wikipedia Summary
- Session limit (10 messages) to control API costs
- Clean conversation memory
- Built with xAI SDK + Streamlit

## 🎮 Try These Prompts

- "What's the weather in New Delhi?"
- "What is 234 * 17 + 89?"
- "What time is it right now in New Delhi?"
- "Latest news about xAI"
- "Wikipedia summary of Agentic AI"

## 🛠️ Tech Stack

- **xAI Grok-4** + Tool Calling
- **Streamlit** (frontend + deployment)
- Python 3.14 + Virtual Environment
- Secure API key handling

## 🚀 How to Run Locally

```bash
git clone https://github.com/vikiscoding/grok-weather-agent.git
cd grok-weather-agent

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Add your key
echo "XAI_API_KEY=your_key_here" > .env

streamlit run app.py