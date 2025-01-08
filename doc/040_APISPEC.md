## API 명세 (최종 - 마크다운 형식)

### 1. 사용자 인증 API

#### 1.1. 회원가입 (`/auth/signup`)

*   **HTTP Method:** `POST`
*   **URL:** `/auth/signup`
*   **요청 헤더:**
    *   `Content-Type: application/json`
*   **요청 바디:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123",
        "nickname": "user123"
    }
    ```
*   **성공 응답 (201 Created):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        {
            "id": 1,
            "email": "user@example.com",
            "nickname": "user123",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        ```
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청 형식)
    *   409 Conflict (이미 존재하는 이메일)

#### 1.2. 로그인 (`/auth/login`)

*   **HTTP Method:** `POST`
*   **URL:** `/auth/login`
*   **요청 헤더:**
    *   `Content-Type: application/json`
*   **요청 바디:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        ```
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청 형식)
    *   401 Unauthorized (잘못된 이메일 또는 비밀번호)

#### 1.3. 로그아웃 (`/auth/logout`)
*   **HTTP Method:** `POST`
*   **URL:** `/auth/logout`
*   **요청 헤더:**
    *   `Authorization: Bearer <access_token>`
*   **요청 바디:** 없음
*   **성공 응답 (204 No Content):**
    *   **응답 헤더:** 없음
*   **실패 응답:**
    *   401 Unauthorized (인증 실패)

### 2. 콘텐츠 유형 및 주제 API

#### 2.1. 콘텐츠 유형 목록 조회 (`/content-types`)

*   **HTTP Method:** `GET`
*   **URL:** `/content-types`
*   **요청 헤더:** 없음
*   **요청 바디:** 없음
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        [
            {
                "id": 1,
                "name": "퀴즈",
                "description": "객관식 퀴즈를 통해 프로그래밍 지식을 테스트합니다.",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "코딩 테스트",
                "description": "코딩 테스트 환경을 제공하여 실전 감각을 익힙니다.",
                "created_at": "2024-01-01T00:00:00",
                 "updated_at": "2024-01-01T00:00:00"
            }
        ]
        ```
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청)

#### 2.2. 특정 콘텐츠 유형에 따른 주제 목록 조회 (`/content-types/{content_type_id}/subjects`)

*   **HTTP Method:** `GET`
*   **URL:** `/content-types/{content_type_id}/subjects`
*   **요청 파라미터:**
    *   `content_type_id` (Path Parameter, Integer): 조회할 콘텐츠 유형의 ID
*  **요청 헤더:** 없음
*  **요청 바디:** 없음
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        [
            {
                "id": 1,
                 "content_type_id": 1,
                "name": "Python 문법",
                "description": "파이썬 프로그래밍 문법을 학습합니다.",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            },
            {
                "id": 2,
                 "content_type_id": 1,
                "name": "FastAPI 문법",
                "description": "FastAPI 프레임워크 사용법을 학습합니다.",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]
        ```
*   **실패 응답:**
    *   404 Not Found (해당 콘텐츠 유형이 존재하지 않음)
    *   400 Bad Request (잘못된 요청)

### 3. 퀴즈 API

#### 3.1. 퀴즈 목록 조회 (`/quizzes`)

*   **HTTP Method:** `GET`
*   **URL:** `/quizzes`
*   **요청 파라미터:**
    *   `subject` (Optional, String): 퀴즈 주제 필터링 (예: `Python 문법`, `FastAPI 문법`)
    *   `skip` (Optional, Integer, Default: 0): 페이지네이션을 위한 스킵할 항목 수
    *   `limit` (Optional, Integer, Default: 10): 페이지네이션을 위한 한 페이지당 항목 수
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        [
            {
                "id": 1,
                "title": "파이썬 변수 선언",
                "content": "파이썬에서 변수를 선언하는 방법은?",
                "options": "[{\"id\": 1, \"content\": \"int x = 10\"}, {\"id\": 2, \"content\": \"x := 10\"}, {\"id\": 3, \"content\": \"x = 10\", \"is_correct\": true}, {\"id\": 4, \"content\": \"var x = 10\"}]",
                "subject": "Python 문법",
                 "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            },
             {
                "id": 2,
                "title": "FastAPI 경로 파라미터",
                "content": "FastAPI에서 경로 파라미터를 정의하는 방법은?",
                "options": "[{\"id\": 1, \"content\": \"@app.route('/items/{item_id}')\"}, {\"id\": 2, \"content\": \"@app.get('/items/<int:item_id>')\"}, {\"id\": 3, \"content\": \"@app.get('/items/{item_id}')\", \"is_correct\": true}, {\"id\": 4, \"content\": \"@app.path('/items/{item_id}')\"}]",
                "subject": "FastAPI 문법",
                 "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]
        ```
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청)

