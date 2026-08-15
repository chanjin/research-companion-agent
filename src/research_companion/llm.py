import ollama

# MODEL = "qwen3:8b"

MODEL = "gemma4:e4b"

def ask_llm(
    system_prompt: str,
    user_prompt: str,
) -> str:

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    return response[
        "message"
    ][
        "content"
    ].strip()