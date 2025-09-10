from pathlib import Path
from dotenv import dotenv_values
from openai import OpenAI

# Load API key from .env
ENV_PATH = Path(__file__).parent / ".env"
api_key = dotenv_values(dotenv_path=str(ENV_PATH)).get("OPENAI_API_KEY", "").strip()
assert api_key.startswith("sk-"), "OPENAI_API_KEY missing/invalid in .env"

client = OpenAI(api_key=api_key)

def motivate(prompt: str):
    """Send a custom motivational request to the AI and return response."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a powerful motivator. Be short, punchy, and inspiring."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=120
    )
    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input("\n🔥 Enter a situation you need motivation for (or type 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👊 Stay strong. Session ended.")
            break
        print("\n⚡ Your motivation:\n", motivate(user_input))
