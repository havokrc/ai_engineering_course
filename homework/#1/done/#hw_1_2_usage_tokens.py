import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
llm_models = ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"]
# llm_models = ["claude-haiku-4-5"]

# Pricing in USD per million tokens (https://www.anthropic.com/pricing)
PRICING = {
    "claude-haiku-4-5":  {"input": 1.00, "output": 5.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-opus-4-7":   {"input": 5.00, "output": 25.00},
}

def get_token_usage(msg, llm_model):
    response = client.messages.create(
        model=llm_model,
        max_tokens=1024,
        messages=[{"role": "user", "content": msg}]
    )
    return {
        "response": response.content[0].text,
        "usage": {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
    }


eng_msg = """You are a weather data analyst. Calculate the average air temperature in Ukraine
over the last 7 days based on the following daily readings (°C):
Day 1: 18.2, Day 2: 19.5, Day 3: 17.8, Day 4: 20.1,
Day 5: 16.4, Day 6: 21.3, Day 7: 19.0.
Provide the average temperature."""
print(f"Msg: {eng_msg}\n")
for llm in llm_models:
    result = get_token_usage(eng_msg, llm)
    inp = result['usage']['input_tokens']
    out = result['usage']['output_tokens']
    price = PRICING[llm]
    cost_per_req = (inp * price['input'] + out * price['output']) / 1_000_000
    cost_per_1000 = cost_per_req * 1000
    monthly_cost = cost_per_1000 * 30

    print("=" * 50)
    print(f"Model: {llm}")
    print(f"\nUsage: input {inp} tokens, output {out} tokens; cost ${cost_per_1000:.4f} per 1000 requests")
    print(f"Conclusion: ${monthly_cost:.2f}/month at 1000 req/day")
    print("=" * 50)
