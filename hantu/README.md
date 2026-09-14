# 한국투자증권 API 연동 가이드 (hantu)

그리드센서KR 사용자를 위한 **한국투자증권 API 연동 가이드** 배포용 정적 페이지입니다.
한국투자증권 KIS Developers에서 APP Key / APP Secret을 발급받아 그리드센서KR에 등록하는 과정을 STEP 1~8로 안내합니다.

## 🔗 배포 주소

https://ansojang.github.io/hantu/

## 📁 구성

```
hantu/
├── index.html      # 가이드 본문 (HTML + CSS 단일 파일, 외부 스크립트 없음)
├── step-02.jpg     # KIS Developers 서비스 신청/조회 메뉴
├── step-03.jpg     # 휴대폰 인증
├── step-04.jpg     # 실전투자계좌 신청
├── step-05.jpg     # QR 인증
├── step-06.jpg     # APP Key 생성 완료
├── step-07.jpg     # 그리드센서KR API 키 등록 메뉴
├── step-08.jpg     # 키 등록 입력 항목
├── shot-credit.jpg # 화면 예시 — 신용거래 신청상태 「미신청」 (개인정보 마스킹)
├── shot-margin.jpg # 화면 예시 — 통합증거금 거래신청 상태 「미신청」 (개인정보 마스킹)
└── README.md
```

모든 자산을 같은 폴더에 두고 **상대 경로**로 참조하므로, `ansojang.github.io` 저장소의 하위 폴더에 그대로 올리면 바로 동작합니다.

## 📋 가이드 목차

| STEP | 내용 |
|------|------|
| 1 | 한국투자증권 홈페이지 접속 |
| 2 | KIS Developers 서비스 신청 / 조회 클릭 |
| 3 | 휴대폰 인증 |
| 4 | KIS Developers 서비스 신청하기 |
| 5 | QR 인증 |
| 6 | 한국투자증권 APP키 생성 완료 |
| 7 | 그리드센서KR API키 등록 메뉴 접속 |
| 8 | 키 등록 하기 |

### 추가 안내 — 전략 세팅 전 필수 점검 (체험판 OT 15~23p)

| 항목 | 내용 |
|------|------|
| 1-2 | 원화 입금 및 환전 (KR / US) |
| 1-2 | 환전은 US 전략 세팅 「전에」 미리 |
| 1-3 | 신용거래 · 통합증거금 「미신청」 확인 |
| 1-3 ① | 신용거래 — 미신청 확인 / 왜 신용을 쓰지 않는가 |
| 1-3 ② | 통합증거금 — 미신청 확인 / 왜 통합증거금을 쓰지 않는가 |

## 🚀 배포

`ansojang/ansojang.github.io` 저장소의 `hantu/` 폴더에 업로드하면 GitHub Pages가 1~2분 내 반영합니다.
메인 사이트(root)는 건드리지 않습니다.

## ⚙️ 배포용 최적화 내역

- 원본 HTML에 base64로 박혀 있던 이미지 7장을 개별 `.jpg` 파일로 분리 (HTML 492KB → 13KB)
- 첫 이미지 `fetchpriority="high"`, 나머지 `loading="lazy"` 지연 로딩
- Pretendard 웹폰트 적용 (윈도우·안드로이드에서도 동일한 글꼴)
- SEO 메타태그 + Open Graph / Twitter 카드 + canonical 추가
- SVG 파비콘 인라인 삽입
- 앱 화면 예시 2장은 계좌번호·휴대폰·이메일을 마스킹 처리 후 게시

## 📄 라이선스

© 글로벌셀러창업연구소(주) · 그리드센서KR. 사내 교육 및 고객 안내용 자료입니다.
