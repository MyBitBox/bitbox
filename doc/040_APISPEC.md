# BitBox API 명세서

## 전체 요약
BitBox API는 프로그래밍 학습 초보자 및 주니어 개발자를 위해 설계된 서비스입니다. 사용자는 다양한 주제별 퀴즈를 풀고, AI 기반 피드백을 받을 수 있으며, 자신의 학습 상태를 관리할 수 있습니다. 이 문서는 RESTful API 형식으로 설계된 백엔드 엔드포인트 명세서를 제공합니다.

---

## 1. 사용자 인증 API

### 1.1 회원가입 (`/auth/signup`)
- **HTTP 메서드**: `POST`
- **요청 헤더**
  - `Content-Type: application/json`
- **요청 바디**
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "nickname": "user123"
  }
  ```
- **응답**
  - 성공 (`201 Created`)
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "nickname": "user123",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    ```
  - 실패
    - `409 Conflict`: 이미 존재하는 이메일/닉네임

---

### 1.2 로그인 (`/auth/login`)
- **HTTP 메서드**: `POST`
- **요청 헤더**
  - `Content-Type: application/json`
- **요청 바디**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **응답**
  - 성공 (`200 OK`)
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1Ni...",
      "token_type": "bearer"
    }
    ```
  - 실패
    - `401 Unauthorized`: 이메일 또는 비밀번호 오류

---

### 1.3 로그아웃 (`/auth/logout`)
- **HTTP 메서드**: `POST`
- **요청 헤더**
  - `Authorization: Bearer <access_token>`
- **요청 바디**: 없음
- **응답**
  - 성공 (`204 No Content`)
  - 실패
    - `401 Unauthorized`: 인증 실패

---

## 2. 퀴즈 API

### 2.1 퀴즈 목록 조회 (`/quizzes`)
- **HTTP 메서드**: `GET`
- **요청 파라미터**
  - `subject` (선택, 문자열): 퀴즈 주제 필터링 (예: `Python 문법`)
  - `skip` (선택, 정수, 기본값: 0): 페이지네이션을 위한 스킵 수
  - `limit` (선택, 정수, 기본값: 10): 페이지네이션 항목 수
- **응답**
  - 성공 (`200 OK`)
    ```json
    [
      {
        "id": 1,
        "title": "파이썬 변수 선언",
        "content": "파이썬에서 변수를 선언하는 방법은?",
        "options": [
          {"id": 1, "content": "int x = 10"},
          {"id": 2, "content": "x := 10"},
          {"id": 3, "content": "x = 10", "is_correct": true},
          {"id": 4, "content": "var x = 10"}
        ],
        "subject": "Python 문법",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
      }
    ]
    ```
  - 실패
    - `400 Bad Request`: 잘못된 요청

---

### 2.2 특정 퀴즈 조회 (`/quizzes/{quiz_id}`)
- **HTTP 메서드**: `GET`
- **요청 파라미터**
  - `quiz_id` (경로 파라미터, 정수): 조회할 퀴즈의 ID
- **응답**
  - 성공 (`200 OK`)
    ```json
    {
      "id": 1,
      "title": "파이썬 변수 선언",
      "content": "파이썬에서 변수를 선언하는 방법은?",
      "options": [
        {"id": 1, "content": "int x = 10"},
        {"id": 2, "content": "x := 10"},
        {"id": 3, "content": "x = 10", "is_correct": true},
        {"id": 4, "content": "var x = 10"}
      ],
      "subject": "Python 문법",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    ```
  - 실패
    - `404 Not Found`: 해당 퀴즈가 존재하지 않음

---

### 2.3 퀴즈 제출 (`/quizzes/{quiz_id}/submit`)
- **HTTP 메서드**: `POST`
- **요청 헤더**
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **요청 파라미터**
  - `quiz_id` (경로 파라미터, 정수): 제출할 퀴즈의 ID
- **요청 바디**
  ```json
  {
    "option_id": 3
  }
  ```
- **응답**
  - 성공 (`201 Created`)
    ```json
    {
      "id": 1,
      "quiz_id": 1,
      "user_id": 1,
      "option_id": 3,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "feedback": {
        "id": 1,
        "content": "정답입니다. 파이썬에서 변수 선언은 x = 값 형태로 합니다.",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
      }
    }
    ```
  - 실패
    - `400 Bad Request`: 잘못된 요청
    - `401 Unauthorized`: 인증 실패
    - `404 Not Found`: 해당 퀴즈가 존재하지 않음

---

## 3. 사용자 API

### 3.1 사용자 정보 조회 (`/users/me`)
- **HTTP 메서드**: `GET`
- **요청 헤더**
  - `Authorization: Bearer <access_token>`
- **요청 바디**: 없음
- **응답**
  - 성공 (`200 OK`)
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "nickname": "user123",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    ```
  - 실패
    - `401 Unauthorized`: 인증 실패

---

### 3.2 사용자 정보 수정 (`/users/me`)
- **HTTP 메서드**: `PUT`
- **요청 헤더**
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **요청 바디**
  ```json
  {
    "nickname": "new_user123"
  }
  ```
- **응답**
  - 성공 (`200 OK`)
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "nickname": "new_user123",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    ```
  - 실패
    - `400 Bad Request`: 잘못된 요청 형식
    - `401 Unauthorized`: 인증 실패

