import streamlit as st
import os
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system, tool, tool_result, assistant

load_dotenv()
api_key = os.getenv("XAI_API_KEY")

st.title("🚀 Multi-Tool Agent by Vikrant")
st.caption("Weather • Calculator • Search • Wikipedia • Time (City-aware)")

# ====================== USAGE LIMIT (Protects your API budget) ======================
MAX_MESSAGES_PER_SESSION = 10

if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# Display usage clearly
st.info(f"**Usage Limit**: {st.session_state.message_count} / {MAX_MESSAGES_PER_SESSION} messages per session\n"
        "→ Refresh the page to start a new session.")

if st.session_state.message_count >= MAX_MESSAGES_PER_SESSION:
    st.error("🚫 You have reached the maximum number of messages for this session.\n\n"
             "Please refresh the page to start a new session.")
    st.stop()

if not api_key:
    st.error("❌ Missing XAI_API_KEY in .env or Streamlit Secrets")
    st.stop()

# ====================== 5 POWERFUL TOOLS ======================
def get_weather(city: str) -> str:
    """Get current temperature for any city/location."""
    import requests
    try:
        geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1").json()
        if not geo.get("results"):
            return f"❌ City not found: {city}"
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        name = geo["results"][0]["name"]
        data = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m").json()["current"]
        return f"**{name}**: {data['temperature_2m']}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


def calculator(expression: str) -> str:
    """Safely evaluate simple math expressions."""
    try:
        allowed = {"__builtins__": {}}
        result = eval(expression, allowed, {})
        return f"**Result**: {result}"
    except Exception as e:
        return f"❌ Invalid math: {str(e)}"


def get_current_time(city: str = None) -> str:
    """Get current date and time for a specific city."""
    city_to_tz = {
        "new delhi": "Asia/Kolkata", "delhi": "Asia/Kolkata", "mumbai": "Asia/Kolkata",
        "toronto": "America/Toronto", "new york": "America/New_York", "london": "Europe/London",
        "paris": "Europe/Paris", "tokyo": "Asia/Tokyo", "sydney": "Australia/Sydney",
    }
    if not city:
        now = datetime.now()
        return f"**Current Time (Local)**: {now.strftime('%I:%M %p')} • {now.strftime('%B %d, %Y')}"
    
    tz_name = city_to_tz.get(city.lower())
    if not tz_name:
        return f"❌ Timezone not available for '{city}'. Try: New Delhi, London, New York, Tokyo."
    try:
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
        return f"**Current Time in {city.title()}**: {now.strftime('%I:%M %p')} • {now.strftime('%B %d, %Y')}"
    except Exception:
        return f"Error getting time for {city}."


def web_search(query: str) -> str:
    """Search the internet using DuckDuckGo."""
    import requests
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        data = requests.get(url, timeout=8).json()
        return data.get("AbstractText") or data.get("Definition", "No clear answer found.")
    except Exception:
        return "Search failed. Try again later."


def wikipedia_summary(topic: str) -> str:
    """Get a short Wikipedia summary for any topic."""
    import requests
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.replace(' ', '_')}"
        data = requests.get(url).json()
        return data.get("extract", "No summary found.")
    except Exception:
        return "Could not fetch Wikipedia summary."


# Tool definitions
tools = [
    tool(name="get_weather", description="Get current temperature for any city or location.", parameters={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}),
    tool(name="calculator", description="Evaluate simple math expressions (e.g. 234*17 + 89)", parameters={"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}),
    tool(name="get_current_time", description="Get current date and time for a specific city (e.g. New Delhi, London, New York, Tokyo).", parameters={"type": "object", "properties": {"city": {"type": "string"}}, "required": []}),
    tool(name="web_search", description="Search the internet for up-to-date information", parameters={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
    tool(name="wikipedia_summary", description="Get a short Wikipedia summary about any topic", parameters={"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}),
]

# ====================== CHAT INTERFACE ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Increment message count
    st.session_state.message_count += 1

    with st.chat_message("assistant"):
        with st.spinner("Grok is thinking..."):
            client = Client(api_key=api_key)
            chat = client.chat.create(model="grok-4", tools=tools)

            chat.append(system(
                "You are a helpful, concise, and fun assistant. "
                "Use the available tools when needed. Be accurate and friendly."
            ))

            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat.append(user(msg["content"]))
                elif msg["role"] == "assistant":
                    chat.append(assistant(msg["content"]))

            response = chat.sample()

            if response.tool_calls:
                chat.append(response)
                for tc in response.tool_calls:
                    name = tc.function.name
                    args = json.loads(tc.function.arguments)

                    if name == "get_weather":
                        result = get_weather(args.get("city", ""))
                    elif name == "calculator":
                        result = calculator(args.get("expression", ""))
                    elif name == "get_current_time":
                        result = get_current_time(args.get("city"))
                    elif name == "web_search":
                        result = web_search(args.get("query", ""))
                    elif name == "wikipedia_summary":
                        result = wikipedia_summary(args.get("topic", ""))
                    else:
                        result = "Tool not implemented yet."

                    chat.append(tool_result(result))

                response = chat.sample()

            answer = response.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})