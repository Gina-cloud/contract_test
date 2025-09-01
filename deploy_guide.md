# GitHub & Streamlit Cloud 배포 가이드

## 📋 배포 준비 완료 사항

### ✅ 파일 구조 정리
- `.gitignore`: 불필요한 파일 제외
- `requirements.txt`: Streamlit Cloud용 패키지 목록
- `streamlit_app.py`: 메인 엔트리 포인트
- `README.md`: 프로젝트 설명서

### ✅ 최적화 완료
- 대용량 법률 파일 제외 (laws/raw_docs/)
- 테스트 출력 파일 제외
- 가상환경 파일 제외

## 🚀 배포 단계

### 1. GitHub 저장소 생성
```bash
# 1) GitHub에서 새 저장소 생성 (예: contract-audit-web)
# 2) 로컬에서 Git 초기화
cd C:\Users\contract-audit-web
git init
git add .
git commit -m "Initial commit: Contract audit system"

# 3) 원격 저장소 연결
git remote add origin https://github.com/YOUR_USERNAME/contract-audit-web.git
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud 배포
1. **https://share.streamlit.io** 접속
2. **GitHub 계정으로 로그인**
3. **"New app" 클릭**
4. **저장소 선택**: `YOUR_USERNAME/contract-audit-web`
5. **Branch**: `main`
6. **Main file path**: `streamlit_app.py`
7. **"Deploy!" 클릭**

### 3. 배포 완료 확인
- 약 2-3분 후 앱 URL 생성
- 예: `https://your-username-contract-audit-web-streamlit-app-xyz123.streamlit.app`

## 🔧 배포 후 설정

### 환경 변수 (필요시)
Streamlit Cloud 대시보드에서 환경 변수 설정 가능

### 도메인 커스터마이징
- Streamlit Cloud Pro 계정에서 커스텀 도메인 설정 가능

## 📊 현재 시스템 특징

### ✨ 주요 기능
- **내부 규칙 검수**: 10개 핵심 규칙
- **스마트 법률 적용**: 계약 유형별 관련 법률만 선별
- **실시간 문서 분석**: PDF/DOCX 업로드 즉시 분석
- **레드라인 문서 생성**: 수정사항 반영된 DOCX 다운로드

### 🎯 검수 범위
- **계약 유형 자동 감지**: 용역/개발/공급/일반계약
- **관련 법률 선별 적용**: 불필요한 법률 검사 제외
- **위험도별 분류**: 필수/권고 위반사항 구분

### 🎨 UI 특징
- **반응형 디자인**: 최대 1100px 너비
- **카드형 정보 표시**: 문서 정보 직관적 표시
- **색각 보조**: 아이콘 + 색상 병행
- **클릭 가능한 위반사항**: Top 3 → 상세 테이블 이동

## 🛠️ 추가 개발 아이디어

### Phase 3 (향후 확장)
- **벡터 검색**: 법률 조항 유사도 기반 검색
- **AI 요약**: GPT 기반 계약서 요약
- **다국어 지원**: 영문 계약서 지원
- **API 제공**: REST API로 외부 시스템 연동

### 고급 기능
- **판례 데이터베이스**: 관련 판례 자동 매칭
- **신구법 비교**: 법률 개정사항 자동 반영
- **전자결재 연동**: 기업 워크플로우 통합

## 📞 배포 지원

배포 과정에서 문제가 발생하면:
1. **Streamlit Cloud 로그 확인**
2. **requirements.txt 패키지 버전 확인**
3. **파일 경로 문제 확인**

---
🎉 **배포 완료 후 URL을 공유해주시면 테스트 도와드리겠습니다!**