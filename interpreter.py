import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Load fallback logic
from rule_based_interpreter import interpret_block as fallback_interpret_block

try:
    if api_key:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        def interpret_block(block_lines):
            """
            Attempts to interpret log lines using GPT. Falls back to rule-based logic on any error.
            """
            import json
            import time

            try:
                block_text = "\n".join(block_lines)

                prompt = f"""
You are a QA engineer analyzing log files from a software system.
For each log line below, determine:
1. Whether the line indicates normal or abnormal behavior.
2. If abnormal, explain what might be the problem.
3. Respond in strict JSON format like this:
[
  {{
    "timestamp": "...",
    "level": "...",
    "message": "...",
    "interpretation": "...",
    "critical": true/false
  }},
  ...
]

Log block:
{block_text}
                """

                # Make the API call
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a QA log analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )

                # Check if a valid response was returned
                if not response or not response.choices:
                    raise ValueError("Empty response from GPT")

                reply = response.choices[0].message.content

                # Try to parse JSON from reply
                try:
                    parsed = json.loads(reply)
                    return parsed
                except json.JSONDecodeError as je:
                    print("⚠️ Failed to parse GPT response. Using fallback.")
                    print("   Response content was:", reply)
                    return fallback_interpret_block(block_lines)

            except Exception as e:
                print("⚠️ GPT completely failed. Using rule-based fallback.")
                print("   Reason:", str(e))
                return fallback_interpret_block(block_lines)

            finally:
                time.sleep(1.0)

    else:
        # No API key = use fallback only
        def interpret_block(block_lines):
            print("⚠️ No API key found. Using rule-based interpreter.")
            return fallback_interpret_block(block_lines)

except Exception as import_error:
    def interpret_block(block_lines):
        print("⚠️ Failed to initialize GPT. Using rule-based interpreter.")
        print("   Reason:", str(import_error))
        return fallback_interpret_block(block_lines)

