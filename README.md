# BitBox

BitBox는 프로그래밍 학습 초보자와 주니어 개발자를 위한 학습 플랫폼입니다. 객관식 퀴즈, 코딩 테스트, 면접 준비 등 다양한 학습 콘텐츠를 제공하며, AI 기반의 즉각적인 피드백을 통해 효과적인 학습을 지원합니다.

## 주요 기능

- **다양한 학습 콘텐츠**
  - 객관식 퀴즈
  - 코딩 테스트
  - 면접 준비 문제
  
- **AI 기반 피드백**
  - 답변에 대한 즉각적인 피드백
  - 개선점 및 학습 방향 제시
  
- **학습 진행 관리**
  - 주제별 학습 진행률 확인
  - 개인 학습 이력 관리

## 기술 스택

### Backend
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite3 (Database)
- OpenAI API (AI 피드백)

### Frontend
- HTML/CSS/JavaScript
- Monaco Editor (코드 에디터)
- Toast UI Editor (텍스트 에디터)

## 시작하기

### 요구사항
- Python 3.8 이상

### 설치 및 실행

1. 저장소 클론
```bash
git clone git@github.com:MyBitBox/bitbox.git
cd bitbox
```

2. 백엔드 설정
```bash
cd backend
pip install -r requirements.txt
```

3. 환경 변수 설정
```bash
cd backend
touch .env
echo "SECRET_KEY=your-secret-key" >> .env
```

4. 서버 실행
```bash
uvicorn app.main:app --reload
```

5. 프론트엔드 접속
- 브라우저에서 `/frontend/index.html` 열기

## API 문서

- API 문서는 서버 실행 후 `/docs` 또는 `/redoc` 엔드포인트에서 확인 가능
- 주요 API 엔드포인트:
  - `/api/auth/*`: 인증 관련 (회원가입, 로그인, 로그아웃)
  - `/api/users/*`: 사용자 정보 및 학습 진행률
  - `/api/content_types/*`: 콘텐츠 타입 관리
  - `/api/subjects/*`: 학습 주제 관리
  - `/api/quizzes/*`: 퀴즈 관련 CRUD 및 제출
  
## 프로젝트 구조

```
.
├── backend/                # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 엔드포인트
│   │   ├── core/           # 핵심 기능 및 설정
│   │   ├── models/         # 데이터베이스 모델
│   │   └── schemas/        # Pydantic 스키마
│   └── requirements.txt
├── frontend/               # 프론트엔드
│   ├── css/
│   ├── js/
│   └── pages/              # HTML 페이지
└── doc/                    # 프로젝트 문서
```

## 문서

자세한 내용은 `doc` 디렉토리의 문서를 참조하세요:
- [제품 요구사항](doc/001_PRD.md)
- [아키텍처 결정 기록](doc/010_ADR.md)
- [데이터베이스 스키마](doc/020_ERD.md)
- [시스템 시퀀스](doc/030_SEQUENCE_DIAGRAM.md)
- [API 명세서](doc/040_APISPEC.md)
- [폴더 구조](doc/050_FOLDER.md)