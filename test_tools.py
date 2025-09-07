import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔑 API Keys Check")
print("GROQ_API_KEY:", bool(os.environ.get("GROQ_API_KEY")))
print("SERPAPI_API_KEY:", bool(os.environ.get("SERPAPI_API_KEY")))
print("GEOAPIFY_API_KEY:", bool(os.environ.get("GEOAPIFY_API_KEY")))
print("GMAIL_USER:", bool(os.environ.get("GMAIL_USER")))
print("=" * 40)

# --- Import your Agent class ---
from agents.agent import Agent

# Initialize
agent = Agent()

# Test prompt
query = """Plan a trip from Hyderabad to Paris, 
depart October 10 2025 and return October 20 2025. 
Find flights, 3-4 star hotels near the Eiffel Tower, and must-see attractions."""

print("🧪 Running Agent with query:", query)
try:
    response = agent.run(query)
    print("\n✅ Agent Response:\n", response)
except Exception as e:
    print("\n❌ Agent Error:", str(e))
