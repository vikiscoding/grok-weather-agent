import streamlit as st
import os
import json
from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system, tool, tool_result

load_dotenv()
api_key = os.getenv("XAI_API_KEY")

st.title("🚀 Grok Agent with Tools")
st.caption("Weather tool powered by xAI SDK | Built while learning")

if not api_key:
    st.error("❌ Missing XAI_API_KEY in .env")
    st.stop()

# ====================== WEATHER TOOL ======================
def get_weather(city: str) -> str:
    """Get current temperature using free Open-Meteo API"""
    import requests
    try:
        # Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo = requests.get(geo_url).json()
        if not geo.get("results"):
            return f"❌ Could not find location: {city}"
        
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        name = geo["results"][0]["name"]

        # Get weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code"
        data = requests.get(weather_url).json()["current"]
        
        return f"**{name}**: {data['temperature_2m']}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

# Define tool for Grok (correct xAI SDK format)
tools = [
    tool(
        name="get_weather",
        description="Get current temperature for any city or location.",
        parameters={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. Toronto, New York, London"
                }
            },
            "required": ["city"]
        },
    )
]

# ====================== STREAMLIT CHAT ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything (try 'weather in Toronto')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Grok is thinking..."):
            client = Client(api_key=api_key)
            chat = client.chat.create(model="grok-4", tools=tools)

            chat.append(system(
                "You are a helpful assistant. Use the get_weather tool when the user asks about weather."
            ))

            # Add history
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    chat.append(user(msg["content"]))
                elif msg["role"] == "assistant":
                    chat.append(msg["content"])

            response = chat.sample()

            # Handle tool calls
            if response.tool_calls:
                chat.append(response)
                for tc in response.tool_calls:
                    if tc.function.name == "get_weather":
                        args = json.loads(tc.function.arguments)
                        result = get_weather(args["city"])
                        chat.append(tool_result(result))
                
                # Get final answer
                response = chat.sample()

            answer = response.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})