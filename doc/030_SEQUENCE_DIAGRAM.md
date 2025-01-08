# https://mermaid.live/

sequenceDiagram
    participant User
    participant Frontend
    participant Backend
    participant Database
    participant OpenAI API

    %% 시나리오 1: 회원가입 및 로그인
    
    %% 회원가입
    User->>Frontend: 회원가입 페이지 접근
    Frontend->>Backend: POST /auth/signup 요청 (email, password, nickname)
    Backend->>Database: 사용자 정보 저장 (email, password(암호화), nickname)
    Database-->>Backend: 저장된 사용자 정보 반환 (id, email, nickname, created_at, updated_at)
    Backend-->>Frontend: 201 Created, User 정보 응답
    Frontend-->>User: 회원가입 성공 메시지 표시
    
    %% 로그인
    User->>Frontend: 로그인 페이지 접근
    Frontend->>Backend: POST /auth/login 요청 (email, password)
    Backend->>Database: 사용자 정보 조회 (email, password)
    Database-->>Backend: 사용자 정보 반환 (email, password(암호화), id)
    Backend->>Backend: JWT 토큰 생성
    Backend-->>Frontend: 200 OK, Token 응답 (access_token)
    Frontend-->>User: 로그인 성공 메시지 표시 및 메인 페이지 이동
    

    %% 시나리오 2: 퀴즈 조회 및 답변 제출
    
    %% 퀴즈 목록 조회
    User->>Frontend: 퀴즈 목록 페이지 접근
    Frontend->>Backend: GET /quizzes 요청 (subject, skip, limit)
    Backend->>Database: 퀴즈 목록 조회 (subject 조건, skip, limit 적용)
    Database-->>Backend: 퀴즈 목록 반환 (id, title, content, subject, options)
    Backend-->>Frontend: 200 OK, 퀴즈 목록 응답
    Frontend-->>User: 퀴즈 목록 표시
    
    %% 특정 퀴즈 조회
    User->>Frontend: 퀴즈 상세 페이지 접근
    Frontend->>Backend: GET /quizzes/{quiz_id} 요청
    Backend->>Database: 퀴즈 정보 조회 (quiz_id)
    Database-->>Backend: 퀴즈 정보 반환 (id, title, content, subject, options)
    Backend-->>Frontend: 200 OK, 퀴즈 상세 정보 응답
    Frontend-->>User: 퀴즈 상세 정보 표시

    %% 답변 제출
    User->>Frontend: 객관식 답변 선택 후 제출
    Frontend->>Backend: POST /quizzes/{quiz_id}/submit 요청 (option_id, JWT 토큰 포함)
    Backend->>Database: 사용자 인증 (JWT 토큰 검증)
    Database-->>Backend: 사용자 정보 반환 (id)
    Backend->>Database: 답변 저장 (quiz_id, user_id, option_id)
    Database-->>Backend: 저장된 답변 정보 반환 (id, quiz_id, user_id, option_id)
    Backend->>Database: 퀴즈 정보 조회 (quiz_id)
    Database-->>Backend: 퀴즈 정보 반환 (options)
    Backend->>Backend: 선택한 옵션이 정답인지 확인
    Backend->>OpenAI API: AI 피드백 요청 (답변 내용)
    OpenAI API-->>Backend: AI 피드백 결과 반환 (content)
    Backend->>Database: 피드백 저장 (answer_id, content)
    Database-->>Backend: 저장된 피드백 정보 반환 (id, answer_id, content)
    Backend->>Backend: 답변 및 피드백 정보 결합 (answer, feedback)
    Backend-->>Frontend: 201 Created, 답변 및 피드백 정보 응답
    Frontend-->>User: 답변 및 피드백 결과 표시

    %% 시나리오 3: 사용자 정보 조회 및 수정
    
    %% 사용자 정보 조회
    User->>Frontend: 사용자 프로필 페이지 접근
    Frontend->>Backend: GET /users/me 요청 (JWT 토큰 포함)
    Backend->>Database: 사용자 인증 (JWT 토큰 검증)
    Database-->>Backend: 사용자 정보 반환 (id, email, nickname, created_at, updated_at)
    Backend-->>Frontend: 200 OK, 사용자 정보 응답
    Frontend-->>User: 사용자 프로필 정보 표시
    
    %% 사용자 정보 수정
    User->>Frontend: 사용자 닉네임 수정 후 저장
    Frontend->>Backend: PUT /users/me 요청 (nickname, JWT 토큰 포함)
    Backend->>Database: 사용자 인증 (JWT 토큰 검증)
    Database-->>Backend: 사용자 정보 반환 (id)
    Backend->>Database: 사용자 정보 업데이트 (nickname)
    Database-->>Backend: 업데이트된 사용자 정보 반환 (id, email, nickname, created_at, updated_at)
    Backend-->>Frontend: 200 OK, 업데이트된 사용자 정보 응답
    Frontend-->>User: 수정된 사용자 프로필 정보 표시