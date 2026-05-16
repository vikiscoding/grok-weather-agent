import os
from dotenv import load_dotenv
from xai_sdk import Client
from xai_sdk.chat import user, system

# ====================== LOAD SECURE API KEY ======================
load_dotenv()                    # Loads .env file
api_key = os.getenv("XAI_API_KEY")

if not api_key:
    print("❌ ERROR: No XAI_API_KEY found!")
    print("   Please check your .env file")
    exit(1)

print("✅ API key loaded successfully from .env")

# ====================== CREATE YOUR AGENT ======================
client = Client(api_key=api_key)

chat = client.chat.create(model="grok-4")

chat.append(system(
    "You are a friendly, concise Python teacher. "
    "Help the user learn by building small agents step-by-step."
))

print("🚀 Grok Agent is ready! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! 👋")
        break
    
    chat.append(user(user_input))
    response = chat.sample()          # ← This was the fix
    
    print(f"Grok: {response.content}\n")
    
    # Important: Add the response back to maintain conversation memory
    chat.append(response)