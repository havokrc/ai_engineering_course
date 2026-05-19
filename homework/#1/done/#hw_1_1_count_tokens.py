import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
llm_models = ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"]

def count_tokens(msg, llm_model):
    response = client.messages.count_tokens(
        model=llm_model,
        messages=[{"role": "user", "content": msg}]
    )
    return response.input_tokens


eng_msg = "Automated testing helps teams catch bugs early in the development cycle. Writing clear and maintainable test cases reduces the cost of fixing defects. A good test suite gives developers confidence to refactor code without breaking existing functionality."
ukr_msg = "Автоматизоване тестування допомагає командам виявляти баги на ранніх етапах розробки. Написання чітких та підтримуваних тест-кейсів знижує вартість виправлення дефектів. Хороший набір тестів дає розробникам впевненість рефакторити код без поломки існуючої функціональності."
print(f"Eng msg: {eng_msg}")
print(f"Ukr msg: {ukr_msg}")
for llm in llm_models:
    used_tokens_eng = count_tokens(eng_msg, llm)
    used_tokens_ukr = count_tokens(ukr_msg, llm)
    token_ratio = used_tokens_ukr / used_tokens_eng if used_tokens_eng > 0 else float('inf')
    print("-" * 50)
    print(f"LLM model: {llm}")
    print(f"English msg == {used_tokens_eng} tokens")
    print(f"Ukrainian msg == {used_tokens_ukr} tokens")
    print("-"*5)
    print(f"Token ratio ({llm}): x%.2f\n" % token_ratio)