#### 3.2. 특정 퀴즈 조회 (`/quizzes/{quiz_id}`)

*   **HTTP Method:** `GET`
*   **URL:** `/quizzes/{quiz_id}`
*   **요청 파라미터:**
    *   `quiz_id` (Path Parameter, Integer): 조회할 퀴즈의 ID
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
       {
            "id": 1,
            "title": "파이썬 변수 선언",
            "content": "파이썬에서 변수를 선언하는 방법은?",
            "options": "[{\"id\": 1, \"content\": \"int x = 10\"}, {\"id\": 2, \"content\": \"x := 10\"}, {\"id\": 3, \"content\": \"x = 10\", \"is_correct\": true}, {\"id\": 4, \"content\": \"var x = 10\"}]",
            "subject": "Python 문법",
             "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        ```
*   **실패 응답:**
    *   404 Not Found (해당 퀴즈가 존재하지 않음)

#### 3.3. 퀴즈 제출 (`/quizzes/{quiz_id}/submit`)
*   **HTTP Method:** `POST`
*   **URL:** `/quizzes/{quiz_id}/submit`
*   **요청 헤더:**
    *   `Content-Type: application/json`
    *   `Authorization: Bearer <access_token>`
*   **요청 파라미터:**
    *   `quiz_id` (Path Parameter, Integer): 제출할 퀴즈의 ID
*   **요청 바디:**
    ```json
    {
        "option_id": 3
    }
    ```
*   **성공 응답 (201 Created):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
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
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청 형식)
    *   401 Unauthorized (인증 실패)
    *   404 Not Found (해당 퀴즈가 존재하지 않음)

### 4. 사용자 API

#### 4.1. 사용자 정보 조회 (`/users/me`)

*   **HTTP Method:** `GET`
*   **URL:** `/users/me`
*   **요청 헤더:**
    *   `Authorization: Bearer <access_token>`
*   **요청 바디:** 없음
*   **성공 응답 (200 OK):**
    *   **응답 헤더:** `Content-Type: application/json`
    *   **응답 바디:**
        ```json
        {
            "id": 1,
            "email": "user@example.com",
            "nickname": "user123",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        ```
*   **실패 응답:**
    *   401 Unauthorized (인증 실패)

#### 4.2. 사용자 정보 수정 (`/users/me`)
*   **HTTP Method:** `PUT`
*   **URL:** `/users/me`
*   **요청 헤더:**
    *   `Content-Type: application/json`
    *   `Authorization: Bearer <access_token>`
*   **요청 바디:**
    ```json
     {
        "nickname": "new_user123"
      }
    ```
*  **성공 응답 (200 OK):**
    *  **응답 헤더:** `Content-Type: application/json`
    *  **응답 바디:**
        ```json
        {
            "id": 1,
            "email": "user@example.com",
            "nickname": "new_user123",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        ```
*   **실패 응답:**
    *   400 Bad Request (잘못된 요청 형식)
    *   401 Unauthorized (인증 실패)