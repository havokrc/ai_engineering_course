import anthropic
import time
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
PROMPT = (
    "Design a folder structure and pyproject.toml for a Python/pytest/playwright "
    "AQA framework based on POM pattern. Include: browser context, API client, "
    "DB client, test folders for API, UI and e2e tests with conftest files. "
    "No code implementation needed, structure and config only."
)


def run_request(client, run_num, model, thinking_config, effort=None):
    params = {
        "model": model,
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": PROMPT}],
        "thinking": thinking_config,
    }

    if effort is not None:
        params["output_config"] = {"effort": effort}

    start = time.perf_counter()
    response = client.messages.create(**params)
    elapsed = time.perf_counter() - start

    print(f"Run {run_num}:")
    print(f"- Model: {response.model}")
    print(f"- Thinking: {thinking_config.get('type')}")
    print(f"- Time: {elapsed:.2f}s")
    print(f"- Input: {response.usage.input_tokens} tokens")
    print(f"- Output: {response.usage.output_tokens} tokens")
    print()

    thinking_type = thinking_config.get("type", "disabled")
    effort_part = f"_{effort}" if effort is not None else ""
    timestamp = datetime.now().strftime("%H:%M:%S")
    filename = f"{model}_{thinking_type}{effort_part}_{timestamp}.txt"

    text_content = "\n\n".join(
        block.text for block in response.content if block.type == "text"
    )
    with open(filename, "w") as f:
        f.write(text_content)


def main():
    client = anthropic.Anthropic()

    print("hw_1_12")
    print(f"PROMPT: {PROMPT}\n")
    run_request(
        client,
        run_num=1,
        model="claude-sonnet-4-5-20250929",
        thinking_config={"type": "disabled"},
    )

    run_request(
        client,
        run_num=2,
        model="claude-sonnet-4-6",
        thinking_config={"type": "adaptive"},
        effort="medium",
    )


if __name__ == "__main__":
    main()
