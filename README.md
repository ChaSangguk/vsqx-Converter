# VSQX Converter

VSQX 파일의 발음 표기 데이터를 다른 언어 체계에 맞게 변환해주는 도구입니다.

이 프로젝트는 VOCALOID 계열 보이스뱅크에서 사용하는 VSQX XML 형식을 읽고, 특정 언어 간 발음 매핑 규칙을 적용해 변환 결과를 새 파일로 저장합니다. 주 사용 흐름은 GUI 기반의 파일 선택 및 변환이며, 내부적으로는 `controller -> service -> model` 구조로 작업을 분리하려고 정리되어 있습니다.

## 주요 기능

- VSQX XML 파일 읽기
- 언어 간 발음 표기 변환 규칙 적용
- 여러 파일 일괄 변환
- GUI 기반 선택 및 변환 실행
- 변환 결과를 새 파일로 저장 (`_updated.vsqx`)
- 실패 파일과 에러 메시지 로그 기록

## 지원 환경

- Python 3.10 이상 권장
- `lxml` 필요
- Tkinter 기반 GUI 사용

## 설치

1. 저장소를 클론합니다.
   ```bash
   git clone https://github.com/ChaSangguk/vsqx-Converter.git
   cd vsqx-Converter
   ```

2. 가상 환경을 만들고 의존성을 설치합니다.
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install lxml
   ```

3. 프로젝트를 실행합니다.
   ```bash
   python main.py
   ```

## 사용 방법

프로그램을 실행하면 GUI 창이 열립니다.

1. 시작 언어 선택
2. 도착 언어 선택
3. 변환할 VSQX 파일 선택
4. 변환 완료 후 결과 파일 확인

예를 들어 다음과 같은 변환 규칙이 설정되어 있습니다.

- `jpnToKor`
- `korToJpn`
- `jpnToEng`

변환 규칙은 `list/convert.json`에서 관리됩니다.

## 변환 동작 방식

프로젝트의 핵심 흐름은 다음과 같습니다.

1. `main.py`에서 GUI를 실행
2. `view/gui.py`에서 파일 선택 및 언어 조합 수집
3. `controller/controller.py`에서 변환 요청 생성
4. `service/conversion_service.py`에서 변환 규칙 로드 및 VSQX 처리
5. `model/vsqx_convert.py`에서 실제 XML 변환 수행
6. 결과 파일이 저장됨

## 파일 구조

```text
vsqx-Converter/
├── config/
│   └── setting.py              # 경로, JSON 로딩, 기본 설정
├── controller/
│   ├── controller.py           # GUI와 서비스 연결
│   └── errorController.py     # 사용자 정의 예외
├── list/
│   ├── convert.json            # 변환 경로/언어 정보
│   ├── jpnTokor.json           # 일본어 -> 한국어 규칙
│   ├── korTojpn.json           # 한국어 -> 일본어 규칙
│   └── jpnToeng.json           # 일본어 -> 영어 규칙
├── model/
│   ├── conversion_request.py   # 변환 요청 DTO
│   ├── conversion_result.py    # 변환 결과 DTO
│   ├── vsqx_convert.py         # XML 변환 엔진
│   └── __init__.py
├── service/
│   ├── conversion_service.py   # 비즈니스 로직 서비스
│   ├── service.py              # 서비스 진입점/호환 래퍼
│   └── __init__.py
├── view/
│   ├── gui.py                  # Tkinter GUI
│   └── __init__.py
├── locales/
├── log/
├── main.py                     # 실행 진입점
├── README.md
├── LICENSE
└── .gitignore
```

## 변환 규칙 파일

`list/convert.json`에는 언어 조합과 각 규칙 파일 경로가 정의됩니다.

예시:

```json
{
  "jpnTokor": {
    "from": "jpn",
    "to": "kor",
    "path": "list/jpnTokor.json"
  },
  "korTojpn": {
    "from": "kor",
    "to": "jpn",
    "path": "list/korTojpn.json"
  }
}
```

규칙 파일 자체는 `singular`, `multiple` 키를 가지는 사전형 매핑 구조를 사용합니다.

## 출력 동작

- 입력: `example.vsqx`
- 출력: `example_updated.vsqx`
- 이미 같은 이름의 결과 파일이 존재하면 자동으로 `_1`, `_2` 형태로 파일명을 보완합니다.

## 주의사항

- 변환은 XML 구조를 기반으로 수행하므로 파일이 손상되었거나 비정상적인 XML이면 실패할 수 있습니다.
- 규칙 파일이 없거나 잘못된 형식이면 변환이 중단됩니다.
- 이 프로젝트는 개인용 변환 도구로 시작되었고, 현재는 구조 정리와 예외 처리 개선이 진행 중인 상태입니다.

## 개발 상태

현재 프로젝트는 기능 동작을 중심으로 만들어졌으며, 구조 개선과 서비스 계층 분리가 진행되고 있습니다. 다만 배포용 품질 기준을 맞추기 위해 다음이 보완되면 더 안정적입니다.

- 테스트 코드 추가
- 더 명확한 예외 분류
- 변환 실패 항목 상세 보고
- 사용자 문서 추가
- 실제 샘플 파일 End-to-End 검증

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
