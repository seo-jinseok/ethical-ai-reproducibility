# 한국어 논문 테이블 수정 및 본문 내용 보존 가이드

## 문제 상황
논문의 테이블들이 페이지 너비를 초과하여 잘리는 문제가 발생했고, 테이블 수정 과정에서 원본 논문의 본문 내용이 손실되었습니다.

## 해결책 개요
본 가이드는 다음과 같은 해결책을 제시합니다:
1. 원본 한국어 논문 내용 복원
2. 테이블 너비 문제 해결
3. 본문 내용과 수정된 테이블 모두 보존

## 파일 구조

### `tex/paper_kor.tex`
- 완전한 한국어 논문 파일
- 모든 원본 본문 내용 포함
- 수정된 테이블 포맷 적용
- 올바른 LaTeX 패키지 사용

### `tex/paper_kor_new.tex`
- 백업 파일 (현재 비어있음)
- 향후 수정 작업 시 원본 보존용

## 테이블 너비 해결 방법

### 1. 사용된 LaTeX 패키지
```latex
% 테이블 관리 패키지
\usepackage{adjustbox}    % 테이블 스케일링
\usepackage{tabularx}     % 반응형 칼럼 너비
\usepackage{longtable}    # 다중 페이지 테이블
\usepackage{booktabs}     % 전문적인 테이블 형식
\usepackage{array}        % 칼럼 타입 확장
\usepackage{multirow}     % 다중행 셀
```

### 2. 테이블 형식별 해결책

#### A. adjustbox를 사용한 스케일링
```latex
\begin{table}[htbp]
\centering
\begin{adjustbox}{width=\textwidth}
\begin{tabular}{|l|c|c|c|c|c|c|}
% 테이블 내용
\end{tabular}
\end{adjustbox}
\caption{테이블 제목}
\end{table}
```

**장점:**
- 간단한 구현
- 테이블 구조 보존
- 자동 크기 조정

**단점:**
- 너무 넓은 테이블의 경우 텍스트가 작아질 수 있음

#### B. tabularx를 사용한 반응형 칼럼
```latex
\begin{table}[htbp]
\centering
\begin{tabularx}{\textwidth}{|l|X|X|X|X|}
% X 칼럼은 자동으로 확장됨
% l, c, r은 고정 너비
\end{tabularx}
\caption{테이블 제목}
\end{table>
```

**장점:**
- 텍스트 가독성 유지
- 칼럼 내 텍스트 래핑
- 자동 너비 조정

**단점:**
- 수동으로 칼럼 타입 지정 필요
- 테이블 높이 증가 가능

#### C. longtable을 사용한 다중 페이지 테이블
```latex
\begin{longtable}{|l|c|c|c|c|c|}
\caption{긴 테이블} \\
\hline
% 헤더 행
\endfirsthead
% 계속 페이지 헤더
\multicolumn{6}{c}{\textbf{이전 페이지에서 계속}} \\
\hline
% 헤더 행
\endhead
% 계속 페이지 푸터
\hline \multicolumn{6}{r}{\textit{다음 페이지에 계속}} \\
\endfoot
% 마지막 푸터
\hline
\endlastfoot
% 테이블 내용
\end{longtable}
```

**장점:**
- 매우 긴 테이블 처리
- 자동 페이지 나누기
- 커스텀 헤더/푸터

**단점:**
- 복잡한 문법
- table 환경과 함께 사용 불가

## 구현된 한국어 논문 내용

### 주요 섹션
1. **서론**: AI 윤리 평가의 중요성과 연구 목적
2. **관련 연구**: 기존 AI 윤리 연구의 한계점
3. **연구 방법론**: 실험 설계 및 평가 지표
4. **실험 결과**: 6개의 상세한 결과 테이블
5. **논의 및 한계점**: 연구 결과 해석 및 제한사항
6. **결론**: 연구 성과 및 향후 계획

### 포함된 테이블
1. 문화적 민감성 점수 (adjustbox 사용)
2. 프레임워크 성능 비교 (tabularx 사용)  
3. 적대적 견고성 테스트 결과 (longtable 사용)
4. 전문가 패널 평가 (adjustbox 사용)
5. 통계적 유의성 분석 (tabularx 사용)

## 사용 방법

### 1. LaTeX 컴파일
```bash
cd tex/
pdflatex paper_kor.tex
```

### 2. 추가 패키지 필요 시
```bash
# Ubuntu/Debian
sudo apt install texlive-lang-korean texlive-fonts-recommended

# 또는 개별 패키지 설치
tlmgr install kotex adjustbox tabularx longtable
```

### 3. 테이블 수정 작업 프로세스
1. `paper_kor.tex`를 `paper_kor_new.tex`로 백업
2. `paper_kor.tex`에서 테이블 수정 작업 수행
3. 컴파일 테스트로 오류 확인
4. 원본 내용 손실 방지를 위해 정기적 백업

## 베스트 프랙티스

### 1. 패키지 로딩 순서
```latex
\usepackage{array}        % 기본 배열/테이블 향상
\usepackage{tabularx}     % 반응형 칼럼
\usepackage{longtable}    % 다중 페이지 테이블
\usepackage{adjustbox}    % 스케일링 및 조정
\usepackage{booktabs}     % 전문적 테이블 포맷
```

### 2. 칼럼 타입 선택
- `X`: tabularx에서 래핑되는 콘텐츠용
- `l`, `c`, `r`: 고정 너비 콘텐츠용
- `>{\centering\arraybackslash}X`: 중앙정렬 래핑 칼럼
- `p{width}`: 고정 너비 단락 칼럼

### 3. 오류 방지
- 항상 `\usepackage` 사용 (`\usepackag` 아님)
- 괄호 매칭 주의깊게 확인
- 자주 컴파일 테스트 수행
- 테두리용 `\hline` 적절히 사용

## 문제 해결

### 일반적 오류 및 해결책

1. **정의되지 않은 제어 시퀀스 `\usepackag`**
   - 해결: `\usepackage`로 수정

2. **패키지를 찾을 수 없음**
   - LaTeX 패키지 설치
   - 패키지 이름 철자 확인

3. **테이블이 너무 넓다는 경고**
   - `adjustbox`로 스케일링
   - `tabularx`로 반응형 디자인 변경
   - 내용 줄이기 또는 테이블 분할

4. **칼럼 정렬 오류**
   - 칼럼 지정이 데이터 칼럼과 일치하는지 확인
   - `\hline` 및 `&` 위치 확인
   - 적절한 칼럼 타입 사용

## 향후 유지보수

1. **정기적 백업**: 중요한 수정 전 백업 파일 생성
2. **버전 관리**: Git을 통한 변경사항 추적
3. **컴파일 테스트**: 수정 후 즉시 컴파일 확인
4. **문서화**: 주요 변경사항 기록

이 가이드를 따르면 한국어 논문의 원본 내용을 보존하면서 테이블 너비 문제를 효과적으로 해결할 수 있습니다.