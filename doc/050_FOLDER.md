# 프로젝트 폴더 구조

```
.
├── README.md                           # 프로젝트 소개 및 설치 가이드
├── backend/                            # 백엔드 애플리케이션 루트
│   ├── app/                            # FastAPI 애플리케이션
│   │   ├── __init__.py                 # Python 패키지 선언
│   │   ├── api/                        # API 엔드포인트 정의
│   │   │   ├── __init__.py             # API 라우터 통합
│   │   │   ├── auth.py                 # 인증/인가 관련 API (회원가입, 로그인)
│   │   │   ├── content_type.py         # 콘텐츠 타입 CRUD API
│   │   │   ├── quiz.py                 # 퀴즈 관련 API (조회, 제출, 피드백)
│   │   │   ├── subject.py              # 주제 관련 API
│   │   │   └── user.py                 # 사용자 관련 API (프로필, 학습 이력)
│   │   ├── core/                       # 핵심 기능 및 설정
│   │   │   ├── __init__.py             # 코어 모듈 통합
│   │   │   ├── database.py             # 데이터베이스 연결 및 세션 관리
│   │   │   └── utils.py                # 공통 유틸리티 함수
│   │   ├── main.py                     # FastAPI 앱 진입점 및 설정
│   │   ├── models/                     # SQLAlchemy 모델 정의
│   │   │   ├── __init__.py             # 모델 통합
│   │   │   ├── answer.py               # 답변 모델
│   │   │   ├── content_type.py         # 콘텐츠 타입 모델
│   │   │   ├── quiz.py                 # 퀴즈 모델
│   │   │   ├── subject.py              # 주제 모델
│   │   │   └── user.py                 # 사용자 모델
│   │   ├── schemas/                    # Pydantic 스키마 정의
│   │   │   ├── __init__.py             # 스키마 통합
│   │   │   ├── content_type.py         # 콘텐츠 타입 요청/응답 스키마
│   │   │   ├── quiz.py                 # 퀴즈 요청/응답 스키마
│   │   │   ├── subject.py              # 주제 요청/응답 스키마
│   │   │   └── user.py                 # 사용자 요청/응답 스키마
│   │   └── tests/                      # 테스트 코드
│   │       └── __init__.py             # 테스트 패키지 선언
│   ├── bitbox.db                       # SQLite 데이터베이스 파일
│   └── requirements.txt                # Python 패키지 의존성 목록
├── doc/                                # 프로젝트 문서
│   ├── 001_PRD.md                      # 제품 요구사항 문서
│   ├── 010_ADR.md                      # 아키텍처 결정 기록
│   ├── 020_ERD.md                      # 데이터베이스 스키마 설계
│   ├── 030_SEQUENCE_DIAGRAM.md         # 시스템 시퀀스 다이어그램
│   ├── 040_APISPEC.md                  # API 명세서
│   └── 050_FOLDER.md                   # 폴더 구조 설명 (현재 파일)
└── frontend/                           # 프론트엔드 애플리케이션 루트
    ├── css/                            # 스타일시트
    │   └── style.css                   # 전역 스타일 정의
    ├── index.html                      # 메인 페이지
    ├── js/                             # JavaScript 모듈
    │   └── auth.js                     # 인증 관련 기능 (로그인, 회원가입)
    └── pages/                          # HTML 페이지
        ├── content_type_list.html      # 콘텐츠 타입 목록 페이지
        ├── dashboard.html              # 대시보드 페이지
        ├── login.html                  # 로그인 페이지
        ├── profile.html                # 사용자 프로필 페이지
        ├── quiz.html                   # 퀴즈 목록 페이지
        ├── quiz_detail.html            # 퀴즈 상세/풀이 페이지
        ├── signup.html                 # 회원가입 페이지
        └── subject_list.html           # 주제 목록 페이지
```