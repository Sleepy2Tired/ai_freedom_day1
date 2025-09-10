from pathlib import Path
from dotenv import dotenv_values
from openai import OpenAI
from datetime import datetime

# Load API key from .env
ENV_PATH = Path(__file__).parent / ".env"
api_key = dotenv_values(dotenv_path=str(ENV_PATH)).get("OPENAI_API_KEY", "").strip()
assert api_key.startswith("sk-"), "OPENAI_API_KEY missing/invalid in .env"

client = OpenAI(api_key=api_key)

def motivate(prompt: str):
    """Generate motivation + 3 action steps."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a motivator + productivity coach. Keep it short, punchy, and practical."},
            {"role": "user", "content": f"Motivate me and give me 3 action steps for: {prompt}"}
        ],
        temperature=0.8,
        max_tokens=200
    )
    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    logs_path = Path(__file__).parent / "daily_log.txt"
    print("\n📓 Daily Journal & Motivation Logger")
    while True:
        user_input = input("\n📝 What’s on your mind? (or 'exit' to quit): ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("👊 Session ended. Keep pushing forward.")
            break

        result = motivate(user_input)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"\n[{timestamp}] INPUT: {user_input}\n{result}\n"
        with open(logs_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

        print("\n⚡ Your motivation:\n", result)
        print(f"\n✅ Saved to {logs_path}")
