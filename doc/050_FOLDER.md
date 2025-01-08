```
project_root/
├── backend/           # 백엔드 관련 코드
│   ├── app/           # FastAPI 애플리케이션 코드
│   │   ├── __init__.py
│   │   ├── api/       # API 엔드포인트 관련 코드
│   │   │   ├── __init__.py
│   │   │   ├── auth.py   # 사용자 인증 관련 API
│   │   │   ├── quiz.py   # 퀴즈 관련 API
│   │   │   ├── content_type.py # 콘텐츠 유형 관련 API
│   │   │   ├── subject.py # 주제 관련 API
│   │   │   ├── user.py   # 사용자 프로필 관련 API
│   │   ├── core/      # 핵심 로직 및 유틸리티 코드
│   │   │   ├── __init__.py
│   │   │   ├── config.py # 환경 설정
│   │   │   ├── database.py # 데이터베이스 연결
│   │   │   ├── security.py # 보안 관련
│   │   │   ├── utils.py # 유틸리티 함수
│   │   ├── models/    # 데이터베이스 모델
│   │   │   ├── __init__.py
│   │   │   ├── user.py  # 사용자 모델
│   │   │   ├── quiz.py  # 퀴즈 모델
│   │   │   ├── content_type.py # 콘텐츠 유형 모델
│   │   │   ├── subject.py # 주제 모델
│   │   │   ├── answer.py # 답변 모델
│   │   │   ├── feedback.py # 피드백 모델
│   │   ├── schemas/    # API 스키마 (Pydantic)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── quiz.py
│   │   │   ├── content_type.py
│   │   │   ├── subject.py
│   │   ├── tests/     # 테스트 코드
│   │   │   ├── __init__.py
│   │   │   ├── test_api.py
│   │   │   ├── test_services.py
│   │   ├── main.py      # FastAPI 애플리케이션 진입점
│   ├── migrations/     # 데이터베이스 마이그레이션
│   │   ├── versions/
│   │   ├── env.py
│   │   ├── alembic.ini
│   ├── .env            # 환경 변수 파일
│   ├── requirements.txt # 의존성 목록
│   ├── Dockerfile       # Dockerfile
│   └── docker-compose.yml # Docker Compose 파일
├── frontend/          # 프론트엔드 관련 코드
│   ├── assets/        # 이미지, 폰트 등 정적 파일
│   │   ├── images/
│   │   └── fonts/
│   ├── css/           # CSS 스타일 파일
│   │   ├── style.css
│   ├── js/            # JavaScript 코드
│   │   ├── app.js       # 메인 JavaScript 파일
│   │   ├── auth.js      # 사용자 인증 관련
│   │   ├── quiz.js      # 퀴즈 관련
│   │   ├── dashboard.js # 대시보드 관련
│   │   ├── content_type.js # 콘텐츠 유형 관련
│   │   ├── api.js      # API 호출 관련
│   ├── pages/        # HTML 페이지
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── dashboard.html
│   │   ├── quiz.html
│   │   ├── content_type.html # 콘텐츠 유형 선택 페이지
│   │   ├── subject.html # 주제 선택 페이지
│   ├── components/     # 재사용 가능한 UI 컴포넌트
│   │   ├── header.html
│   │   ├── footer.html
│   └── index.html      # 초기 진입점
├── docs/              # 문서 관련
├── .gitignore         # Git 무시 파일
└── README.md          # 프로젝트 설명 파일
```