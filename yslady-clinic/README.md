# 연세미 여성의원 사이트 — 콘텐츠 발행 가이드

각 1차 메뉴마다 **전용 게시판**이 있고, 글 HTML 파일을 폴더에 추가하는 방식으로 콘텐츠를 계속 발행합니다.

## 폴더 구조

```
yslady-clinic/
├─ index.html                 메인 페이지
├─ assets/style.css           공유 디자인(글씨체·색상)
├─ _post-template.html        ← 새 글 만들 때 복사해서 쓰는 템플릿
├─ about/       index.html + 글들      (병원소식·공지)
├─ surgery/     index.html + 글들      (여성성형 정보)
├─ pregnancy/   index.html + 글들      (임신·산부인과 칼럼)
├─ checkup/     index.html + 글들      (건강검진 가이드)
├─ beauty/      index.html + 글들      (뷰티 클리닉 소식)
└─ community/   index.html + 글들      (온라인 상담·FAQ)
```

## 새 글 발행하는 법 (3단계)

**1. 템플릿 복사** — `_post-template.html`을 복사해 발행할 메뉴 폴더 안에 새 이름으로 저장합니다.
   예: 여성성형 글이면 `surgery/post-이쁜이수술-비용.html` (영문·하이픈 파일명 권장)

**2. 내용 채우기** — 파일을 열어 `[대괄호]` 부분을 실제 내용으로 바꿉니다.
   - `<title>` / 요약 설명 : 검색 키워드 + "인천" 포함
   - `canonical` 주소의 `[메뉴폴더]/[파일명]`을 실제 값으로 수정
   - 제목(H1)은 **질문형**이면 검색·AI 답변 노출에 유리
   - 요약(summary)에 **핵심 답변을 먼저** 한두 문장으로
   - FAQ 2개 이상 채우기 (JSON-LD와 본문 모두)

**3. 목록에 카드 추가** — 해당 메뉴 `index.html`을 열어 게시판 `<ul>` 안에 한 줄 추가:
   ```html
   <li><a href="파일명.html"><span><span class="tag">정보</span>새 글 제목</span><span class="d">2026.07.10 · NEW</span></a></li>
   ```
   (필요하면 메인 `index.html`의 Journal 섹션 카드도 같은 방식으로 교체)

이 세 파일을 GitHub에 커밋하면 `https://ansojang.github.io/yslady-clinic/[메뉴]/` 게시판에 바로 반영됩니다.

## 꼭 지킬 것 (의료법 제56조 준수)

- 치료 효과를 **보장·단정하는 표현 금지** ("반드시 완치", "부작용 없음" 등)
- 후기·전후 사진은 치료효과 오인 우려가 없도록 주의 (필요 시 의료광고 심의 확인)
- 각 글에는 "개인차가 있으며 정확한 진단은 내원 진료" 안내(callout)를 유지

## SEO/GEO/AEO 자동 반영 요소

템플릿에는 아래가 이미 들어 있어, 내용만 채우면 3중 최적화가 적용됩니다.
- 시맨틱 HTML · title · meta description · Open Graph
- JSON-LD (MedicalWebPage + FAQPage)
- 질문형 헤딩 + 답변 우선 요약 + FAQ 섹션
