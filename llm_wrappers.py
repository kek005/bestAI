import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Optional: if you're using a .env file
client = OpenAI(api_key=os.getenv("OPENAI_DUEL_KEY"))

def get_response_openai(prompt, model="gpt-4o-mini"):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        raw_response = completion.choices[0].message.content
        print(f"\n🧠 Raw LLM Response:\n{raw_response}")
        return raw_response.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"