from llm import ask_llm


def main():
    #prompt = "연구 질문이란 무엇인지 간단히 설명해줘."
    prompt = """
나는 AI Agent에 관한 연구를 시작하려고 한다.

이 연구 주제를 탐색하기 위해 고려할 수 있는
연구 질문 3개를 제안해줘.
"""

    response = ask_llm(prompt)

    print(response)


if __name__ == "__main__":
    main()