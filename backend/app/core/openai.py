import os
import logging
import aiohttp
from typing import List, Dict, Any, Optional
from enum import Enum
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_URL = os.getenv(
    "OPENAI_API_URL", "https://open-api.jejucodingcamp.workers.dev/"
)
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "30"))  # seconds

# Prompts
MULTIPLE_CHOICE_CORRECT_PROMPT = """
다음은 프로그래밍 학습자가 푼 객관식 퀴즈입니다:

문제: {quiz_title}
문제 설명: {quiz_content}
정답 선택: {selected_content}

아래의 정보를 포함하여 상세 피드백을 제공하세요:
1. **왜 정답이 맞는지** 명확한 설명
2. 이 개념이 실제 프로그래밍에서 사용되는 사례 1~2개
3. 관련 주제에 대해 추가 학습할 만한 심화 내용
4. 유사한 개념이나 예제를 통한 확장 학습 제안
"""

MULTIPLE_CHOICE_INCORRECT_PROMPT = """
다음은 프로그래밍 학습자가 푼 객관식 퀴즈입니다:

문제: {quiz_title}
문제 설명: {quiz_content}
사용자가 선택한 답변: {selected_content}
정답: {correct_content}

아래의 정보를 포함하여 상세 피드백을 제공하세요:
1. **왜 사용자의 선택이 틀렸는지** 설명
2. **이와 같은 실수를 피하는 전략**
3. 관련된 개념의 확장 학습 제안
4. 유사한 문제를 제공하여 개념을 재확인할 수 있는 연습 기회 제안
"""

CODING_PROMPT = """
다음은 코딩 테스트 문제와 학습자가 작성한 코드입니다:

문제: {quiz_title}
문제 설명: {quiz_content}
작성한 코드: {selected_content}

아래의 정보를 포함하여 상세 피드백을 제공하세요:
1. **코드의 정확성 평가** (의도한 문제를 정확히 해결했는가?)
2. **코드 스타일과 가독성** (더 명확하거나 간결하게 작성할 수 있는지)
3. **성능 개선점** (시간/공간 복잡도 관점에서)
4. **다양한 접근 방식 제안** (더 나은 해결 방법이나 대안)
5. 학습자가 이해할 수 있는 **심화 학습 주제**와 추가 연습 과제
"""

TEXT_PROMPT = """
다음은 개발자 면접 준비를 위해 학습자가 작성한 답변입니다:

질문: {quiz_title}
질문 설명: {quiz_content}
작성한 답변:
{selected_content}

아래의 정보를 포함하여 상세 피드백을 제공하세요:
1. **답변의 완성도**와 내용의 정확성
2. **핵심 개념에 대한 이해도** 평가
3. **답변 구조와 논리성** (좀 더 명확하게 설명하거나 개선할 방법)
4. 부족한 부분 및 **추가로 언급하면 좋은 내용**
5. 면접 상황에서 **실제 활용 가능한 대답 요령**과 팁
6. 관련 개념을 확장 학습할 수 있는 자료나 주제
"""

SYSTEM_PROMPT = """
당신은 프로그래밍 교육 전문가이자 멘토입니다. 프로그래밍 학습 초보자와 주니어 개발자가 스스로 성장할 수 있도록 명확하고 체계적인 피드백과 친절한 설명을 제공합니다. 

다음과 같은 가이드를 따라 학습자의 이해를 돕고 실력을 향상시킬 수 있도록 지원하세요:

1. **명확하고 구체적인 설명 제공:**  
   - 학습자가 쉽게 이해할 수 있도록 용어를 명확히 정의하고, 복잡한 개념은 간단한 예제로 설명합니다.  
   - 응답 시 **마크다운 형식을 활용**하여 피드백을 구조화하며, 코드블록과 표, 불릿 포인트 등을 적극적으로 사용합니다.

2. **실제 활용 사례 강조:**  
   - 학습자가 배운 개념을 실무에서 어떻게 사용할 수 있는지 구체적인 예제를 들어 설명합니다.  
   - 코드 활용 시 **코드블록(```code```)**을 사용하여 학습자가 복사/실행할 수 있도록 합니다.

3. **추가 학습 방향 제안:**  
   - 현재 학습 수준을 고려하여 연관된 주제나 심화 학습 자료를 추천합니다.  
   - 학습자를 위한 연습 문제 또는 심화 학습 자료를 **목록 형태로 제공**하여 선택지를 넓힙니다.

4. **구조적이고 논리적인 피드백:**  
   - 피드백의 각 항목은 논리적 순서에 따라 명확히 구분되며, **불릿 포인트**로 정리해 학습자가 읽기 쉽게 작성합니다.  
   - 표를 사용하여 장단점 비교, 개념 요약 등을 시각적으로 제공합니다.

5. **학습 동기 부여:**  
   - 피드백에 긍정적인 메시지를 포함하여 학습자가 자신감을 잃지 않고 지속적으로 학습할 수 있도록 격려합니다.  
   - 학습자의 강점을 언급하며, 개선이 필요한 부분에 대한 구체적인 가이드를 제안합니다.

### 추가 요구 사항
- 모든 응답은 **마크다운 형식**으로 작성되어야 하며, 코드 예제를 포함할 경우 **코드블록**(````)을 사용하세요.  
- 복잡한 개념이나 구조를 설명할 때는 **표** 또는 **불릿 포인트**를 활용하여 학습자가 시각적으로 이해하기 쉽게 만드세요.  
- 항상 학습자의 수준과 배경을 고려하며, 학습자 중심의 접근 방식을 유지합니다.  
- 최우선 목표는 학습자가 자신감을 가지고 실력을 향상시킬 수 있도록 돕는 것입니다.
"""


