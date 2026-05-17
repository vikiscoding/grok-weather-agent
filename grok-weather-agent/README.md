# 🚀 A Multi-Tool Agent using Grok

A live, interactive agent powered by **xAI Grok-4** with real tool calling.

**Live Demo**: https://svikweatheragent.streamlit.app/ 

---

### ✨ Features
- **Weather** → Current temperature for any city
- **Calculator** → Safe math expressions
- **City-aware Time** → Local time in major cities
- **Web Search** → Real-time DuckDuckGo results
- **Wikipedia Summary** → Quick topic summaries

### Screenshots

![Demo 1]!  
*[(Weather + Calculator in action* !!!)](streamlit_demo1.png)

![Demo 2]  

![*Time + Search example* !](streamlit_demo2.png)
*(Add 2–3 screenshots here — see instructions below)*

### Tech Stack
- **Frontend**: Streamlit
- **LLM**: Grok-4 (xAI)
- **Tools**: Custom Python functions + xAI SDK
- **Deployment**: Streamlit Cloud

### How to Run Locally

```bash
git clone https://github.com/vikiscoding/grok-weather-agent.git
cd grok-weather-agent
pip install -r requirements.txt
cp .env.example .env          # Add your XAI_API_KEY
streamlit run app.py
Usage Limit
10 messages per session (protects API budget). Refresh page to reset.


git clone https://github.com/vikiscoding/grok-weather-agent.git
cd grok-weather-agent

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

# Add your key
echo "XAI_API_KEY=your_key_here" > .env

streamlit run app.py

Want to Contribute?
Feel free to open issues or PRs!
Made with ❤️ by Vikrant