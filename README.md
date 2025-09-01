# 계약서 자동 검수 시스템

## 🎯 개요
AI 기반 계약서 자동 검수 웹 시스템입니다. 내부 규칙과 27개 법률을 기반으로 계약서의 위험 요소를 자동으로 분석합니다.

## ✨ 주요 기능
- **PDF/DOCX 업로드**: 계약서 파일 자동 텍스트 추출
- **2단계 검수**: 내부 규칙 + 법률 준수 검사
- **스마트 법률 적용**: 계약 유형별 관련 법률만 선별 적용
- **실시간 결과**: 위반사항 즉시 표시 및 수정안 제공
- **레드라인 문서**: 수정 사항이 반영된 DOCX 파일 생성

## 🚀 온라인 데모
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📊 검수 범위

### 내부 규칙 (10개)
- 대금 지급 조건
- 검수 및 인수 절차  
- 인력 관리 규정
- 지연 및 납기 관리
- 세무 및 원천징수
- 변경 관리
- 지식재산권

### 법률 준수 (27개 법률)
- **민법**: 계약, 손해배상, 채권채무
- **상법**: 상거래, 회사법
- **소프트웨어 진흥법**: IT 서비스 관련
- **하도급거래 공정화법**: 하도급 관련
- **세법**: 법인세법, 부가가치세법
- 기타 관련 법률 22개

## 🎨 UI 특징
- **카드형 문서 정보**: 계약 유형, 기간, 금액 자동 추출
- **색각 보조 디자인**: 아이콘 + 색상 병행 표시
- **클릭 가능한 위반사항**: Top 3 위반사항 클릭 시 상세 내용으로 이동
- **카테고리별 그룹핑**: 관련 조항별로 정리된 결과 표시

## 🛠️ 기술 스택
- **Frontend**: Streamlit
- **Backend**: Python, FastAPI
- **문서 처리**: PyMuPDF, python-docx
- **데이터**: JSON 기반 규칙 엔진

## 📁 프로젝트 구조
```
contract-audit-web/
├── ui/
│   └── streamlit_app.py          # 메인 UI
├── app/
│   ├── services/                 # 핵심 서비스
│   │   ├── extractor.py         # 문서 텍스트 추출
│   │   ├── rules_engine.py      # 내부 규칙 엔진
│   │   ├── smart_law_engine.py  # 스마트 법률 엔진
│   │   ├── combined_engine.py   # 통합 검수 엔진
│   │   └── redline_docx.py      # 레드라인 문서 생성
│   └── models/
│       └── schema.py            # 데이터 모델
├── rules/
│   └── base.rules.json          # 내부 검수 규칙
├── laws/                        # 법률 데이터 (배포시 제외)
└── sample_docs/                 # 샘플 문서
```

## 🚀 로컬 실행

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/contract-audit-web.git
cd contract-audit-web
```

### 2. 가상환경 설정
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 실행
```bash
streamlit run ui/streamlit_app.py
```

## 🌐 Streamlit Cloud 배포

### 1. GitHub 저장소 생성
1. GitHub에서 새 저장소 생성
2. 코드 푸시

### 2. Streamlit Cloud 연결
1. [share.streamlit.io](https://share.streamlit.io) 접속
2. GitHub 저장소 연결
3. `ui/streamlit_app.py` 지정
4. 배포 완료

## 📋 사용법

### 1. 계약서 업로드
- PDF 또는 DOCX 파일 업로드
- 자동 텍스트 추출 및 문서 정보 표시

### 2. 검수 결과 확인
- 내부 규칙 위반사항 확인
- 법률 준수 사항 검토
- 위험도별 우선순위 확인

### 3. 수정 파일 다운로드
- DOCX 파일의 경우 수정 사항이 반영된 레드라인 문서 생성
- 카테고리별로 정리된 수정 제안사항 포함

## 🔧 커스터마이징

### 내부 규칙 수정
`rules/base.rules.json` 파일을 편집하여 조직의 표준에 맞게 규칙을 수정할 수 있습니다.

### 법률 데이터 업데이트
`laws/` 디렉토리에 새로운 법률 문서를 추가하여 검수 범위를 확장할 수 있습니다.

## 📄 라이선스
MIT License

## 🤝 기여하기
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의
프로젝트 관련 문의사항이 있으시면 이슈를 등록해주세요.

---
⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!