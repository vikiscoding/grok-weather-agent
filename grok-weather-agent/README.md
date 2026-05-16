# 🚀 Grok Agent with Tools

A live interactive agent powered by **xAI Grok** + **Streamlit** with real tool calling.

![Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-brightgreen)

## ✨ Features

- Real-time chat with Grok-4
- **Weather Tool** (fetches live temperature using Open-Meteo API)
- Tool calling capability (can be extended easily)
- Clean, responsive web interface
- Secure API key handling

## 🛠️ Tech Stack

- **xAI SDK** (`grok-4`)
- **Streamlit** (frontend)
- Python 3.14 + Virtual Environment
- Tool calling with function execution

## 🎮 Try It Live

👉 **[Open the Live Agent](https://svikgrokweatheragent.streamlit.app)**

Try asking:
- "What's the weather in Toronto?"
- "Weather in West Rouge"
- "Compare Toronto and Vancouver weather"

## 📸 Screenshots

*(Add screenshots here later)*

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/vikiscoding/grok-agent-weather.git
cd grok-agent-weather

# 2. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your key
echo "XAI_API_KEY=xai-your-key-here" > .env

# 5. Run
streamlit run app.py