class QuizType(str, Enum):
    """퀴즈 타입을 정의하는 열거형 클래스"""

    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    CODING = "CODING"
    TEXT = "TEXT"


class OpenAIError(Exception):
    """OpenAI API 관련 에러를 처리하기 위한 커스텀 예외 클래스"""

    pass


def create_feedback_prompt(
    quiz_type: QuizType,
    quiz_title: str,
    quiz_content: str,
    selected_content: str,
    correct_content: Optional[str] = None,
    is_correct: bool = False,
) -> str:
    """
    퀴즈 타입과 사용자의 답변에 따라 적절한 프롬프트를 생성합니다.

    Args:
        quiz_type: 퀴즈 타입 (객관식, 코딩, 텍스트)
        quiz_title: 퀴즈 제목
        quiz_content: 퀴즈 내용
        selected_content: 사용자가 선택한 답변
        correct_content: 정답 (객관식인 경우)
        is_correct: 정답 여부 (객관식인 경우)

    Returns:
        str: OpenAI에 전달할 프롬프트
    """
    format_args = {
        "quiz_title": quiz_title,
        "quiz_content": quiz_content,
        "selected_content": selected_content,
        "correct_content": correct_content,
    }

    if quiz_type == QuizType.MULTIPLE_CHOICE:
        template = (
            MULTIPLE_CHOICE_CORRECT_PROMPT
            if is_correct
            else MULTIPLE_CHOICE_INCORRECT_PROMPT
        )
    elif quiz_type == QuizType.CODING:
        template = CODING_PROMPT
    else:  # TEXT
        template = TEXT_PROMPT

    return template.format(**format_args)


async def generate_quiz_feedback(
    quiz_title: str,
    quiz_content: str,
    selected_content: str,
    correct_content: Optional[str] = None,
    is_correct: bool = False,
    quiz_type: str = None,
) -> str:
    """
    퀴즈 응답에 대한 AI 피드백을 생성합니다.

    Args:
        quiz_title: 퀴즈 제목
        quiz_content: 퀴즈 내용
        selected_content: 사용자가 선택한 답변
        correct_content: 정답 (객관식인 경우)
        is_correct: 정답 여부
        quiz_type: 퀴즈 타입

    Returns:
        str: 생성된 피드백

    Raises:
        HTTPException: API 호출 실패 시 발생
    """
    try:
        quiz_type_enum = QuizType(quiz_type) if quiz_type else QuizType.TEXT
        user_content = create_feedback_prompt(
            quiz_type_enum,
            quiz_title,
            quiz_content,
            selected_content,
            correct_content,
            is_correct,
        )

        messages: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

        timeout = aiohttp.ClientTimeout(total=OPENAI_TIMEOUT)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(OPENAI_API_URL, json=messages) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]

                error_detail = await response.text()
                logger.error(
                    f"OpenAI API 에러: 상태 코드 {response.status}, 상세: {error_detail}"
                )
                raise OpenAIError(f"API 응답 상태 코드: {response.status}")

    except aiohttp.ClientError as e:
        logger.error(f"OpenAI API 네트워크 에러: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI 서비스에 연결할 수 없습니다.",
        )

    except OpenAIError as e:
        logger.error(f"OpenAI API 에러: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAI 서비스에서 오류가 발생했습니다.",
        )

    except Exception as e:
        logger.error(f"피드백 생성 중 예상치 못한 에러 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="피드백을 생성하는 중 오류가 발생했습니다.",
        )
