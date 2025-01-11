import aiohttp
from typing import List, Dict, Any

JEJU_OPENAI_URL = "https://open-api.jejucodingcamp.workers.dev/"


async def generate_quiz_feedback(
    quiz_title: str,
    quiz_content: str,
    selected_content: str,
    correct_content: str = None,
    is_correct: bool = False,
    quiz_type: str = None,
) -> str:
    """
    퀴즈 응답에 대한 AI 피드백을 생성합니다.
    """
    if quiz_type == "MULTIPLE_CHOICE":
        if is_correct:
            user_content = f"""
            다음은 프로그래밍 퀴즈와 사용자의 정답 선택입니다:

            문제: {quiz_title}
            문제 내용: {quiz_content}
            사용자의 선택: {selected_content}

            사용자가 정답을 선택했습니다. 다음 내용을 포함하여 상세한 설명을 제공해주세요:
            1. 왜 이 답이 정답인지에 대한 설명
            2. 이 개념의 실제 활용 사례
            3. 관련된 추가 학습 포인트
            """
        else:
            user_content = f"""
            다음은 프로그래밍 퀴즈와 사용자의 오답 선택입니다:

            문제: {quiz_title}
            문제 내용: {quiz_content}
            사용자의 선택: {selected_content}
            정답: {correct_content}

            사용자가 오답을 선택했습니다. 다음 내용을 포함하여 상세한 설명을 제공해주세요:
            1. 왜 사용자의 선택이 잘못되었는지 설명
            2. 정답에 대한 상세한 설명
            3. 이러한 실수를 피하는 방법
            4. 관련 개념에 대한 추가 학습 포인트
            """
    elif quiz_type == "CODING":
        user_content = f"""
        다음은 코딩 테스트 문제와 사용자의 답안입니다:

        문제: {quiz_title}
        문제 내용: {quiz_content}
        사용자의 코드:
        ```
        {selected_content}
        ```

        다음 내용을 포함하여 상세한 피드백을 제공해주세요:
        1. 코드의 정확성 평가
        2. 코드 스타일과 가독성 분석
        3. 성능 관점에서의 개선점
        4. 더 나은 해결 방법 제안
        5. 관련된 추가 학습 포인트
        """
    else:  # TEXT type
        user_content = f"""
        다음은 면접 질문과 사용자의 답변입니다:

        질문: {quiz_title}
        질문 내용: {quiz_content}
        사용자의 답변:
        {selected_content}

        다음 내용을 포함하여 상세한 피드백을 제공해주세요:
        1. 답변의 완성도와 정확성
        2. 핵심 개념의 이해도
        3. 답변 구조와 논리성
        4. 개선이 필요한 부분
        5. 추가로 언급하면 좋을 내용
        6. 실제 면접에서의 대답 요령
        """

    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": "당신은 프로그래밍 교육 전문가입니다. 학습자의 이해를 돕기 위해 명확하고 친절한 설명을 제공해주세요.",
        },
        {"role": "user", "content": user_content},
    ]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(JEJU_OPENAI_URL, json=messages) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_detail = await response.text()
                    print(
                        f"API Error: Status {response.status}, Detail: {error_detail}"
                    )
                    return "죄송합니다. 피드백을 생성하는 중 오류가 발생했습니다."

    except Exception as e:
        print(f"Error generating feedback: {str(e)}")
        return "죄송합니다. 피드백을 생성하는 중 오류가 발생했습니다."
